import argparse
import getpass
import warnings
from pathlib import Path

import keyring.errors

from mmvs_localization import credentials
from mmvs_localization import main
from mmvs_localization.config_loader import load_project_config


def prompt_api_token(parser: argparse.ArgumentParser) -> str:
    print("Create a Crowdin Personal Access Token at https://crowdin.com/settings#api-key")
    print("Select only Translations (project.translation) with Read only access.")
    print("Do not select All scopes or Read and Write. Choose an expiration date for your token.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            api_token = getpass.getpass("Paste your Crowdin API token (hidden): ").strip()
    except (EOFError, getpass.GetPassWarning):
        parser.error("Token entry requires a terminal that supports hidden input. Run 'auth login' in a terminal.")
    if not api_token:
        parser.error("The Crowdin API token cannot be empty.")
    credentials.save_api_token(api_token)
    print("Crowdin API token saved in the system credential store.")
    return api_token


def main_cli():
    parser = argparse.ArgumentParser(description="Export Crowdin translations to an Unreal Engine project.")
    subparsers = parser.add_subparsers(dest="command")
    export_parser = subparsers.add_parser("export", help="Export translations using a JSON configuration file.")
    export_parser.add_argument("config", type=Path, help="Path to the JSON configuration file.")
    auth_parser = subparsers.add_parser("auth", help="Manage the Crowdin API token.")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_action", required=True)
    auth_subparsers.add_parser("login", help="Store a Crowdin API token in the system credential store.")
    auth_subparsers.add_parser("logout", help="Remove the stored Crowdin API token.")

    args = parser.parse_args()

    if args.command == "auth":
        try:
            if args.auth_action == "login":
                prompt_api_token(parser)
            elif credentials.delete_api_token():
                print("Crowdin API token removed from the system credential store.")
            else:
                print("No Crowdin API token was stored.")
        except keyring.errors.KeyringError as error:
            parser.error(f"Could not access the system credential store: {error}")
        return

    if args.command is None:
        config_path = input("Configuration file path: ").strip().strip('"')
        if not config_path:
            parser.error("A configuration file path is required.")
        config_path = Path(config_path).expanduser()
    else:
        config_path = args.config.expanduser()

    try:
        project_config = load_project_config(config_path)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    try:
        api_token = credentials.get_api_token()
        if not api_token:
            print("No Crowdin API token found.")
            api_token = prompt_api_token(parser)
    except keyring.errors.KeyringError as error:
        parser.error(f"Could not access the system credential store: {error}")

    main.main(project_config, api_token)


if __name__ == "__main__":
    main_cli()
