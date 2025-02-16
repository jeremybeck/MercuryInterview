from langchain.chains import RetrievalQA
from language_models import *
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
from transaction_tags import ApprovalResponse
from vector_db import retriever_db
from langchain_core.prompts import PromptTemplate

policy_parser = PydanticOutputParser(pydantic_object=ApprovalResponse)

qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are an intelligent assistant that retrieves expense policy text to evaluate whether a provided transaction is allowable according to policy.  :
    You need to ensure that policy is followed while still allowing some reasonable flexibility. For example, the policy may not mention snacks or coffee, but does mention a per diem.  As long as those transactions fit within the per diem budget, they should be allowed.
    
    Assume that each transaction is associated with attendance at a larger onsite, and not paying for the onsite itself. To that end, when assigning GL codes, prioritize travel meals over business meals. 
    
    Reply with the following fields in json only
      - policy_flag: ['Allowed', 'Disallowed', 'More Information Required']
      - policy_explanation: Justification for the policy_flag value
      - policy_sources:  a list of passages from the policy reinforcing the explanation
      - policy_gl_code: GLCode = Field(..., description="Recommended General Ledger Code for Transaction based on policy")
      - recommendation: Next steps for resolving the transaction

    Policy Information:
    {context}

    Transaction Details:
    {question}

    Response: 
    """
)

output_fixing_parser = OutputFixingParser.from_llm(
    llm=base_llm,
    parser=policy_parser
)

qa_chain = RetrievalQA.from_chain_type(
    llm=base_llm,
    chain_type="stuff",
    retriever=retriever_db,
    chain_type_kwargs={"prompt": qa_prompt}
)

def policy_chain(input=None, qa_chain=qa_chain, output_fixing_parser=output_fixing_parser):

    answer = qa_chain.invoke(input)
    result = output_fixing_parser.parse(answer.get('result'))

    return result