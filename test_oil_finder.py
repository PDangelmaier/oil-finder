import unittest
from unittest.mock import patch, MagicMock

from mb_oil_finder.vin_decoder import VinDecoder
from mb_oil_finder.oil_finder import OilFinder
from mb_oil_finder.exceptions import InvalidVinError, EngineNotFoundError, OilSpecificationNotFoundError


class TestVinValidator(unittest.TestCase):
    """Test the VIN validation functionality."""

    def setUp(self):
        self.vin_decoder = VinDecoder()
    
    def test_valid_vin(self):
        """Test that a valid Mercedes VIN is accepted."""
        valid_vins = [
            "WDD2050421A123456",  # C-Class
            "WDB9634031L924883",  # Sprinter
            "WDC1569421J123456",  # GLC
        ]
        
        for vin in valid_vins:
            with self.subTest(vin=vin):
                self.assertTrue(self.vin_decoder.validate_vin(vin))
    
    def test_invalid_vin_length(self):
        """Test that VINs with incorrect length are rejected."""
        invalid_vins = [
            "WDD20504",          # Too short
            "WDD2050421A1234567", # Too long
            "",                  # Empty string
        ]
        
        for vin in invalid_vins:
            with self.subTest(vin=vin):
                with self.assertRaises(InvalidVinError):
                    self.vin_decoder.validate_vin(vin)
    
    def test_invalid_vin_characters(self):
        """Test that VINs with invalid characters are rejected."""
        invalid_vins = [
            "WDD2050421A12345Q",  # Q is not allowed in VIN
            "WDD2050421A12345I",  # I is not allowed in VIN
            "WDD2050421A12345O",  # O is not allowed in VIN
            "WDD2050421$123456",  # Special character
        ]
        
        for vin in invalid_vins:
            with self.subTest(vin=vin):
                with self.assertRaises(InvalidVinError):
                    self.vin_decoder.validate_vin(vin)
    
    def test_non_mercedes_vin(self):
        """Test that non-Mercedes VINs are rejected."""
        non_mercedes_vins = [
            "1HGCM82633A123456",  # Honda
            "JH4KA7670NC123456",  # Acura
            "5TFUM5F10DX123456",  # Toyota
        ]
        
        for vin in non_mercedes_vins:
            with self.subTest(vin=vin):
                with self.assertRaises(InvalidVinError):
                    self.vin_decoder.validate_vin(vin)


class TestVinDecoder(unittest.TestCase):
    """Test the VIN decoding functionality."""

    def setUp(self):
        self.vin_decoder = VinDecoder()
    
    def test_decode_valid_vin(self):
        """Test decoding a valid VIN."""
        vin = "WDD2050421A123456"
        result = self.vin_decoder.decode(vin)
        
        self.assertEqual(result["manufacturer"], "Mercedes-Benz")
        self.assertEqual(result["model_series"], "205")
        self.assertEqual(result["engine_code"], "42")
        self.assertEqual(result["model_year"], "1")
        self.assertEqual(result["assembly_plant"], "A")
        self.assertEqual(result["serial_number"], "123456")
    
    def test_decode_extracts_engine_code(self):
        """Test that the engine code is correctly extracted from various VINs."""
        test_cases = [
            {"vin": "WDD2050421A123456", "expected_engine_code": "42"},
            {"vin": "WDB9634031L924883", "expected_engine_code": "03"},
            {"vin": "WDC1569421J123456", "expected_engine_code": "42"},
        ]
        
        for case in test_cases:
            with self.subTest(vin=case["vin"]):
                result = self.vin_decoder.decode(case["vin"])
                self.assertEqual(result["engine_code"], case["expected_engine_code"])
    
    def test_decode_invalid_vin_raises_error(self):
        """Test that decoding an invalid VIN raises an error."""
        invalid_vins = [
            "WDD205042",           # Too short
            "WDD2050421A1234567",  # Too long
            "1HGCM82633A123456",   # Non-Mercedes
        ]
        
        for vin in invalid_vins:
            with self.subTest(vin=vin):
                with self.assertRaises(InvalidVinError):
                    self.vin_decoder.decode(vin)
    
    def test_engine_type_lookup(self):
        """Test that the engine type is correctly determined from the engine code."""
        # Mock the internal engine code lookup
        with patch.object(self.vin_decoder, '_get_engine_type') as mock_get_engine:
            mock_get_engine.return_value = {"type": "OM651", "description": "2.1L Diesel"}
            
            result = self.vin_decoder.get_engine_info("42")
            
            self.assertEqual(result["type"], "OM651")
            self.assertEqual(result["description"], "2.1L Diesel")
    
    def test_unknown_engine_code_raises_error(self):
        """Test that an unknown engine code raises an error."""
        with patch.object(self.vin_decoder, '_get_engine_type') as mock_get_engine:
            mock_get_engine.return_value = None
            
            with self.assertRaises(EngineNotFoundError):
                self.vin_decoder.get_engine_info("99")  # Assuming 99 is not a valid engine code


