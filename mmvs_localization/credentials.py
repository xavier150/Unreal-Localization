import keyring


SERVICE_NAME = "UnrealLocalization"
CROWDIN_TOKEN_NAME = "crowdin-api-token"


def get_api_token() -> str | None:
    return keyring.get_password(SERVICE_NAME, CROWDIN_TOKEN_NAME)


def save_api_token(api_token: str) -> None:
    keyring.set_password(SERVICE_NAME, CROWDIN_TOKEN_NAME, api_token)


def delete_api_token() -> bool:
    if get_api_token() is None:
        return False

    keyring.delete_password(SERVICE_NAME, CROWDIN_TOKEN_NAME)
    return True
