from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from transaction_tags import *
from language_models import *

parsing_template = '''
You are provided with a transaction in a business spend management product.  Assign an expense category describing the transaction, as well as a General Ledger (GL) code.  

Use all the information provided with the transaction, including the time of day, amount, and vendor, as well as any provided receipt or notes, to rationalize what the right category should be. 

For each output, provide a confidence level (Low, Medium, High) that describes if you have no idea, if it is a reasonable guess, or you are certain of the answer. 

### Formatting Instructions
{format_instructions}

### Transaction
{transaction}


'''

transaction_parser = JsonOutputParser(pydantic_object=Transaction)

parsing_prompt = PromptTemplate(
    template = parsing_template,
    input_variables = ['transaction'],
    partial_variables = {'format_instructions': transaction_parser.get_format_instructions()}
)

transaction_llm = base_llm.with_structured_output(Transaction)

transaction_chain = parsing_prompt | transaction_llm