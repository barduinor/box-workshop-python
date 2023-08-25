""" Application configurations """
import os
from dotenv import load_dotenv


class AppConfig:
    """application configurations"""

    def __init__(self) -> None:
        load_dotenv()
        # Common configurations
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")

        # OAuth2 configurations
        self.redirect_uri = os.getenv("REDIRECT_URI")
        self.callback_hostname = os.getenv("CALLBACK_HOSTNAME")
        self.callback_port = int(os.getenv("CALLBACK_PORT", 5000))

        # CCG configurations
        self.enterprise_id = os.getenv("ENTERPRISE_ID")
        self.ccg_user_id = os.getenv("CCG_USER_ID")

        # JWT configurations
        self.jwt_config_path = os.getenv("JWT_CONFIG_PATH")

    def __repr__(self) -> str:
        return f"AppConfig({self.__dict__})"
