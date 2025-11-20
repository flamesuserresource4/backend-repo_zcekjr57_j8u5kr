"""
Database Schemas for Farmers Management System

Each Pydantic model below maps to a MongoDB collection with the lowercased
class name. Example: Seed -> "seed" collection.

These schemas are used for validation and also power the built-in database viewer.
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Core farmer content types

class Seed(BaseModel):
    name: str = Field(..., description="Seed name")
    crop: str = Field(..., description="Crop type, e.g., Wheat, Paddy")
    variety: Optional[str] = Field(None, description="Variety or hybrid name")
    company: Optional[str] = Field(None, description="Brand or supplier")
    season: Optional[str] = Field(None, description="Sowing season, e.g., Kharif/Rabi/Zaid")
    days_to_maturity: Optional[int] = Field(None, ge=1, description="Approx days to harvest")
    recommended_states: Optional[List[str]] = Field(None, description="States where recommended")
    notes: Optional[str] = Field(None, description="Farming notes or instructions")
    language: Optional[str] = Field(None, description="Language code, e.g., hi, mr, te")
    state: Optional[str] = Field(None, description="State this content is tailored for")

class Instrument(BaseModel):
    name: str = Field(..., description="Equipment name")
    category: Optional[str] = Field(None, description="Category, e.g., Tractor, Sprayer")
    description: Optional[str] = Field(None, description="What it does and how to use")
    price: Optional[float] = Field(None, ge=0, description="Approx price in INR")
    vendor: Optional[str] = Field(None, description="Brand or supplier")
    language: Optional[str] = Field(None, description="Language code, e.g., hi, mr, te")
    state: Optional[str] = Field(None, description="State this content is tailored for")

class Plant(BaseModel):
    name: str = Field(..., description="Plant/Crop name")
    climate: Optional[str] = Field(None, description="Climate requirements")
    soil: Optional[str] = Field(None, description="Soil requirements")
    irrigation: Optional[str] = Field(None, description="Irrigation schedule")
    fertilizer: Optional[str] = Field(None, description="Fertilizer guidance")
    pest_management: Optional[str] = Field(None, description="Pest/Disease management tips")
    language: Optional[str] = Field(None, description="Language code, e.g., hi, mr, te")
    state: Optional[str] = Field(None, description="State this content is tailored for")

class Subsidy(BaseModel):
    title: str = Field(..., description="Scheme title")
    department: Optional[str] = Field(None, description="Govt department")
    description: Optional[str] = Field(None, description="Scheme details in simple words")
    eligibility: Optional[str] = Field(None, description="Who can apply")
    benefits: Optional[str] = Field(None, description="What you get")
    how_to_apply: Optional[str] = Field(None, description="Application steps / portal")
    state: Optional[str] = Field(None, description="State (if state-level scheme)")
    language: Optional[str] = Field(None, description="Language code, e.g., hi, mr, te")

# Example generic user schema kept for reference (not used by UI)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

