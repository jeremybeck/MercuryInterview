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
    Ensure that policy is followed strictly. 
    
    Reply with the following fields in json only
      - policy_flag: ['Allowed', 'Disallowed', 'More Information Required']
      - policy_explanation: Justification for the policy_flag value
      - sources:  a list of passages from the policy reinforcing the explanation
      - recommendation: Next steps for resolving the transaction

    Context:
    {context}

    Question:
    {question}

    Respond in JSON format:
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