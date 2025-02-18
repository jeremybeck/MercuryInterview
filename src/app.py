import pandas as pd
from prompts import *
from policy_qa import *
import plotly.express as px

tab1, tab2, tab3 = st.tabs(['Submit Expenses', 'Expense Report', 'How It Works'])

with tab1:
    # Streamlit UI
    st.title("Submit Expense")
    expense_type = st.radio("", ["Expense", "Mileage (Deactivated)"], horizontal=True)

    expense_date = st.date_input("Expense Date")
    expense_time = st.time_input("Expense Time")
    merchant = st.text_input("Merchant")
    amount = st.text_input("Amount", value="$ 0.00")
    notes = st.text_area("Notes", placeholder="What was this expense for?")
    receipt = st.file_uploader("Receipt", type=["png", "jpg", "pdf"], help="Upload a Receipt")

    @st.cache_resource()
    def invoke_transaction_chain(transaction_details):
        answer = transaction_chain.invoke({'transaction': transaction_details})
        return answer

    def invoke_policy_chain(_result):
        approval_response = policy_chain(_result.json())
        return approval_response


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
        result = invoke_transaction_chain(transaction_details)

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

        result.transaction_category = selected_category
        result.gl_code = selected_gl_code

        # Policy Review
        approval_response = invoke_policy_chain(result)

        # Create the ApprovalResponse object

        # Display the response
        if approval_response.policy_flag == 'Allowed':
            st.info(
                f"**Policy Review**: {approval_response.policy_flag}\n\n**Explanation**: {approval_response.policy_explanation}\n\n**Recommendation**: {approval_response.recommendation}")
        elif approval_response.policy_flag == 'Disallowed':
            st.error(
                f"**Policy Review**: {approval_response.policy_flag}\n\n**Explanation**: {approval_response.policy_explanation}\n\n**Recommendation**: {approval_response.recommendation}")
        else:
            st.warning(
                f"**Policy Review**: {approval_response.policy_flag}\n\n**Explanation**: {approval_response.policy_explanation}\n\n**Recommendation**: {approval_response.recommendation}")


with tab2:
    # Sample DataFrame for demonstration purposes
    df = pd.read_parquet('./data/transactions_processed.parquet').sort_values(by='AMOUNT')

    # Group transactions by policy decision
    allowed = df[df['policy_decision'] == 'Allowed']
    disallowed = df[df['policy_decision'] == 'Disallowed']
    more_info = df[df['policy_decision'] == 'More Information Required']

    # Calculate high level metrics
    total_transactions = len(df)
    total_amount = df['AMOUNT'].sum().round(2)
    gl_code_counts = df['policy_gl_code'].value_counts().reset_index()
    gl_code_counts.columns = ['GL Code', 'Count']

    # Streamlit UI
    st.title('Event Report: Product Onsite')

    with st.container(border=True):
        st.header('Overview')
        col1, col2, col3 = st.columns(3)
        col1.metric(label='Total Transactions', value=total_transactions)
        col2.metric(label='Total Amount', value=f"${total_amount}")
        col3.metric(label='Unique GL Codes', value=len(gl_code_counts))

    # Plotly Column Plot for GL Codes
    fig_gl = px.bar(gl_code_counts, x='GL Code', y='Count', title='Spending by GL Code', color='GL Code')
    st.plotly_chart(fig_gl)

    # Pie Chart for Policy Decision Breakdown
    policy_counts = df['policy_decision'].value_counts().reset_index()
    policy_counts.columns = ['Policy Decision', 'Count']
    remap_dict = {
        'Allowed': 'Compliant',
        'Disallowed': 'Non-Compliant',
        'More Information Required': 'More Info Required'
    }

    # Remap the 'Policy Decision' column values
    policy_counts['Policy Decision'] = policy_counts['Policy Decision'].replace(remap_dict)
    order = ['Compliant', 'More Info Required', 'Non-Compliant']
    color_sequence = ['#1f77b4', '#d62728', '#aec7e8']
    policy_counts['Policy Decision'] = pd.Categorical(policy_counts['Policy Decision'], categories=order, ordered=True)

    fig_policy = px.pie(policy_counts, names='Policy Decision', values='Count', title='Policy Review')
    fig_policy.update_traces(marker=dict(colors=color_sequence))
    st.plotly_chart(fig_policy)

    with st.expander(f'Ready for Approval: {allowed.shape[0]}'):
        st.dataframe(allowed.style.applymap(lambda x: 'background-color: rgba(31, 119, 180, 0.3);'))

    with st.expander(f'More Information Required: {more_info.shape[0]}'):
        st.dataframe(more_info.style.applymap(lambda x: 'background-color: rgba(174, 199, 232, 0.3);'))

    with st.expander(f'Review Non-Compliant Transactions: {disallowed.shape[0]}'):
        st.dataframe(disallowed.style.applymap(lambda x: 'background-color: rgba(214, 39, 40, 0.3);'))

    with st.expander(f'Comparison of Model vs Manual Tags:'):
        st.dataframe(pd.crosstab(df['MERCURY_CATEGORY'], df['transaction_category']))


with tab3:

    next_up_str = '''
## Expense Categorization  
The current implementation leverages transaction details and a zero-shot prompt.  Specific Transaction details like those listed below can be modified to change tagging decisions. 
- Merchant Name
- Notes
- Time and Date of Transaction
- Receipt

For each transaction the system provides:
  1. A recommended tag/GL code
  2. An explanation for the tag/GL Code
  3. A confidence in the output (needs calibration in future versions)
  4. Alternative tags that may relate to the transaction.  

### Categorization Next Steps:  
- Incorporate **few-shot learning** using historical transactions to improve categorization accuracy.  
- Implement **representation learning** for embeddings using **Shared Encoder Networks** to fine-tune embeddings for classification and retrieval tasks.  

---

## Policy Assessments  
Policy assessments are conducted using **Retrieval Augmented Generation (RAG)** with a vector database that embeds and stores policy documents. 
The policy documents are processed, chunked according to document structure, and embedded. Metadata can be leveraged to filter to specific policies depending on whether the expense is related to general policy, travel, etc. Transaction details from above are then used to retrieve relevant policy chunks, and evaluate whether the transaction is allowed.  A next best action recommendation is also made to rectify any issues, or approve.  

### Next Steps:  
- Enhance RAG functionality by incorporating a more **agentic system** that can iterate through questions, and ask related followup questions to assess ambiguous policies.  
- Integrate historical transactions for users to enable accurate policy assessments, particularly for policies based on aggregated transactions (e.g., $100/week for lunch perks).  
'''

    st.markdown('    # Spend Management System Overview  ')
    st.info('Please note this is an early prototype app intended to demonstrate functionality and collect user feedback to assess value and priorities. There are many opportunities to improve functionality, and to that end a description of how the app currently works and intended next steps are included below')
    st.markdown(next_up_str)