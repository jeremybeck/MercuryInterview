from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Literal
from enum import Enum

class GLCode(Enum):
    # Advertising & Marketing
    ADVERTISING_AWARENESS = "Advertising - Awareness"
    ADVERTISING_CONVERSION = "Advertising - Conversion"
    BRANDING = "Branding"
    CREATIVE = "Creative"
    MARKET_RESEARCH = "Market Research"

    # Professional Services & Fees
    PROFESSIONAL_FEES_AND_SERVICES = "Professional Fees and Services"
    PROFESSIONAL_DEVELOPMENT = "Professional Development"
    SPONSORSHIPS_CONFERENCES = "Sponsorships & Conferences"

    # Travel & Lodging
    AIRFARE = "Airfare"
    GROUND_TRANSPORTATION = "Ground Transportation"
    LODGING = "Lodging"
    TRAVEL_MEALS = "Travel - Meals"
    TRAVEL_OTHER_WIFI = "Travel - Other/Wifi"

    # Meals & Entertainment
    BUSINESS_MEALS = "Business Meals"
    CUSTOMER_ACTIVATION_MEALS = "Customer Activation - Meals"
    OFFICE_MEALS = "Office Meals"
    TEAM_HAPPY_HOUR = "Team Happy Hour"
    INTERNAL_EVENTS_COMPANY = "Internal Events - Company"
    INTERNAL_EVENTS_TEAM = "Internal Events - Team"
    ENTERTAINMENT = "Entertainment"

    # Gifts & Merch
    INTERNAL_GIFTS = "Internal Gifts"
    BUSINESS_GIFTS_EXTERNAL = "Business Gifts - External"
    MERCH_EXTERNAL = "Merch - External"
    MERCH_INTERNAL = "Merch - Internal"

    # Office & Utilities
    OFFICE_EXPENSES = "Office Expenses"
    OFFICE_SNACKS_COFFEE_RUNS = "Office Snacks/Coffee Runs"
    COMPUTER_SUPPLIES = "Computer Supplies"
    SOFTWARE = "Software"
    PRINTING_AND_SHIPPING = "Printing and Shipping"
    UTILITIES = "Utilities"
    BUILDING_UTILITIES_FEES = "Building & Utilities Fees"

    # Events & ERG
    CUSTOMER_FACING_MERCURY_EVENTS = "Customer-facing Mercury Events"
    VC_SPEEDY_EVENTS = "VC Speedy Events"
    COMPANY_ERG = "Company ERG"

    # Financial & Fees
    BANK_FEES = "Bank Fees"
    DISPUTED_CHARGE = "Disputed Charge"
    ACCIDENTAL_PERSONAL_CHARGE = "Accidental Personal Charge"

    # Miscellaneous & Perks
    LUNCH_PERKS = "Lunch Perks"
    REPAIRS_MAINTENANCE = "Repairs & Maintenance"
    DUES_SUBSCRIPTIONS = "Dues & Subscriptions"
    OTHER = "Other"


class MercuryCategory(Enum):
    # Advertising & Marketing
    ADVERTISING = "Advertising"
    ENTERTAINMENT = "Entertainment"
    GAMBLING = "Gambling"

    # Travel & Transportation
    AIRLINES = "Airlines"
    CAR_RENTAL = "CarRental"
    GROUND_TRANSPORTATION = "GroundTransportation"
    RIDESHARE_AND_TAXIS = "RideshareAndTaxis"
    PARKING = "Parking"
    LODGING = "Lodging"
    OTHER_TRAVEL = "OtherTravel"
    VEHICLE_EXPENSES = "VehicleExpenses"

    # Food & Dining
    ALCOHOL_AND_BARS = "AlcoholAndBars"
    FOOD_DELIVERY = "FoodDelivery"
    GROCERY = "Grocery"
    RESTAURANTS = "Restaurants"

    # Professional & Education
    CONFERENCES = "Conferences"
    EDUCATION = "Education"
    LEGAL = "Legal"
    PROFESSIONAL_SERVICES = "ProfessionalServices"

    # Office & Supplies
    OFFICE_SUPPLIES = "OfficeSupplies"
    SHIPPING = "Shipping"
    SOFTWARE = "Software"
    INTERNET_AND_TELEPHONE = "InternetAndTelephone"
    FACILITIES_EXPENSES = "FacilitiesExpenses"
    UTILITIES = "Utilities"

    # Health & Insurance
    MEDICAL = "Medical"
    INSURANCE = "Insurance"

    # Memberships & Fees
    MEMBERSHIPS = "Memberships"
    FEES = "Fees"
    TAXES = "Taxes"

    # Retail & Shopping
    BOOKS_AND_NEWSPAPER = "BooksAndNewspaper"
    CLOTHING = "Clothing"
    ELECTRONICS = "Electronics"
    RETAIL = "Retail"

    # Charity & Political
    CHARITY = "Charity"
    POLITICAL = "Political"

    # Miscellaneous
    FUEL_AND_GAS = "FuelAndGas"
    OTHER = "Other"


class Transaction(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    transaction_merchant: str = Field(..., description="Name of the merchant for the transaction")
    transaction_notes: Optional[str] = Field(None, description="Additional notes about the transaction")
    transaction_receipt: Optional[str] = Field(None, description="URL to the transaction receipt")
    transaction_category: MercuryCategory = Field(..., description="Category of the expense")
    alternative_categories: list[MercuryCategory] = Field(..., description='Top 5 alternative categories for transaction_category')
    transaction_category_confidence: float = Field(..., description="Confidence of the category assignment")
    transaction_category_explanation: str = Field(..., description="1 Sentence Rationale for Choosing the category")
    gl_code: GLCode = Field(..., description="General Ledger codes associated with the transaction")
    alternative_gl_codes: list[GLCode] = Field(..., description='5 alternative likely General Ledger codes associated with the transaction')
    gl_code_confidence: float = Field(..., description="Confidence level of the general ledger code")
    gl_code_explanation: str = Field(..., description="1 Sentence Rationale for Choosing the GL code")
    policy_notes: Optional[str] = Field(None, description="Notes related to policy or approval status")


class ApprovalResponse(BaseModel):
    policy_flag: Literal['Allowed', 'Disallowed', 'More Information Required'] = Field(..., description="Indicates the policy status of the transaction.")
    policy_explanation: str = Field(..., description="Relevant information from the policy documents justifying the policy_flag value.")
    polcy_sources: list[str] = Field(...,description="Sources related to the policy documents")
    recommendation: str = Field(..., description="Recommendation containing next steps for additional information, or updating categories/GL codes for the transaction.")