import streamlit as st
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from prompts import *
# Streamlit UI
st.title("Submit Expense")
expense_type = st.radio("", ["Expense", "Mileage"], horizontal=True)

expense_date = st.date_input("Expense Date")
expense_time = st.time_input("Expense Time")
merchant = st.text_input("Merchant")
amount = st.text_input("Amount", value="$ 0.00")
notes = st.text_area("Notes", placeholder="What was this expense for?")
receipt = st.file_uploader("Receipt", type=["png", "jpg", "pdf"], help="We can pull your transaction details automatically.")

if st.button("Review"):
    # Here is where you'd integrate the OpenAI call
    transaction_details = {
        'expense_date': expense_date,
        'expense_time': expense_time,
        'transaction_merchant': merchant,
        'transaction_amount': amount,
        'transaction_notes': notes,
        'transaction_receipt': receipt
    }
    # Mocking OpenAI response
    result = transaction_chain.invoke({'transaction': transaction_details})

    st.subheader("Categorization Result")
    # Recommended Category Dropdown
    category_options = [result.transaction_category.value] + \
                       [cat.value for cat in result.alternative_categories]
    selected_category = st.selectbox("Recommended Category", options=category_options)
    st.info(f"Explanation: {result.transaction_category_explanation} \n Confidence: {result.transaction_category_confidence}")

    st.markdown("### Accounting Use")
    gl_code_options = [result.gl_code.value] + \
                      [gl.value for gl in result.alternative_gl_codes]
    selected_gl_code = st.selectbox("GL Code", options=gl_code_options)
    st.info(f"Explanation: {result.gl_code_explanation} \nConfidence:, {result.gl_code_confidence}")