"""
Handles the box client object creation
orchestrates the authentication process
"""

from boxsdk import Client, JWTAuth, CCGAuth
from utils.box_oauth import oauth_from_previous
from utils.config import AppConfig
from utils.oauth_callback import callback_handle_request, open_browser


def get_client(config: AppConfig) -> Client:
    """Returns a boxsdk Client object"""
    oauth = oauth_from_previous()

    # do we need to authorize the app?
    if not oauth.access_token:
        auth_url, csrf_token = oauth.get_authorization_url(config.redirect_uri)
        open_browser(auth_url)
        callback_handle_request(config, csrf_token)

    oauth = oauth_from_previous()

    if not oauth.access_token:
        raise RuntimeError("Unable to authenticate")

    oauth.refresh(oauth.access_token)

    return Client(oauth)


def get_jwt_client(config: AppConfig, as_user_id: str = None) -> Client:
    """Returns a boxsdk Client object"""

    auth = JWTAuth.from_settings_file(config.jwt_config_path)

    client = Client(auth)

    if as_user_id:
        as_user = client.user(as_user_id)
        client.as_user(as_user)

    return client


def get_ccg_enterprise_client(config: AppConfig, as_user_id: str = None) -> Client:
    """Returns a boxsdk Client object"""

    auth = CCGAuth(
        client_id=config.client_id,
        client_secret=config.client_secret,
        enterprise_id=config.enterprise_id,
    )

    client = Client(auth)

    if as_user_id:
        as_user = client.user(as_user_id)
        client.as_user(as_user)

    return client


def get_ccg_user_client(config: AppConfig, as_user_id: str = None) -> Client:
    """Returns a boxsdk Client object"""

    auth = CCGAuth(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user=config.ccg_user_id,
    )

    client = Client(auth)

    if as_user_id:
        as_user = client.user(as_user_id)
        client.as_user(as_user)

    return client
