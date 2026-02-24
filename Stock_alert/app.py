import streamlit as st
from intent_detector import detect_intent
from llm_engine import generate_explanation
from output_filter import filter_output

st.set_page_config(page_title="Financial Risk Explanation Tool", layout="centered")

st.title("📊 Financial Risk Explanation Tool")
st.write("Educational AI explaining mutual funds safely.")

user_input = st.text_area("Ask about mutual funds, risks, or diversification:")

if st.button("Generate Explanation"):

    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        intent = detect_intent(user_input)

        if intent["intent"] == "investment_advice":
            st.error("🚫 I cannot provide specific investment advice. Please consult a licensed financial advisor.")
        else:
            try:
                explanation = generate_explanation(user_input)
                filtered = filter_output(explanation)

                if filtered["status"] == "blocked":
                    st.error(filtered["message"])
                else:
                    st.success("AI Response")
                    st.write(filtered["message"])

                    confidence = 0.95 if intent["risk_level"] == "low" else 0.40
                    st.info(f"Confidence Score: {confidence}")

            except Exception:
                st.error("⚠️ System error. Please check API key or try again.")