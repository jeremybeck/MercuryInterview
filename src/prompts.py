from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from transaction_tags import *
from language_models import *

parsing_template = '''
You are provided with a transaction in a business spend management product. Use the following chain of thought below:

Step 1: Analyze all information provided with the transaction to summarize what you know about it. 
Step 2: Pick the 5 most likely transaction categories for the transaction
Step 3: Revisit the information you know about the Transaction to pick the top transaction category
Step 4: Using all information about the transaction you know so far, pick the 5 most likely GL codes.
Step 5:  Pick 5 Alternative GL codes
Step 6:  Provide Explanations and your confidence for the chosen Category and GL code


### Choose from the following options: 

Transaction Categories:
    "Advertising",
    "Airlines",
    "AlcoholAndBars",
    "BooksAndNewspaper",
    "CarRental",
    "Charity",
    "Clothing",
    "Conferences",
    "Education",
    "Electronics",
    "Entertainment",
    "FacilitiesExpenses",
    "Fees",
    "FoodDelivery",
    "FuelAndGas",
    "Gambling",
    "GovernmentServices",
    "Grocery",
    "GroundTransportation",
    "Insurance",
    "InternetAndTelephone",
    "Legal",
    "Lodging",
    "Medical",
    "Memberships",
    "OfficeSupplies",
    "Other",
    "OtherTravel",
    "Parking",
    "Political",
    "ProfessionalServices",
    "Restaurants",
    "Retail",
    "RideshareAndTaxis",
    "Shipping",
    "Software",
    "Taxes",
    "Utilities",
    "VehicleExpenses"
    
GL Codes:
    "Professional Fees and Services",
    "Travel - Meals",
    "Internal Events - Company",
    "Printing and Shipping",
    "Internal Gifts",
    "Customer Activation - Meals",
    "Advertising - Awareness",
    "Office Meals",
    "Lodging",
    "Advertising - Conversion",
    "Company ERG",
    "Business Meals",
    "Ground Transportation",
    "Sponsorships & Conferences",
    "Other",
    "Team Happy Hour",
    "Business Gifts - External",
    "Travel - Other/Wifi",
    "Customer-facing Mercury Events",
    "Repairs & Maintenance",
    "Computer Supplies",
    "Software",
    "VC Speedy Events",
    "Airfare",
    "Entertainment",
    "Dues & Subscriptions",
    "Lunch Perks",
    "Office Snacks/Coffee Runs",
    "Merch - External",
    "Office Expenses",
    "Disputed Charge",
    "Bank Fees",
    "Accidental Personal Charge",
    "Utilities",
    "Market Research",
    "Merch - Internal",
    "Professional Development",
    "Creative",
    "Building & Utilities Fees",
    "Internal Events - Team",
    "Branding"
    
    
Respond with the following fields and format
### Fields to Determine
    transaction_category: Category of the expense
    alternative_categories:  Base these on your initial 5 choices in the event the chosen category is incorrect. 
    transaction_category_confidence: Confidence of the category assignment
    transaction_category_explanation: 1 Sentence Rationale for Choosing the category
    gl_code: General Ledger code associated with the transaction
    alternative_gl_codes: If the GL code is wrong, these are the most likely right choices. 
    gl code_confidence: Confidence level of the general ledger code
    gl_code_explanation: 1 Sentence Rationale for Choosing the GL code

### Formatting Instructions
{format_instructions}

### Transaction Details Below
{transaction}

Begin Chain of Thought!
Step 1:
'''

transaction_parser = JsonOutputParser(pydantic_object=Transaction)

parsing_prompt = PromptTemplate(
    template = parsing_template,
    input_variables = ['transaction'],
    partial_variables = {'format_instructions': transaction_parser.get_format_instructions()}
)

transaction_llm = base_llm.with_structured_output(Transaction)

transaction_chain = parsing_prompt | transaction_llm