# E-commerce Knowledge Graph & AI Retrieval System

## 1. Project Overview

This project implements a simple Knowledge Graph for an e-commerce dataset and an AI-powered retrieval system.

The system uses:

- Python
- Pandas
- NetworkX
- Groq LLM
- python-dotenv

The LLM converts natural-language questions into a structured intent. The intent is then executed against the Knowledge Graph to retrieve the required information.

The final answer is generated using only the data retrieved from the Knowledge Graph.

---

## 2. Problem Statement

The goal is to build a Knowledge Graph for an e-commerce system containing:

- Products
- Brands
- Categories
- Vendors
- Customers
- Orders

The system allows users to ask natural-language questions and retrieve relevant information from the Knowledge Graph.

### Example Questions

- What is the price of iPhone 15?
- Show me products in Fruits category.
- Which products from Apple are supplied by TechWorld?
- What has Rahul Sharma ordered?
- Find products containing mouse.
- Show me all banana products.

---

## 3. Architecture

```text
                    User Question
                          |
                          v
                  +---------------+
                  |    Groq LLM   |
                  | Query Parser  |
                  +---------------+
                          |
                          v
                  Structured Intent
                          |
                          v
                +-------------------+
                |   Knowledge Graph |
                |     NetworkX      |
                +-------------------+
                          |
                          v
                   Retrieved Data
                          |
                          v
                  +---------------+
                  |    Groq LLM   |
                  | Answer Generator|
                  +---------------+
                          |
                          v
                    Final Answer
```

The first LLM call understands the user's natural-language question and converts it into a structured intent.

The retrieval layer executes that intent against the NetworkX Knowledge Graph.

The retrieved graph data is then provided to the second LLM call, which generates the final response.

The Knowledge Graph is the source of truth for factual information.

---

## 4. Knowledge Graph

The graph is implemented using NetworkX.

### Entities

The graph contains the following entity types:

- Product
- Brand
- Category
- Vendor
- Customer
- Order

### Relationships

```text
Customer --PLACED--> Order

Order --CONTAINS--> Product

Product --MADE_BY--> Brand

Product --BELONGS_TO--> Category

Product --SUPPLIED_BY--> Vendor
```

These relationships allow the retrieval layer to perform graph traversal and answer questions involving products, brands, categories, vendors, customers, and orders.

---

## 5. Graph Statistics

The current dataset creates:

```text
Nodes: 58
Edges: 78
```

The graph contains:

```text
16 Product nodes
10 Brand nodes
6 Category nodes
6 Vendor nodes
5 Customer nodes
15 Order nodes
```

Total:

```text
16 + 10 + 6 + 6 + 5 + 15 = 58 nodes
```

The relationships include:

```text
16 Product -> Brand relationships
16 Product -> Category relationships
16 Product -> Vendor relationships
15 Customer -> Order relationships
15 Order -> Product relationships
```

Total:

```text
16 + 16 + 16 + 15 + 15 = 78 edges
```

---

## 6. Dataset

The project uses CSV files for the e-commerce data.

```text
data/
├── products.csv
├── brands.csv
├── categories.csv
├── vendors.csv
├── customers.csv
└── orders.csv
```

### Products

Products contain:

- Product ID
- Product name
- Brand ID
- Category ID
- Vendor ID
- Price

### Orders

Orders contain:

- Order ID
- Customer ID
- Product ID
- Quantity

---

## 7. Banana Requirement

The assignment requires the word `banana` to appear exactly five times as a node/value in the Knowledge Graph and to be retrievable.

The implementation satisfies this requirement using five Product name values.

### Banana Products

```text
P007 -> Banana
P008 -> Banana Smoothie
P009 -> Organic Banana
P010 -> Banana Chips
P016 -> Banana Bread
```

Therefore, exactly five Product values contain the word `banana`.

### Banana Retrieval

The system supports the question:

```text
Show me all banana products
```

The retrieval layer returns:

```text
Banana — ₹80

Banana Smoothie — ₹150

Organic Banana — ₹120

Banana Chips — ₹100

Banana Bread — ₹180
```

The validation script confirms that exactly five banana products exist.

Run:

```powershell
python validate_banana.py
```

Expected result:

```text
Total banana products: 5

SUCCESS: Banana requirement satisfied!
```

---

## 8. Retrieval System

