"""
VIN Decoder module for Mercedes-Benz vehicles.
Provides functionality to parse and validate VINs, and extract engine information.
"""
from typing import Dict, Optional, Tuple

from .exceptions import InvalidVINError, UnsupportedVehicleError
from .models import VINData, EngineData


class VINDecoder:
    """Class for parsing and validating Mercedes-Benz Vehicle Identification Numbers (VIN)."""
    
    # Manufacturer codes for Mercedes-Benz
    MB_MANUFACTURER_CODES = {"WDD", "WDB", "WDC", "WMX", "4JG"}
    
    # VIN position mapping
    VIN_STRUCTURE = {
        "manufacturer": (0, 3),    # Positions 1-3
        "model_series": (3, 6),    # Positions 4-6
        "engine_code": (6, 8),     # Positions 7-8
        "model_details": (8, 9),   # Position 9
        "model_year": (9, 10),     # Position 10
        "plant_code": (10, 11),    # Position 11
        "serial_number": (11, 17)  # Positions 12-17
    }
    
    # Engine code mapping (simplified example)
    ENGINE_CODES = {
        "42": EngineData(
            code="42",
            type="OM651",
            family="Diesel",
            description="2.1L 4-cylinder diesel engine",
            displacement=2.1,
            cylinders=4,
            fuel_type="Diesel"
        ),
        "64": EngineData(
            code="64",
            type="M276",
            family="Gasoline",
            description="3.5L V6 gasoline engine",
            displacement=3.5,
            cylinders=6,
            fuel_type="Gasoline"
        ),
        # Add more engine codes as needed
    }
    
    def __init__(self):
        """Initialize the VIN decoder."""
        pass
    
    def validate_vin(self, vin: str) -> bool:
        """
        Validate a Mercedes-Benz VIN.
        
        Args:
            vin: A 17-character Vehicle Identification Number
            
        Returns:
            bool: True if the VIN is valid, False otherwise
            
        Raises:
            InvalidVINError: If the VIN format is invalid
        """
        # Check basic VIN format
        if not vin or not isinstance(vin, str):
            raise InvalidVINError("VIN must be a non-empty string")
        
        # Check length
        if len(vin) != 17:
            raise InvalidVINError("VIN must be 17 characters long")
        
        # Check for valid characters (no I, O, Q)
        if any(c in "IOQ" for c in vin):
            raise InvalidVINError("VIN contains invalid characters: I, O, or Q are not allowed")
        
        # Check if it's a Mercedes-Benz VIN
        manufacturer_code = vin[:3]
        if manufacturer_code not in self.MB_MANUFACTURER_CODES:
            raise UnsupportedVehicleError(f"Not a recognized Mercedes-Benz VIN: {manufacturer_code}")
        
        # A more complete implementation would include checksum validation
        # but we'll simplify for this example
        
        return True
    
    def decode_vin(self, vin: str) -> VINData:
        """
        Decode a Mercedes-Benz VIN into its components.
        
        Args:
            vin: A 17-character Vehicle Identification Number
            
        Returns:
            VINData: Parsed VIN data
            
        Raises:
            InvalidVINError: If VIN validation fails
        """
        # Validate the VIN first
        self.validate_vin(vin)
        
        # Extract components based on position
        components = {}
        for name, (start, end) in self.VIN_STRUCTURE.items():
            components[name] = vin[start:end]
        
        # Look up engine data
        engine_data = self._get_engine_data(components["engine_code"])
        
        # Create and return VIN data object
        return VINData(
            vin=vin,
            manufacturer=components["manufacturer"],
            model_series=components["model_series"],
            engine_code=components["engine_code"],
            model_details=components["model_details"],
            model_year=components["model_year"],
            plant_code=components["plant_code"],
            serial_number=components["serial_number"],
            engine=engine_data
        )
    
    def _get_engine_data(self, engine_code: str) -> Optional[EngineData]:
        """
        Get engine data based on the engine code.
        
        Args:
            engine_code: The engine code extracted from the VIN
            
        Returns:
            Optional[EngineData]: Engine data if found, None otherwise
        """
        return self.ENGINE_CODES.get(engine_code)

