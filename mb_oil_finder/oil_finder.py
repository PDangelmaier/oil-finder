"""
Oil Finder module for Mercedes-Benz vehicles.
Provides functionality to find the appropriate oil based on engine specifications.
"""
from typing import Dict, List, Optional

from .models import EngineData, OilRecommendation, OilSpecification
from .exceptions import NoOilRecommendationError


class OilFinder:
    """Class for finding appropriate oil for Mercedes-Benz engines."""
    
    # MB Approval number to oil specification mapping
    OIL_SPECIFICATIONS = {
        "229.1": OilSpecification(
            mb_approval="229.1",
            viscosity="10W-40",
            type="Semi-synthetic",
            description="Basic specification for gasoline and diesel engines"
        ),
        "229.3": OilSpecification(
            mb_approval="229.3",
            viscosity="5W-40",
            type="Synthetic",
            description="High-performance specification for gasoline and diesel engines"
        ),
        "229.5": OilSpecification(
            mb_approval="229.5",
            viscosity="5W-30",
            type="Synthetic",
            description="Advanced specification for extended drain intervals"
        ),
        "229.51": OilSpecification(
            mb_approval="229.51",
            viscosity="5W-30",
            type="Synthetic",
            description="Low SAPS oil for diesel engines with particulate filters"
        ),
        # Add more specifications as needed
    }
    
    # Engine type to oil specification mapping
    ENGINE_OIL_MAPPING = {
        "OM651": {
            "primary": "229.51",
            "alternatives": ["229.5", "229.3"]
        },
        "M276": {
            "primary": "229.5",
            "alternatives": ["229.3"]
        },
        # Add more engine types as needed
    }
    
    def __init__(self):
        """Initialize the Oil Finder."""
        pass
    
    def find_oil_by_engine(self, engine_data: EngineData) -> OilRecommendation:
        """
        Find the recommended oil for a specific engine.
        
        Args:
            engine_data: Engine data extracted from VIN
            
        Returns:
            OilRecommendation: The recommended oil and alternatives
            
        Raises:
            NoOilRecommendationError: If no oil recommendation is found
        """
        if not engine_data or not engine_data.type:
            raise NoOilRecommendationError("Invalid engine data")
        
        # Look up engine type in our mapping
        mapping = self.ENGINE_OIL_MAPPING.get(engine_data.type)
        if not mapping:
            raise NoOilRecommendationError(f"No oil recommendation for engine type: {engine_data.type}")
        
        # Get primary oil specification
        primary_spec = self.OIL_SPECIFICATIONS.get(mapping["primary"])
        if not primary_spec:
            raise NoOilRecommendationError(f"Primary oil specification not found: {mapping['primary']}")
        
        # Get alternative specifications
        alternative_specs = []
        for alt_code in mapping["alternatives"]:
            alt_spec = self.OIL_SPECIFICATIONS.get(alt_code)
            if alt_spec:
                alternative_specs.append(alt_spec)
        
        # Create and return oil recommendation
        return OilRecommendation(
            primary=primary_spec,
            alternatives=alternative_specs
        )
    
    def find_oil_by_vin(self, vin_data: 'VINData') -> OilRecommendation:
        """
        Find the recommended oil based on VIN data.
        
        Args:
            vin_data: Parsed VIN data
            
        Returns:
            OilRecommendation: The recommended oil and alternatives
            
        Raises:
            NoOilRecommendationError: If no oil recommendation is found
        """
        if not vin_data or not vin_data.engine:
            raise NoOilRecommendationError("VIN data does not contain engine information")
        
        # Use the engine data to find oil recommendations
        return self.find_oil_by_engine(vin_data.engine)

