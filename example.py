#!/usr/bin/env python3
"""
Example script demonstrating usage of Mercedes-Benz VIN decoder and oil finder.
This script provides practical examples of:
1. Basic VIN decoding and oil recommendations
2. Error handling for invalid VINs
3. Oil recommendations for different climate conditions
4. Working with real Mercedes-Benz VIN patterns
"""

import sys
from mb_oil_finder.vin_decoder import VINDecoder
from mb_oil_finder.oil_finder import OilFinder
from mb_oil_finder.exceptions import InvalidVINError, UnsupportedModelError, OilSpecificationNotFoundError


def basic_usage_example():
    """Demonstrates basic usage of the VIN decoder and oil finder."""
    print("\n=== Basic Usage Example ===")
    
    # Create instances of the VIN decoder and oil finder
    vin_decoder = VINDecoder()
    oil_finder = OilFinder()
    
    # Example Mercedes-Benz VIN (C-Class with diesel engine)
    vin = "WDD2050421A123456"
    
    try:
        # Decode the VIN
        decoded_vin = vin_decoder.decode(vin)
        
        print(f"VIN: {vin}")
        print(f"Manufacturer: {decoded_vin['manufacturer']}")
        print(f"Model series: {decoded_vin['model_series']}")
        print(f"Engine code: {decoded_vin['engine_code']}")
        print(f"Engine type: {decoded_vin['engine_type']}")
        print(f"Model year: {decoded_vin['model_year']}")
        
        # Get oil recommendation
        oil_recommendation = oil_finder.get_recommendation(decoded_vin)
        
        print("\nRecommended Oil:")
        print(f"MB Approval: {oil_recommendation['primary']['mb_approval']}")
        print(f"Viscosity: {oil_recommendation['primary']['viscosity']}")
        print(f"Type: {oil_recommendation['primary']['type']}")
        
        if oil_recommendation.get('alternatives'):
            print("\nAlternative Options:")
            for alt in oil_recommendation['alternatives']:
                print(f"- MB Approval: {alt['mb_approval']}, "
                      f"Viscosity: {alt['viscosity']}, "
                      f"Type: {alt['type']}")
    
    except Exception as e:
        print(f"Error: {e}")


def error_handling_example():
    """Demonstrates error handling for various error scenarios."""
    print("\n=== Error Handling Example ===")
    
    vin_decoder = VINDecoder()
    oil_finder = OilFinder()
    
    # Example 1: Invalid VIN (wrong format)
    invalid_vin = "ABC123"
    try:
        vin_decoder.decode(invalid_vin)
    except InvalidVINError as e:
        print(f"Example 1 - Invalid VIN error: {e}")
    
    # Example 2: Valid format but unsupported model
    unsupported_vin = "WDD9999999Z999999"  # Made-up VIN
    try:
        decoded_vin = vin_decoder.decode(unsupported_vin)
        oil_finder.get_recommendation(decoded_vin)
    except UnsupportedModelError as e:
        print(f"Example 2 - Unsupported model error: {e}")
    
    # Example 3: Missing oil specification
    try:
        # Simulate a scenario where oil specification is not found
        # (This might be an antique vehicle or a very rare model)
        vintage_vin = "WDB1230421A123456"  # Vintage Mercedes
        decoded_vin = vin_decoder.decode(vintage_vin)
        oil_finder.get_recommendation(decoded_vin)
    except OilSpecificationNotFoundError as e:
        print(f"Example 3 - Oil specification error: {e}")


def climate_conditions_example():
    """Demonstrates oil recommendations for different climate conditions."""
    print("\n=== Climate Conditions Example ===")
    
    vin_decoder = VINDecoder()
    oil_finder = OilFinder()
    
    # E-Class example
    vin = "WDB2130701A456789"
    
    try:
        decoded_vin = vin_decoder.decode(vin)
        print(f"Vehicle: {decoded_vin['model_series']} with {decoded_vin['engine_type']} engine")
        
        # Standard conditions (default)
        standard_recommendation = oil_finder.get_recommendation(decoded_vin)
        print("\nStandard Climate Recommendation:")
        print(f"MB Approval: {standard_recommendation['primary']['mb_approval']}")
        print(f"Viscosity: {standard_recommendation['primary']['viscosity']}")
        
        # Hot climate conditions
        hot_recommendation = oil_finder.get_recommendation(
            decoded_vin, 
            climate_conditions={"type": "hot", "min_temp": 25, "max_temp": 45}
        )
        print("\nHot Climate Recommendation:")
        print(f"MB Approval: {hot_recommendation['primary']['mb_approval']}")
        print(f"Viscosity: {hot_recommendation['primary']['viscosity']}")
        
        # Cold climate conditions
        cold_recommendation = oil_finder.get_recommendation(
            decoded_vin, 
            climate_conditions={"type": "cold", "min_temp": -30, "max_temp": 10}
        )
        print("\nCold Climate Recommendation:")
        print(f"MB Approval: {cold_recommendation['primary']['mb_approval']}")
        print(f"Viscosity: {cold_recommendation['primary']['viscosity']}")
        
    except Exception as e:
        print(f"Error: {e}")


def real_vin_examples():
    """Demonstrates the use of real Mercedes-Benz VIN patterns."""
    print("\n=== Real VIN Pattern Examples ===")
    
    vin_decoder = VINDecoder()
    oil_finder = OilFinder()
    
    # List of example VINs representing different Mercedes models
    example_vins = [
        # C-Class with petrol engine
        {"vin": "WDD2050871F123456", "description": "C-Class (W205) with M274 petrol engine"},
        # E-Class with diesel engine
        {"vin": "WDD2130701A456789", "description": "E-Class (W213) with OM654 diesel engine"},
        # S-Class with petrol engine
        {"vin": "WDD2229061A789012", "description": "S-Class (W222) with M256 petrol engine"},
        # GLC SUV with hybrid engine
        {"vin": "WDC2539541F345678", "description": "GLC-Class (X253) with hybrid powertrain"}
    ]
    
    for example in example_vins:
        print(f"\nProcessing: {example['description']}")
        print(f"VIN: {example['vin']}")
        
        try:
            decoded_vin = vin_decoder.decode(example['vin'])
            
            print(f"Engine code: {decoded_vin['engine_code']}")
            print(f"Engine type: {decoded_vin['engine_type']}")
            
            oil_recommendation = oil_finder.get_recommendation(decoded_vin)
            print(f"Recommended oil: {oil_recommendation['primary']['viscosity']} "
                  f"(MB {oil_recommendation['primary']['mb_approval']})")
            
        except Exception as e:
            print(f"Error processing VIN: {e}")


def main():
    """Main function that runs all examples."""
    print("Mercedes-Benz VIN Decoder and Oil Finder Examples")
    print("=" * 50)
    
    try:
        basic_usage_example()
        error_handling_example()
        climate_conditions_example()
        real_vin_examples()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

