"""
Data models for the Mercedes-Benz VIN Decoder and Oil Finder.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class EngineData:
    """Data model for engine information."""
    code: str  # Engine code from VIN
    type: str  # Engine type/family (e.g., OM651, M276)
    family: str  # General family (Diesel, Gasoline)
    description: str  # Human-readable description
    displacement: float  # Engine displacement in liters
    cylinders: int  # Number of cylinders
    fuel_type: str  # Fuel type (Diesel, Gasoline)


@dataclass
class OilSpecification:
    """Data model for oil specifications."""
    mb_approval: str  # Mercedes-Benz approval number (e.g., 229.5)
    viscosity: str  # Oil viscosity grade (e.g., 5W-30)
    type: str  # Oil type (Synthetic, Semi-synthetic, Mineral)
    description: str  # Human-readable description


@dataclass
class OilRecommendation:
    """Data model for oil recommendations."""
    primary: OilSpecification  # Primary recommended oil
    alternatives: List[OilSpecification]  # Alternative oils


@dataclass
class VINData:
    """Data model for parsed VIN information."""
    vin: str  # Full VIN
    manufacturer: str  # Manufacturer code (e.g., WDD)
    model_series: str  # Model series code (e.g., 205)
    engine_code: str  # Engine code
    model_details: str  # Model details
    model_year: str  # Model year code
    plant_code: str  # Assembly plant code
    serial_number: str  # Serial production number
    engine: Optional[EngineData] = None  # Engine data (if available)

