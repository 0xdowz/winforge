class LicensingError(Exception):
    """Base exception for all licensing errors."""
    pass


class InvalidSignatureError(LicensingError):
    """Raised when digital signature verification fails."""
    pass


class LicenseExpiredError(LicensingError):
    """Raised when license expiration date has passed."""
    pass


class MachineMismatchError(LicensingError):
    """Raised when machine fingerprint match score is below threshold."""
    pass


class ClockRollbackError(LicensingError):
    """Raised when system clock rollback is detected."""
    pass


class CorruptedLicenseError(LicensingError):
    """Raised when license JSON structure is invalid."""
    pass