The retrieval layer is implemented in:

```text
src/retrieval.py
```

It supports the following operations.

### Product Details

```text
product_details
```

Retrieves:

- Product name
- Price
- Brand
- Category
- Vendor

Example:

```text
What is the price of iPhone 15?
```

---

### Products by Category

```text
products_by_category
```

Retrieves products belonging to a specified category.

Example:

```text
Show me products in Fruits category
```

---

### Products by Brand and Vendor

```text
products_by_brand_and_vendor
```

Retrieves products matching both a specified brand and vendor.

Example:

```text
Which products from Apple are supplied by TechWorld?
```

---

### Customer Orders

```text
customer_orders
```

Retrieves products and quantities ordered by a customer.

Example:

```text
What has Rahul Sharma ordered?
```

---

### Product Search

```text
search_products
```

Searches product names using a search term.

Example:

```text
Find products containing mouse
```

---

### Banana Products

```text
banana_products
```

Retrieves all products whose product name contains the word `banana`.

Example:

```text
Show me all banana products
```

---

## 9. LLM Integration

Groq is used to convert natural-language questions into structured intents.

For example:

### User Question

```text
What is the price of iPhone 15?
```

### Generated Intent

```json
{
  "operation": "product_details",
  "product_name": "iPhone 15"
}
```

Another example:

### User Question

```text
What has Rahul Sharma ordered?
```

### Generated Intent

```json
{
  "operation": "customer_orders",
  "customer_name": "Rahul Sharma"
}
```

The structured intent is then passed to the retrieval layer.

### Supported Operations

```text
product_details
products_by_category
products_by_brand_and_vendor
customer_orders
search_products
banana_products
```

---

## 10. Grounding

The system is designed to keep the final answer grounded in the Knowledge Graph.

The complete process is:

```text
Natural Language Question
            |
            v
     LLM Intent Extraction
            |
            v
      Graph Retrieval
            |
            v
     Retrieved Graph Data
            |
            v
    LLM Answer Generation
            |
            v
       Final Answer
```

The LLM does not directly provide factual answers from its own knowledge.

Instead:

1. The user asks a natural-language question.
2. The first LLM converts the question into a structured intent.
3. The retrieval layer executes the intent against the Knowledge Graph.
4. The graph returns the relevant data.
5. The retrieved data is provided to the second LLM call.
6. The second LLM generates the final answer using the retrieved data.

This design helps keep the final answer grounded in the project's actual dataset and reduces unsupported information.

---

## 11. Sample Questions and Results

### Question 1

```text
What is the price of iPhone 15?
```

Retrieved information:

```text
Product: iPhone 15
Price: ₹69999
Brand: Apple
Category: Smartphones
Vendor: TechWorld
```

Example final answer:

```text
The price of the iPhone 15 is ₹69,999.
```

---

### Question 2

```text
Show me products in Fruits category
```

Retrieved products:

```text
Banana — ₹80
Banana Smoothie — ₹150
Organic Banana — ₹120
Banana Chips — ₹100
Banana Bread — ₹180
```

---

### Question 3

```text
Which products from Apple are supplied by TechWorld?
```

Retrieved products:

```text
iPhone 15 — ₹69999
MacBook Air M2 — ₹89999
```

---

### Question 4

```text
What has Rahul Sharma ordered?
```

Retrieved orders:

```text
iPhone 15 — quantity 1
Banana — quantity 5
MacBook Air M2 — quantity 1
```

---

### Question 5

```text
Find products containing mouse
```

Retrieved products:

```text
Wireless Mouse — ₹999
```

---

### Question 6

```text
Show me all banana products
```

Retrieved products:

```text
Banana — ₹80
Banana Smoothie — ₹150
Organic Banana — ₹120
Banana Chips — ₹100
Banana Bread — ₹180
```

---

## 12. Project Structure

```text
ecom_graph-ai/
│
├── data/
│   ├── products.csv
│   ├── brands.csv
│   ├── categories.csv
│   ├── vendors.csv
│   ├── customers.csv
│   └── orders.csv
│
├── src/
│   ├── data_loader.py
│   ├── knowledge_graph.py
│   ├── retrieval.py
│   ├── llm.py
│   ├── main.py
│   ├── test_graph.py
│   ├── test_retrieval.py
│   ├── test_llm.py
│   └── __init__.py
│
├── validate_banana.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

---

## 13. Installation

Clone or download the project.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the environment:

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## 14. Environment Variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_actual_groq_api_key
```

