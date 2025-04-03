"""
Custom exceptions for the Mercedes-Benz VIN Decoder and Oil Finder.
"""


class MBOilFinderError(Exception):
    """Base exception for all MB Oil Finder errors."""
    pass


class VINDecoderError(MBOilFinderError):
    """Base exception for VIN decoder errors."""
    pass


class InvalidVINError(VINDecoderError):
    """Exception raised for invalid VIN format."""
    pass


class UnsupportedVehicleError(VINDecoderError):
    """Exception raised for unsupported vehicle types."""
    pass


class OilFinderError(MBOilFinderError):
    """Base exception for oil finder errors."""
    pass


class NoOilRecommendationError(OilFinderError):
    """Exception raised when no oil recommendation is found."""
    pass


class EngineDataError(MBOilFinderError):
    """Exception raised for engine data errors."""
    pass