class TestOilFinder(unittest.TestCase):
    """Test the oil finder functionality."""

    def setUp(self):
        self.oil_finder = OilFinder()
    
    def test_find_oil_by_engine_type(self):
        """Test finding oil specification by engine type."""
        engine_info = {"type": "OM651", "description": "2.1L Diesel"}
        
        result = self.oil_finder.find_oil_by_engine_type(engine_info)
        
        self.assertIn("primary", result)
        self.assertIn("mb_approval", result["primary"])
        self.assertIn("viscosity", result["primary"])
        self.assertIn("type", result["primary"])
        
        # Check for specific values (assuming OM651 needs MB 229.5 oil)
        self.assertEqual(result["primary"]["mb_approval"], "229.5")
        self.assertEqual(result["primary"]["viscosity"], "5W-30")
        self.assertEqual(result["primary"]["type"], "Synthetic")
    
    def test_find_oil_with_alternatives(self):
        """Test that alternative oil recommendations are provided."""
        engine_info = {"type": "OM651", "description": "2.1L Diesel"}
        
        result = self.oil_finder.find_oil_by_engine_type(engine_info)
        
        self.assertIn("alternatives", result)
        self.assertIsInstance(result["alternatives"], list)
        self.assertGreater(len(result["alternatives"]), 0)
        
        # Check first alternative
        alt = result["alternatives"][0]
        self.assertIn("mb_approval", alt)
        self.assertIn("viscosity", alt)
        self.assertIn("type", alt)
    
    def test_unknown_engine_type_raises_error(self):
        """Test that an unknown engine type raises an error."""
        engine_info = {"type": "UNKNOWN", "description": "Unknown Engine"}
        
        with self.assertRaises(OilSpecificationNotFoundError):
            self.oil_finder.find_oil_by_engine_type(engine_info)
    
    def test_find_oil_considers_climate(self):
        """Test that climate conditions are considered in oil recommendations."""
        engine_info = {"type": "OM651", "description": "2.1L Diesel"}
        
        # Cold climate test
        cold_result = self.oil_finder.find_oil_by_engine_type(engine_info, climate="cold")
        self.assertEqual(cold_result["primary"]["viscosity"], "0W-30")
        
        # Hot climate test
        hot_result = self.oil_finder.find_oil_by_engine_type(engine_info, climate="hot")
        self.assertEqual(hot_result["primary"]["viscosity"], "5W-40")


class TestIntegrationFlow(unittest.TestCase):
    """Test the complete flow from VIN to oil recommendation."""

    def setUp(self):
        self.vin_decoder = VinDecoder()
        self.oil_finder = OilFinder()
    
    def test_complete_flow_valid_vin(self):
        """Test the complete flow from VIN to oil recommendation for a valid VIN."""
        vin = "WDD2050421A123456"
        
        # Step 1: Validate VIN
        self.assertTrue(self.vin_decoder.validate_vin(vin))
        
        # Step 2: Decode VIN
        decoded_info = self.vin_decoder.decode(vin)
        self.assertEqual(decoded_info["engine_code"], "42")
        
        # Step 3: Get engine information
        engine_info = self.vin_decoder.get_engine_info(decoded_info["engine_code"])
        self.assertEqual(engine_info["type"], "OM651")
        
        # Step 4: Get oil recommendation
        oil_recommendation = self.oil_finder.find_oil_by_engine_type(engine_info)
        self.assertEqual(oil_recommendation["primary"]["mb_approval"], "229.5")
        
        # Test the complete flow in one function call
        result = self.oil_finder.get_oil_recommendation_by_vin(vin)
        
        # Verify the result structure
        self.assertIn("vin", result)
        self.assertEqual(result["vin"], vin)
        
        self.assertIn("engine", result)
        self.assertEqual(result["engine"]["type"], "OM651")
        
        self.assertIn("oil_recommendation", result)
        self.assertEqual(result["oil_recommendation"]["primary"]["mb_approval"], "229.5")
    
    def test_complete_flow_invalid_vin(self):
        """Test the complete flow with an invalid VIN."""
        invalid_vin = "WDD205042"  # Too short
        
        with self.assertRaises(InvalidVinError):
            self.oil_finder.get_oil_recommendation_by_vin(invalid_vin)
    
    def test_complete_flow_unsupported_engine(self):
        """Test the complete flow with a valid VIN but unsupported engine."""
        # Mock a valid VIN but with an unsupported engine code
        valid_vin = "WDD2050991A123456"  # Assuming 99 is not a valid engine code
        
        # Mock the validation to pass
        with patch.object(self.vin_decoder, 'validate_vin', return_value=True):
            # Mock the decoding to return a valid result but with an invalid engine code
            with patch.object(self.vin_decoder, 'decode') as mock_decode:
                mock_decode.return_value = {
                    "manufacturer": "Mercedes-Benz",
                    "model_series": "205",
                    "engine_code": "99",  # Invalid engine code
                    "model_year": "1",
                    "assembly_plant": "A",
                    "serial_number": "123456"
                }
                
                # Test that the flow raises the appropriate error
                with self.assertRaises(EngineNotFoundError):
                    self.oil_finder.get_oil_recommendation_by_vin(valid_vin)


if __name__ == "__main__":
    unittest.main()

