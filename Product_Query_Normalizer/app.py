"""
Interactive Streamlit UI for Product Query Normalizer.
Provides user-friendly interface for query parsing, ambiguity detection, and clarification.
"""

import streamlit as st
from schemas import ProductTypeEnum, UsageContextEnum
from normalizer import ProductQueryNormalizer


def init_session_state():
    """Initialize session state for the Streamlit app."""
    if "normalizer" not in st.session_state:
        st.session_state.normalizer = ProductQueryNormalizer()
    if "step" not in st.session_state:
        st.session_state.step = "input"  # input, review, clarify, results
    if "query" not in st.session_state:
        st.session_state.query = ""
    if "parsed_result" not in st.session_state:
        st.session_state.parsed_result = None
    if "user_responses" not in st.session_state:
        st.session_state.user_responses = {}


def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Product Query Normalizer",
        page_icon="🛍️",
        layout="wide",
    )

    st.markdown("# 🛍️ Product Query Normalizer")
    st.markdown(
        "Parse and clarify your product search queries with structured analysis."
    )

    init_session_state()

    # Sidebar for info
    with st.sidebar:
        st.markdown("## About")
        st.markdown(
            "This tool helps normalize e-commerce product queries by:\n"
            "- Extracting product type, price, usage context, features\n"
            "- Detecting ambiguities and missing information\n"
            "- Running clarification loops\n"
            "- Validating against business rules"
        )

        st.markdown("## Features")
        st.markdown(
            "✅ Schema enforcement (Pydantic)\n"
            "✅ Ambiguity detection\n"
            "✅ Interactive clarification\n"
            "✅ Budget validation\n"
            "✅ Confidence scoring"
        )

    # Main content
    tabs = st.tabs(["Parse Query", "Examples", "About"])

    with tabs[0]:
        st.markdown("## Step 1: Enter Your Query")
        query_input = st.text_area(
            "What product are you looking for?",
            placeholder="e.g., Best headphones around 4k for gym",
            height=100,
        )

        if st.button("🔍 Parse Query", type="primary"):
            if query_input.strip():
                st.session_state.query = query_input
                st.session_state.parsed_result = st.session_state.normalizer.normalize(
                    query_input
                )
                st.session_state.step = "review"
                st.rerun()
            else:
                st.warning("Please enter a product query.")

        # Display results if available
        if st.session_state.parsed_result:
            st.markdown("---")
            st.markdown("## Step 2: Review Parsed Data")

            result = st.session_state.parsed_result
            parsed = result.parsed_query

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Extracted Information")
                st.metric(
                    "Product Type",
                    parsed.product_type.value,
                    delta=f"Confidence: {parsed.confidence_score:.0%}",
                )

                if parsed.price_range:
                    st.metric(
                        "Budget Range",
                        f"₹{parsed.price_range.min_price:.0f} - ₹{parsed.price_range.max_price:.0f}",
                    )
                else:
                    st.info("No price range detected")

            with col2:
                st.markdown("### Context & Features")
                if parsed.usage_context:
                    contexts = ", ".join([c.value for c in parsed.usage_context])
                    st.success(f"**Usage:** {contexts}")
                else:
                    st.warning("No usage context detected")

                if parsed.feature_preferences:
                    features = ", ".join(parsed.feature_preferences)
                    st.success(f"**Features:** {features}")
                else:
                    st.warning("No features detected")

            # Show completeness
            st.markdown("---")
            if parsed.is_complete:
                st.success("✅ Query is complete!")
            else:
                st.warning(
                    f"⚠️ Missing fields: {', '.join(parsed.missing_fields)}"
                )

            # Show ambiguities and clarifications
            ambiguities = st.session_state.normalizer.get_ambiguities(
                st.session_state.query
            )

            if ambiguities:
                st.markdown("## Step 3: Clarify Ambiguities")
                st.markdown(
                    f"Found **{len(ambiguities)}** field(s) that could use clarification:"
                )

                for amb in ambiguities:
                    with st.expander(f"📝 {amb.field_label}"):
                        st.markdown(f"**Question:** {amb.question}")

                        if amb.field_name == "product_type" and amb.options:
                            response = st.selectbox(
                                f"Select {amb.field_label}",
                                options=amb.options,
                                key=f"response_{amb.field_name}",
                            )
                            st.session_state.user_responses[amb.field_name] = response

                        elif amb.field_name == "price_range":
                            response = st.number_input(
                                "Enter maximum budget (₹)",
                                min_value=0,
                                step=1000,
                                key=f"response_{amb.field_name}",
                            )
                            if response > 0:
                                st.session_state.user_responses[amb.field_name] = str(
                                    response
                                )

                        elif amb.field_name == "usage_context" and amb.options:
                            response = st.selectbox(
                                f"Select {amb.field_label}",
                                options=amb.options,
                                key=f"response_{amb.field_name}",
                            )
                            st.session_state.user_responses[amb.field_name] = response

                        elif amb.field_name == "feature_preferences" and amb.options:
                            selected = st.multiselect(
                                f"Select important {amb.field_label}",
                                options=amb.options,
                                key=f"response_{amb.field_name}",
                            )
                            if selected:
                                st.session_state.user_responses[amb.field_name] = (
                                    ", ".join(selected)
                                )

                        else:
                            response = st.text_input(
                                f"Clarify {amb.field_label}",
                                key=f"response_{amb.field_name}",
                            )
                            if response:
                                st.session_state.user_responses[amb.field_name] = (
                                    response
                                )

                # Re-normalize with clarifications
                if st.button("✅ Apply Clarifications"):
                    clarified_result = st.session_state.normalizer.normalize(
                        st.session_state.query,
                        st.session_state.user_responses,
                    )
                    st.session_state.parsed_result = clarified_result
                    st.rerun()

                st.markdown("---")

            # Show validation results
            if result.validation_errors:
                st.markdown("### ⚠️ Validation Issues")
                for error in result.validation_errors:
                    st.error(f"• {error}")
            elif result.is_valid:
                st.success("✅ Query passed all validation checks!")

            # Show final details
            with st.expander("📊 Detailed Results"):
                st.json(
                    {
                        "product_type": parsed.product_type.value,
                        "price_range": (
                            {
                                "min": parsed.price_range.min_price,
                                "max": parsed.price_range.max_price,
                            }
                            if parsed.price_range
                            else None
                        ),
                        "usage_context": [c.value for c in parsed.usage_context],
                        "features": parsed.feature_preferences,
                        "confidence_score": parsed.confidence_score,
                        "is_complete": parsed.is_complete,
                        "is_valid": result.is_valid,
                    }
                )

    with tabs[1]:
        st.markdown("## Example Queries")
        st.markdown(
            "Try these queries to see how the normalizer works:"
        )

        examples = [
            ("Best headphones around 4k for gym", "headphones"),
            ("Gaming laptop under 100000", "laptop"),
            ("Waterproof earbuds for running", "earbuds"),
            ("Professional microphone for streaming", "microphone"),
            ("Budget smartphone 15k for office", "phone"),
            ("i need a good camera", "camera"),
        ]

        for i, (query, product) in enumerate(examples):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{i+1}.** {query}")
                st.caption(f"Product: {product}")
            with col2:
                if st.button("Try", key=f"example_{i}"):
                    st.session_state.query = query
                    st.session_state.parsed_result = (
                        st.session_state.normalizer.normalize(query)
                    )
                    st.session_state.step = "review"
                    st.rerun()
            st.divider()

    with tabs[2]:
        st.markdown("## How It Works")

        st.markdown("### 📋 Architecture")
        st.markdown(
            """
        1. **Parser**: Extracts product type, price, context, features using regex and keywords
        2. **Detector**: Identifies ambiguities and missing information
        3. **Clarifier**: Runs interactive loop for user inputs
        4. **Validator**: Enforces business rules (budget ranges, numeric validation)
        5. **Normalizer**: Orchestrates the full pipeline
        """
        )

        st.markdown("### 🔍 Key Features")
        st.markdown(
            """
        - **Schema Enforcement**: Uses Pydantic for strict validation
        - **Ambiguity Detection**: Automatically identifies unclear fields
        - **Clarification Loop**: Asks users for specific missing information
        - **Business Rule Validation**: Checks budget is reasonable for product type
        - **Confidence Scoring**: Indicates how confident the parse is (0-100%)
        """
        )

        st.markdown("### 💼 Supported Products")
        products = [p.value for p in ProductTypeEnum if p != ProductTypeEnum.UNKNOWN]
        st.markdown(", ".join(products))

        st.markdown("### 🎯 Usage Contexts")
        contexts = [c.value for c in UsageContextEnum if c != UsageContextEnum.UNKNOWN]
        st.markdown(", ".join(contexts))


if __name__ == "__main__":
    main()
