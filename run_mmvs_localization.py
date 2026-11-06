import argparse
from pathlib import Path

from mmvs_localization import main
from mmvs_localization import config


def main_cli():
    parser = argparse.ArgumentParser(description="Export Crowdin translations to an Unreal Engine project.")
    subparsers = parser.add_subparsers(dest="command")
    export_parser = subparsers.add_parser("export", help="Export translations using a JSON configuration file.")
    export_parser.add_argument("config", type=Path, help="Path to the JSON configuration file.")

    args = parser.parse_args()
    if args.command is None:
        config_path = input("Configuration file path: ").strip().strip('"')
        if not config_path:
            parser.error("A configuration file path is required.")
        config_path = Path(config_path).expanduser()
    else:
        config_path = args.config.expanduser()

    try:
        config.load_project_id(config_path)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    main.main()


if __name__ == "__main__":
    main_cli()
