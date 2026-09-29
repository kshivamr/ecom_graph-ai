import os
import json

from dotenv import load_dotenv
from groq import Groq
from groq import APIError


# Load environment variables
load_dotenv()


def get_client():
    """
    Create and return the Groq client.

    The API key is checked only when the LLM is actually used.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. "
            "Please add it to your .env file."
        )

    return Groq(api_key=api_key)


# =========================================================
# QUESTION -> STRUCTURED INTENT
# =========================================================

def question_to_intent(question):
    """
    Convert a natural-language question into a structured
    JSON intent that can be executed by the retrieval layer.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    client = get_client()

    system_prompt = """
You are a query parser for an e-commerce Knowledge Graph.

Your job is ONLY to understand the user's question and
convert it into a structured JSON intent.

Do NOT answer the user's question.

Do NOT invent IDs.

Do NOT invent product IDs, customer IDs, brand IDs,
category IDs, vendor IDs, or order IDs.

Use names exactly as they appear in the user's question.

--------------------------------------------------
KNOWLEDGE GRAPH ENTITIES
--------------------------------------------------

- Product
- Brand
- Category
- Vendor
- Customer
- Order

--------------------------------------------------
RELATIONSHIPS
--------------------------------------------------

Customer -> PLACED -> Order

Order -> CONTAINS -> Product

Product -> MADE_BY -> Brand

Product -> BELONGS_TO -> Category

Product -> SUPPLIED_BY -> Vendor

--------------------------------------------------
SUPPORTED OPERATIONS
--------------------------------------------------

1. product_details

Use when the user asks about one specific product.

Required field:
product_name

Example:

Question:
"What is the price of iPhone 15?"

Return:

{
    "operation": "product_details",
    "product_name": "iPhone 15"
}


2. products_by_category

Use when the user asks for products belonging to
a particular category.

Required field:
category

Example:

Question:
"Show me products in Fruits category"

Return:

{
    "operation": "products_by_category",
    "category": "Fruits"
}


3. products_by_brand_and_vendor

Use when the user asks for products that satisfy
BOTH a brand and a vendor condition.

Required fields:
brand
vendor

Example:

Question:
"Which products from Apple are supplied by TechWorld?"

Return:

{
    "operation": "products_by_brand_and_vendor",
    "brand": "Apple",
    "vendor": "TechWorld"
}


Another example:

Question:
"Show products made by Samsung and supplied by ElectroMart"

Return:

{
    "operation": "products_by_brand_and_vendor",
    "brand": "Samsung",
    "vendor": "ElectroMart"
}


4. customer_orders

Use when the user asks what a customer ordered.

Required field:
customer_name

Example:

Question:
"What has Rahul Sharma ordered?"

Return:

{
    "operation": "customer_orders",
    "customer_name": "Rahul Sharma"
}


5. search_products

Use when the user wants to search product names
using a general search term.

Required field:
search_term

Example:

Question:
"Find products containing mouse"

Return:

{
    "operation": "search_products",
    "search_term": "mouse"
}


6. banana_products

Use when the user specifically asks for banana products
or asks to show all banana products.

No additional field is required.

Example:

Question:
"Show me all banana products"

Return:

{
    "operation": "banana_products"
}

--------------------------------------------------
IMPORTANT RULES
--------------------------------------------------

Rule 1:
Return ONLY valid JSON.

Rule 2:
Do NOT return Markdown.

Rule 3:
Do NOT explain your answer.

Rule 4:
Do NOT answer the user's question.

Rule 5:
Never invent IDs.

Rule 6:
Prefer entity names from the user's question.

Rule 7:
If the user mentions both a brand and a vendor and
asks which products satisfy both conditions, use:

products_by_brand_and_vendor

Rule 8:
If the user asks for banana products, use:

banana_products

Rule 9:
Do not confuse a relationship query with a simple
product-name search.

--------------------------------------------------
OUTPUT FORMAT
--------------------------------------------------

Return exactly one JSON object.
"""

    # -----------------------------------------------------
    # CALL GROQ
    # -----------------------------------------------------

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0
        )

    except APIError as error:

        raise RuntimeError(
            f"LLM API request failed: {error}"
        ) from error

    except Exception as error:

        raise RuntimeError(
            f"Unexpected error while calling the LLM: {error}"
        ) from error

    # -----------------------------------------------------
    # CHECK RESPONSE
    # -----------------------------------------------------

    if not response.choices:

        raise ValueError(
            "LLM returned no response choices."
        )

    result = response.choices[0].message.content

    if not result:

        raise ValueError(
            "LLM returned an empty response."
        )

    result = result.strip()

    # -----------------------------------------------------
    # REMOVE MARKDOWN JSON CODE FENCES
    # -----------------------------------------------------

    if result.startswith("```json"):

        result = result[7:]

    elif result.startswith("```"):

        result = result[3:]

    if result.endswith("```"):

        result = result[:-3]

    result = result.strip()

    # -----------------------------------------------------
    # PARSE JSON
    # -----------------------------------------------------

    try:

        intent = json.loads(result)

    except json.JSONDecodeError as error:

        raise ValueError(
            "LLM returned invalid JSON.\n"
            f"LLM response: {result}\n"
            f"Error: {error}"
        ) from error

    # -----------------------------------------------------
    # VALIDATE INTENT TYPE
    # -----------------------------------------------------

    if not isinstance(intent, dict):

        raise ValueError(
            "LLM intent must be a JSON object."
        )

    # -----------------------------------------------------
    # CHECK OPERATION
    # -----------------------------------------------------

    if "operation" not in intent:

        raise ValueError(
            "LLM intent does not contain an operation."
        )

    supported_operations = {
        "product_details",
        "products_by_category",
        "products_by_brand_and_vendor",
        "customer_orders",
        "search_products",
        "banana_products"
    }

    operation = intent["operation"]

    if operation not in supported_operations:

        raise ValueError(
            f"Unsupported operation returned by LLM: {operation}"
        )

    return intent


