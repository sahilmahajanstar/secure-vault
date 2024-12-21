import re
from rest_framework import status
from common.error.validation_error import ValidationError, ValidationErrorCodes


class UserValidator:
    PATTERNS = {
        "lowercase": r"[a-z]",
        "uppercase": r"[A-Z]",
        "digit": r"\d",
        "special_char": r'[!@#$%^&*(),.?":{}|<>]',
        "min_length": 8,
        "max_length": 128,
    }

    # Strength levels
    WEAK = r"^[a-zA-Z0-9]{8,}$"  # At least 8 alphanumeric chars
    MEDIUM = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"  # Lower, upper, digit
    STRONG = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'  # All types

    @staticmethod
    def validate_email(email: str) -> bool:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, email))

    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        # Allows formats like: +1234567890, 1234567890, +1-234-567-890
        phone_pattern = r"^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
        # Remove any non-digit characters except + for validation
        cleaned_number = "".join(
            char for char in phone_number if char.isdigit() or char == "+"
        )
        return bool(re.match(phone_pattern, cleaned_number))

    @staticmethod
    def validate_username(username: str) -> bool:
        # Alphanumeric, underscore, dot, 3-30 characters
        username_pattern = r"^[a-zA-Z0-9._]{3,30}$"
        return bool(re.match(username_pattern, username))

    @staticmethod
    def validate_name(name: str) -> bool:
        name_pattern = r"^[a-zA-Z\s\-\']{2,50}$"
        return bool(re.match(name_pattern, name))

    @classmethod
    def validate_firstname(cls, firstname: str) -> bool:
        return cls.validate_name(firstname)

    @classmethod
    def validate_lastname(cls, lastname: str) -> bool:
        return cls.validate_name(lastname)

    @classmethod
    def validate_country_code(cls, country_code: str) -> bool:
        return country_code in ["+91"]

    @classmethod
    def validate_password(cls, password: str) -> dict:
        """
        Validate password and return detailed strength info
        """
        checks = {
            "length": len(password) >= cls.PATTERNS["min_length"],
            "lowercase": bool(re.search(cls.PATTERNS["lowercase"], password)),
            "uppercase": bool(re.search(cls.PATTERNS["uppercase"], password)),
            "digit": bool(re.search(cls.PATTERNS["digit"], password)),
            "special_char": bool(re.search(cls.PATTERNS["special_char"], password)),
        }

        # Determine strength
        if re.match(cls.STRONG, password):
            strength = "strong"
        elif re.match(cls.MEDIUM, password):
            strength = "medium"
        elif re.match(cls.WEAK, password):
            strength = "weak"
        else:
            strength = "invalid"

        return {"valid": all(checks.values()), "strength": strength, "checks": checks}

    @classmethod
    def validate(cls, data: dict) -> ValidationError:
        validation = ValidationError(
            "Invalid data",
            ValidationErrorCodes.INVALID_DATA,
            status.HTTP_400_BAD_REQUEST,
        )
        if not cls.validate_email(data["email"]):
            validation.add_error("Invalid email", "email")
        # if not cls.validate_phone_number(data['phone_number']):
        #     validation.add_error('Invalid phone number', 'phone_number')
        if not cls.validate_username(data["username"]):
            validation.add_error("Invalid username", "username")
        if not cls.validate_name(data["first_name"]):
            validation.add_error("Invalid first name", "first_name")
        if not cls.validate_name(data["last_name"]):
            validation.add_error("Invalid last name", "last_name")
        # if not cls.validate_country_code(data['country_code']):
        #     validation.add_error('Invalid country code', 'country_code')
        password_validation = cls.validate_password(data["password"])
        if (
            not password_validation.get("valid")
            or password_validation.get("strength") == "weak"
        ):
            validation.add_error("passoward is weak", "password")
        return validation
