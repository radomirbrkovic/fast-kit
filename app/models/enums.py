import enum

class UserRole(enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"

class UserTokenType(enum.Enum):
    RESET_PASSWORD = "reset_password"
    EMAIL_VERIFICATION = "email_verification"