The `.env` file contains the private API key and should not be committed to GitHub.

A safe template is provided in:

```text
.env.example
```

The `.env.example` file should contain a placeholder rather than the actual API key.

---

## 15. Running the Project

Run the application from the project root:

```powershell
python src\main.py
```

The application will display:

```text
Ask a question:
```

Enter a natural-language question.

For example:

```text
Show me all banana products
```

The application then displays:

1. Generated intent
2. Retrieved graph data
3. Final grounded answer

Example flow:

```text
Ask a question: Show me all banana products

Understanding question...

Generated Intent:
{'operation': 'banana_products'}

Retrieving data from knowledge graph...

Retrieved Graph Data:
[...five banana products...]

Generating final answer...

ANSWER
...
```

---

## 16. Validation and Testing

The project contains separate tests for the graph, retrieval layer, and LLM integration.

### Graph Test

Run from the project root:

```powershell
python src\test_graph.py
```

The test verifies:

- Graph creation
- 58 nodes
- Required entity types
- Important nodes
- Required relationships
- Exactly 5 banana products

Expected final message:

```text
All graph tests passed successfully!
```

---

### Retrieval Test

Run:

```powershell
python src\test_retrieval.py
```

The test verifies:

- Product details
- Missing product handling
- Category retrieval
- Brand + vendor retrieval
- Customer orders
- Product search
- Exactly 5 banana products retrieved

Expected final message:

```text
All retrieval tests passed successfully!
```

---

### LLM Test

Run:

```powershell
python src\test_llm.py
```

The test verifies:

- LLM intent generation
- Product intent generation
- Banana intent generation
- Final grounded answer generation

Expected result:

```text
All LLM tests passed successfully!
```

---

### Banana Validation

Run:

```powershell
python validate_banana.py
```

Expected result:

```text
Banana products found:

P007 -> Banana
P008 -> Banana Smoothie
P009 -> Organic Banana
P010 -> Banana Chips
P016 -> Banana Bread

Total banana products: 5

SUCCESS: Banana requirement satisfied!
```

---

## 17. Technologies Used

| Technology    | Purpose                                             |
| ------------- | --------------------------------------------------- |
| Python        | Main programming language                           |
| Pandas        | CSV/data loading                                    |
| NetworkX      | Knowledge Graph implementation                      |
| Groq          | LLM-based query understanding and answer generation |
| python-dotenv | Environment variable management                     |

---

## 18. Design Decision

NetworkX was selected instead of Neo4j because this assignment requires a lightweight Knowledge Graph implementation.

NetworkX allows the project to represent:

- Nodes
- Relationships
- Attributes
- Graph traversal

without requiring a separate database server.

The retrieval layer performs graph traversal directly using NetworkX.

This makes the project simple to run locally while still demonstrating the core Knowledge Graph and AI retrieval architecture.

---

## 19. Future Improvements

Possible improvements include:

- Migrating the graph to Neo4j
- Supporting Cypher queries
- Adding more complex multi-hop queries
- Adding additional entity types
- Adding a web interface
- Adding conversational memory
- Adding graph visualization
- Adding automated evaluation tests
- Supporting more natural-language query variations

---

## 20. Demo

The Loom video demonstrates:

1. Project overview
2. Dataset structure
3. Knowledge Graph creation
4. Graph entities and relationships
5. Natural-language query processing
6. LLM integration
7. Graph retrieval
8. Grounded answer generation
9. Banana requirement
10. Sample queries and results

---

## 21. Conclusion

This project demonstrates how a Knowledge Graph can be combined with an LLM to provide natural-language access to structured e-commerce data.

The LLM is responsible for understanding the user's question and generating a structured intent.

The Knowledge Graph is responsible for retrieving the factual information.

The retrieved graph data is then passed to the LLM to generate the final response.

This creates a simple pipeline:

```text
User Question
      ↓
LLM Intent Extraction
      ↓
Knowledge Graph Retrieval
      ↓
Retrieved Data
      ↓
LLM Answer Generation
      ↓
Final Grounded Answer
```

The project also satisfies the required banana validation by containing exactly five Product name values containing the word `banana`.
