from pathlib import Path

from data_loader import load_data
from knowledge_graph import create_graph
from llm import question_to_intent, generate_answer
from retrieval import execute_intent


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# =========================================================
# LOAD DATA
# =========================================================

print("Loading dataset...")

data = load_data(str(DATA_DIR))


# =========================================================
# CREATE KNOWLEDGE GRAPH
# =========================================================

print("Creating knowledge graph...")

graph = create_graph(data)

print("Graph created successfully!")
print(f"Nodes: {graph.number_of_nodes()}")
print(f"Edges: {graph.number_of_edges()}")


# =========================================================
# ASK USER QUESTION
# =========================================================

print("\n========================================")
print(" E-COMMERCE KNOWLEDGE GRAPH")
print("========================================")


question = input("\nAsk a question: ").strip()


if not question:

    print("\nNo question was provided.")
    raise SystemExit(0)


# =========================================================
# QUESTION -> INTENT
# =========================================================

print("\nUnderstanding question...")

try:

    intent = question_to_intent(question)

except Exception as error:

    print("\nCould not understand the question.")
    print(f"Error: {error}")
    raise SystemExit(1)


print("\nGenerated Intent:")
print(intent)


# =========================================================
# INTENT -> GRAPH RETRIEVAL
# =========================================================

print("\nRetrieving data from knowledge graph...")

try:

    retrieved_data = execute_intent(
        graph,
        intent
    )

except Exception as error:

    print("\nKnowledge graph retrieval failed.")
    print(f"Error: {error}")
    raise SystemExit(1)


print("\nRetrieved Graph Data:")
print(retrieved_data)


# =========================================================
# GRAPH DATA -> FINAL ANSWER
# =========================================================

print("\nGenerating final answer...")

try:

    answer = generate_answer(
        question,
        retrieved_data
    )

except Exception as error:

    print("\nCould not generate the final answer.")
    print(f"Error: {error}")
    raise SystemExit(1)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n========================================")
print(" ANSWER")
print("========================================")

print(answer)