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

    def invoke_policy_chain(_result_to_pass):
        approval_response = policy_chain(_result_to_pass.json())
        return approval_response

    @st.cache_resource()
    def update_categories(_result):
        st.subheader("Categorization Result")
        # Recommended Category Dropdown
        # Store selections in session state
        if 'selected_category' not in st.session_state:
            st.session_state.selected_category = _result.transaction_category.value
        if 'selected_gl_code' not in st.session_state:
            st.session_state.selected_gl_code = _result.gl_code.value



    # Store the transaction details, result, and approval response in session state
    if 'transaction_details' not in st.session_state:
        st.session_state.transaction_details = None
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    if 'selected_gl_code' not in st.session_state:
        st.session_state.selected_gl_code = None

    # Function to trigger policy review
    def trigger_policy_review():

        print(f"Running Policy Review with {st.session_state.selected_category}, {st.session_state.selected_gl_code}")
        result_to_pass = st.session_state.result

        #del st.session_state.approval_response
        result_to_pass.transaction_category = MercuryCategory(st.session_state.selected_category)
        result_to_pass.transaction_category_explanation = 'Manually Reassigned'
        result_to_pass.gl_code = GLCode(st.session_state.selected_gl_code)
        result_to_pass.gl_code_explanation = 'Manually Reassigned'

        print(result_to_pass.model_dump_json())
        approval_response = invoke_policy_chain(result_to_pass)
        print(approval_response)
        if approval_response.policy_flag == 'Allowed':
            st.info(
                f"**Policy Review**: {approval_response.policy_flag}\n\n**Explanation**: {approval_response.policy_explanation}\n\n**Recommendation**: {approval_response.recommendation}"
            )
        elif approval_response.policy_flag == 'Disallowed':
            st.error(
                f"**Policy Review**: {approval_response.policy_flag}\n\n**Explanation**: {approval_response.policy_explanation}\n\n**Recommendation**: {approval_response.recommendation}"
            )
        else:
            st.warning(
                f"**Policy Review**: {approval_response.policy_flag}\n\n**Explanation**: {approval_response.policy_explanation}\n\n**Recommendation**: {approval_response.recommendation}"
            )


    # Review Button Logic
    if st.button("Review"):
        transaction_details = {
            'expense_date': expense_date,
            'expense_time': expense_time,
            'transaction_merchant': merchant,
            'transaction_amount': amount,
            'transaction_notes': notes,
            'transaction_receipt': receipt
        }

        st.session_state.transaction_details = transaction_details
        result = invoke_transaction_chain(transaction_details)
        st.session_state.result = result
        # Trigger initial policy review after "Review" is clicked

# Display Results if Available
if st.session_state.result:
    st.subheader("Categorization Result")

    # Recommended Category Dropdown with on_change callback to trigger policy review
    category_options = [st.session_state.result.transaction_category.value] + \
                       [cat.value for cat in st.session_state.result.alternative_categories]
    st.session_state.selected_category = st.selectbox(
        "Recommended Category",
        options=category_options,
        index=0,
        key='category_select',
    )
    st.info(f"Explanation: {st.session_state.result.transaction_category_explanation} \nConfidence: {st.session_state.result.transaction_category_confidence}")

    # GL Code Dropdown with on_change callback to trigger policy review
    gl_code_options = [st.session_state.result.gl_code.value] + \
                      [gl.value for gl in st.session_state.result.alternative_gl_codes]
    st.session_state.selected_gl_code = st.selectbox(
        "GL Code",
        options=gl_code_options,
        index=0,
        key='gl_code_select',
    )
    st.info(f"Explanation: {st.session_state.result.gl_code_explanation} \nConfidence: {st.session_state.result.gl_code_confidence}")

    #trigger_policy_review()
    print(f"Running Policy Review with {st.session_state.selected_category}, {st.session_state.selected_gl_code}")
    result_to_pass = st.session_state.result

    #del st.session_state.approval_response
    result_to_pass.transaction_category = MercuryCategory(st.session_state.selected_category)
    result_to_pass.transaction_category_explanation = 'Manually Reassigned'
    result_to_pass.gl_code = GLCode(st.session_state.selected_gl_code)
    result_to_pass.gl_code_explanation = 'Manually Reassigned'

    print(result_to_pass.model_dump_json())
    approval_response = invoke_policy_chain(result_to_pass)
    print(approval_response)
    if approval_response.policy_flag == 'Allowed':
        st.info(
            f"**Policy Review**: {approval_response.policy_flag}\n\n**Explanation**: {approval_response.policy_explanation}\n\n**Recommendation**: {approval_response.recommendation}"
        )
    elif approval_response.policy_flag == 'Disallowed':
        st.error(
            f"**Policy Review**: {approval_response.policy_flag}\n\n**Explanation**: {approval_response.policy_explanation}\n\n**Recommendation**: {approval_response.recommendation}"
        )
    else:
        st.warning(
            f"**Policy Review**: {approval_response.policy_flag}\n\n**Explanation**: {approval_response.policy_explanation}\n\n**Recommendation**: {approval_response.recommendation}"
        )

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