from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from enum import Enum

class GLCode(Enum):
    PROFESSIONAL_FEES_AND_SERVICES = "Professional Fees and Services"
    TRAVEL_MEALS = "Travel - Meals"
    INTERNAL_EVENTS_COMPANY = "Internal Events - Company"
    PRINTING_AND_SHIPPING = "Printing and Shipping"
    INTERNAL_GIFTS = "Internal Gifts"
    CUSTOMER_ACTIVATION_MEALS = "Customer Activation - Meals"
    ADVERTISING_AWARENESS = "Advertising - Awareness"
    OFFICE_MEALS = "Office Meals"
    LODGING = "Lodging"
    ADVERTISING_CONVERSION = "Advertising - Conversion"
    COMPANY_ERG = "Company ERG"
    BUSINESS_MEALS = "Business Meals"
    GROUND_TRANSPORTATION = "Ground Transportation"
    SPONSORSHIPS_CONFERENCES = "Sponsorships & Conferences"
    OTHER = "Other"
    TEAM_HAPPY_HOUR = "Team Happy Hour"
    BUSINESS_GIFTS_EXTERNAL = "Business Gifts - External"
    TRAVEL_OTHER_WIFI = "Travel - Other/Wifi"
    CUSTOMER_FACING_MERCURY_EVENTS = "Customer-facing Mercury Events"
    REPAIRS_MAINTENANCE = "Repairs & Maintenance"
    COMPUTER_SUPPLIES = "Computer Supplies"
    SOFTWARE = "Software"
    VC_SPEEDY_EVENTS = "VC Speedy Events"
    AIRFARE = "Airfare"
    ENTERTAINMENT = "Entertainment"
    DUES_SUBSCRIPTIONS = "Dues & Subscriptions"
    LUNCH_PERKS = "Lunch Perks"
    OFFICE_SNACKS_COFFEE_RUNS = "Office Snacks/Coffee Runs"
    MERCH_EXTERNAL = "Merch - External"
    OFFICE_EXPENSES = "Office Expenses"
    DISPUTED_CHARGE = "Disputed Charge"
    BANK_FEES = "Bank Fees"
    ACCIDENTAL_PERSONAL_CHARGE = "Accidental Personal Charge"
    UTILITIES = "Utilities"
    MARKET_RESEARCH = "Market Research"
    MERCH_INTERNAL = "Merch - Internal"
    PROFESSIONAL_DEVELOPMENT = "Professional Development"
    CREATIVE = "Creative"
    BUILDING_UTILITIES_FEES = "Building & Utilities Fees"
    INTERNAL_EVENTS_TEAM = "Internal Events - Team"
    BRANDING = "Branding"

class MercuryCategory(Enum):
    ADVERTISING = "Advertising"
    AIRLINES = "Airlines"
    ALCOHOL_AND_BARS = "AlcoholAndBars"
    BOOKS_AND_NEWSPAPER = "BooksAndNewspaper"
    CAR_RENTAL = "CarRental"
    CHARITY = "Charity"
    CLOTHING = "Clothing"
    CONFERENCES = "Conferences"
    EDUCATION = "Education"
    ELECTRONICS = "Electronics"
    ENTERTAINMENT = "Entertainment"
    FACILITIES_EXPENSES = "FacilitiesExpenses"
    FEES = "Fees"
    FOOD_DELIVERY = "FoodDelivery"
    FUEL_AND_GAS = "FuelAndGas"
    GAMBLING = "Gambling"
    GOVERNMENT_SERVICES = "GovernmentServices"
    GROCERY = "Grocery"
    GROUND_TRANSPORTATION = "GroundTransportation"
    INSURANCE = "Insurance"
    INTERNET_AND_TELEPHONE = "InternetAndTelephone"
    LEGAL = "Legal"
    LODGING = "Lodging"
    MEDICAL = "Medical"
    MEMBERSHIPS = "Memberships"
    OFFICE_SUPPLIES = "OfficeSupplies"
    OTHER = "Other"
    OTHER_TRAVEL = "OtherTravel"
    PARKING = "Parking"
    POLITICAL = "Political"
    PROFESSIONAL_SERVICES = "ProfessionalServices"
    RESTAURANTS = "Restaurants"
    RETAIL = "Retail"
    RIDESHARE_AND_TAXIS = "RideshareAndTaxis"
    SHIPPING = "Shipping"
    SOFTWARE = "Software"
    TAXES = "Taxes"
    UTILITIES = "Utilities"
    VEHICLE_EXPENSES = "VehicleExpenses"


class Transaction(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    transaction_merchant: str = Field(..., description="Name of the merchant for the transaction")
    transaction_notes: Optional[str] = Field(None, description="Additional notes about the transaction")
    transaction_receipt: Optional[str] = Field(None, description="URL to the transaction receipt")
    transaction_category: MercuryCategory = Field(..., description="Category of the expense")
    alternative_categories: list[MercuryCategory] = Field(..., description='Alternative possible categories')
    transaction_category_confidence: float = Field(..., description="Confidence of the category assignment")
    transaction_category_explanation: str = Field(..., description="1 Sentence Rationale for Choosing the category")
    gl_code: GLCode = Field(..., description="General Ledger codes associated with the transaction")
    alternative_gl_codes: list[GLCode] = Field(..., description='Alternative General Ledger codes associated with the transaction')
    gl_code_confidence: float = Field(..., description="Confidence level of the general ledger code")
    gl_code_explanation: str = Field(..., description="1 Sentence Rationale for Choosing the GL code")
    policy_notes: Optional[str] = Field(None, description="Notes related to policy or approval status")