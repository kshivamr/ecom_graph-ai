import os

from llm import question_to_intent, generate_answer


print("Running LLM tests...")


# ---------------------------------------------------------
# CHECK API KEY
# ---------------------------------------------------------

if not os.getenv("GROQ_API_KEY"):

    print(
        "SKIP: GROQ_API_KEY is not available. "
        "LLM integration tests were skipped."
    )

    raise SystemExit(0)


# ---------------------------------------------------------
# TEST 1: QUESTION -> INTENT
# ---------------------------------------------------------

intent = question_to_intent(
    "Which products from Apple are supplied by TechWorld?"
)

assert isinstance(intent, dict)

assert intent["operation"] == (
    "products_by_brand_and_vendor"
)

assert intent["brand"].lower() == "apple"
assert intent["vendor"].lower() == "techworld"

print("PASS: LLM intent generation.")


# ---------------------------------------------------------
# TEST 2: PRODUCT INTENT
# ---------------------------------------------------------

intent = question_to_intent(
    "What is the price of iPhone 15?"
)

assert intent["operation"] == "product_details"

assert intent["product_name"].lower() == "iphone 15"

print("PASS: Product intent generation.")


# ---------------------------------------------------------
# TEST 3: BANANA INTENT
# ---------------------------------------------------------

intent = question_to_intent(
    "Show me all banana products"
)

assert intent["operation"] == "banana_products"

print("PASS: Banana intent generation.")


# ---------------------------------------------------------
# TEST 4: GROUNDED FINAL ANSWER
# ---------------------------------------------------------

retrieved_data = {
    "product_id": "P001",
    "product_name": "iPhone 15",
    "price": 69999,
    "brand": "Apple",
    "category": "Smartphones",
    "vendor": "TechWorld"
}

answer = generate_answer(
    "What is the price of iPhone 15?",
    retrieved_data
)

assert isinstance(answer, str)
assert len(answer.strip()) > 0

assert "69999" in answer or "69,999" in answer

print("PASS: Final grounded answer generation.")


print("\nAll LLM tests passed successfully!")