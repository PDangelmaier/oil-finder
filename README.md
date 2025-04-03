# Mercedes-Benz VIN-to-Oil Finder

## Project Overview and Objectives

The Mercedes-Benz VIN-to-Oil Finder is a specialized tool designed to bridge the gap between Vehicle Identification Numbers (VINs) and appropriate oil recommendations for Mercedes-Benz vehicles. This system aims to simplify the process of identifying the correct oil specifications based on a vehicle's unique identifier.

### Key Objectives

- Accurately decode Mercedes-Benz VINs to extract engine and model information
- Match decoded engine types to Mercedes-Benz-approved oil specifications
- Provide climate-specific oil recommendations
- Ensure reliability through comprehensive validation and error handling
- Deliver an easy-to-use interface for both technical and non-technical users

## Technical Architecture

### System Components

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  VIN Decoder    │────▶│  Engine Matcher │────▶│  Oil Finder     │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  VIN Database   │     │ Engine Database │     │  Oil Database   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Core Modules

1. **VIN Decoder (`vin_decoder.py`)**
   - Validates VIN format and checksum
   - Parses VIN to extract manufacturer, model, and engine codes
   - Maps codes to human-readable information

2. **Oil Finder (`oil_finder.py`)**
   - Takes engine information from VIN Decoder
   - Determines appropriate oil specifications (MB-Approval numbers)
   - Handles climate-specific recommendations
   - Provides alternative oil options

3. **Data Models (`models.py`)**
   - Defines structured data classes for VIN information
   - Represents oil recommendations
   - Ensures data consistency across the application

4. **Exception Handling (`exceptions.py`)**
   - Provides custom exceptions for validation errors
   - Handles unsupported VINs or missing specifications
   - Ensures graceful error reporting

### Data Flow

1. User inputs a Mercedes-Benz VIN
2. System validates VIN format and checksum
3. VIN is parsed to extract manufacturer, model, and engine codes
4. Engine code is matched to engine specifications
5. Engine specifications are used to determine oil requirements
6. Oil finder returns primary and alternative recommendations based on engine type and optional climate conditions

## Development Phases

### Phase 1: Research and Data Collection (Completed)
- Compile Mercedes-Benz VIN structure information
- Document engine code mapping
- Collect oil specifications and MB-Approval numbers
- Research climate-specific oil requirements

### Phase 2: Core Implementation (Current)
- Develop VIN validation and parsing
- Implement engine code lookup
- Create oil recommendation logic
- Build basic error handling

### Phase 3: Testing and Validation
- Develop comprehensive test suite
- Validate with known Mercedes-Benz VINs
- Verify oil recommendations against Mercedes-Benz specifications
- Test edge cases and error handling

### Phase 4: User Interface Development
- Create command-line interface
- Develop web API (REST endpoints)
- Implement optional web frontend
- Document API usage

### Phase 5: Deployment and Documentation
- Package for distribution
- Create installation scripts
- Complete user and developer documentation
- Prepare for continuous integration

## Installation and Usage Instructions

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/oil-finder.git
cd oil-finder

# Install required packages
pip install -r requirements.txt
```

### Basic Usage

```python
from mb_oil_finder.vin_decoder import VINDecoder
from mb_oil_finder.oil_finder import OilFinder

# Create instances
decoder = VINDecoder()
finder = OilFinder()

# Example usage with a Mercedes-Benz VIN
vin = "WDD2050421A123456"

try:
    # Decode VIN
    decoded_vin = decoder.decode(vin)
    
    # Get oil recommendation
    recommendation = finder.get_recommendation(decoded_vin)
    
    print(f"Engine: {decoded_vin.engine.description}")
    print(f"Recommended oil: {recommendation['primary']['viscosity']} "
          f"(MB {recommendation['primary']['mb_approval']})")
    
    # Alternative options
    print("\nAlternative options:")
    for alt in recommendation['alternatives']:
        print(f"- {alt['viscosity']} (MB {alt['mb_approval']})")
        
except Exception as e:
    print(f"Error: {e}")
```

### Command-line Usage (Coming Soon)

```bash
# Get oil recommendation from VIN
python -m mb_oil_finder WDD2050421A123456

# Get recommendation with climate information
python -m mb_oil_finder WDD2050421A123456 --climate cold
```

## Testing Strategy

### Unit Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test category
python -m unittest test_oil_finder.TestVINDecoder
```

### Test Coverage

The test suite includes:

1. **VIN Validation Tests**
   - Valid VIN format validation
   - Checksum verification
   - Invalid format detection

2. **VIN Decoding Tests**
   - Manufacturer identification
   - Model series extraction
   - Engine code parsing

3. **Oil Recommendation Tests**
   - Basic engine to oil mapping
   - Climate-specific recommendations
   - Alternative oil options

4. **Integration Tests**
   - Complete flow from VIN to oil recommendation
   - Error handling scenarios
   - Edge cases (rare models, special editions)

## Future Enhancements

### Short-term Roadmap

1. **Data Expansion**
   - Expand engine database to cover all Mercedes-Benz models
   - Add historical models (pre-2000)
   - Include commercial vehicle support

2. **Feature Additions**
   - Oil change interval recommendations
   - Filter recommendations based on VIN
   - Regional specification differences

3. **User Interface Improvements**
   - Web API with Swagger documentation
   - Simple web interface
   - Mobile app for on-the-go lookup

### Long-term Vision

1. **Multi-brand Support**
   - Extend to other German luxury brands
   - Implement universal VIN decoder

2. **Maintenance Module**
   - Full maintenance schedule based on VIN
   - Service interval calculations
   - Parts replacement recommendations

3. **Integration Options**
   - Integration with workshop management systems
   - Dealership service department API
   - Mobile service technician tools

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
