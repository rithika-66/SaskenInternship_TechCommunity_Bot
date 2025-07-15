from rag_pipeline import answer_query

while True:
    user_input = input("❓ Ask your tech question (or type 'exit'): ")
    if user_input.lower() == "exit":
        break
    answer = answer_query(user_input)
    print("🤖 Answer:", answer)