# =========================================================
# RETRIEVED DATA -> FINAL ANSWER
# =========================================================

def generate_answer(question, retrieved_data):
    """
    Generate the final answer using ONLY the data retrieved
    from the Knowledge Graph.

    The LLM is not allowed to introduce information that
    does not exist in retrieved_data.
    """

    # -----------------------------------------------------
    # CHECK QUESTION
    # -----------------------------------------------------

    if not question or not question.strip():

        return (
            "I don't have enough information "
            "to answer this question."
        )

    # -----------------------------------------------------
    # NO RETRIEVED DATA
    # -----------------------------------------------------

    if not retrieved_data:

        return (
            "I don't have enough information "
            "in the knowledge graph to answer this question."
        )

    # -----------------------------------------------------
    # RETRIEVAL ERROR
    # -----------------------------------------------------

    if isinstance(retrieved_data, dict):

        if "error" in retrieved_data:

            return (
                "I don't have enough information "
                "in the knowledge graph to answer this question."
            )

    client = get_client()

    # -----------------------------------------------------
    # CONVERT RETRIEVED DATA TO JSON
    # -----------------------------------------------------

    try:

        retrieved_json = json.dumps(
            retrieved_data,
            indent=2,
            ensure_ascii=False
        )

    except (TypeError, ValueError) as error:

        raise ValueError(
            f"Retrieved data could not be converted to JSON: {error}"
        ) from error

    # -----------------------------------------------------
    # FINAL ANSWER SYSTEM PROMPT
    # -----------------------------------------------------

    system_prompt = """
You are the final answer generator for an
e-commerce Knowledge Graph system.

Your job is to answer the user's question using
ONLY the retrieved data provided to you.

IMPORTANT GROUNDING RULES:

1. Use ONLY the retrieved data.

2. Do NOT use your own world knowledge.

3. Do NOT invent facts.

4. Do NOT calculate or assume information that is
   not directly supported by the retrieved data.

5. Do NOT add products, prices, brands, vendors,
   customers, quantities, or categories that are
   not present in the retrieved data.

6. If the retrieved data does not contain enough
   information to answer the question, say:

"I don't have enough information in the knowledge graph
to answer this question."

7. Give a concise and natural answer.

8. Do not mention internal implementation details
   unless the user asks about them.

The retrieved data is the ONLY source of truth.
"""

    user_prompt = f"""
User Question:
{question}

Retrieved Knowledge Graph Data:
{retrieved_json}

Answer the user's question using ONLY the
retrieved Knowledge Graph Data.
"""

    # -----------------------------------------------------
    # CALL GROQ FOR FINAL ANSWER
    # -----------------------------------------------------

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0
        )

    except APIError as error:

        return (
            "I couldn't generate the final answer because "
            f"the LLM API request failed: {error}"
        )

    except Exception as error:

        return (
            "I couldn't generate the final answer because "
            f"an unexpected LLM error occurred: {error}"
        )

    # -----------------------------------------------------
    # CHECK FINAL RESPONSE
    # -----------------------------------------------------

    if not response.choices:

        return (
            "I couldn't generate an answer because "
            "the LLM returned no response."
        )

    answer = response.choices[0].message.content

    if not answer:

        return (
            "I couldn't generate an answer because "
            "the LLM returned an empty response."
        )

    return answer.strip()