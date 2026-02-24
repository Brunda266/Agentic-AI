from intent_detector import detect_intent
from llm_engine import generate_explanation
from output_filter import filter_output

def calculate_confidence(intent):
    if intent["risk_level"] == "low":
        return 0.95
    return 0.40

def main():
    print("📊 Financial Risk Explanation Tool")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        intent = detect_intent(user_input)

        if intent["intent"] == "investment_advice":
            print("\n🚫 I cannot provide specific investment advice.")
            print("Please consult a licensed financial advisor.\n")
            continue

        try:
            explanation = generate_explanation(user_input)
            filtered = filter_output(explanation)

            if filtered["status"] == "blocked":
                print(filtered["message"])
            else:
                confidence = calculate_confidence(intent)
                print("\nAI Response:\n")
                print(filtered["message"])
                print(f"\nConfidence Score: {confidence}")

        except Exception as e:
            print("⚠️ System error. Please try again.")

if __name__ == "__main__":
    main()