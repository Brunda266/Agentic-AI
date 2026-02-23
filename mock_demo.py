from mock_llm_service import ask_llm

query = input("Enter your query:")
response = ask_llm("You are a helpful AI", query, temperature=0.6)

print("\n Mock AI Response :\n")
print(response)