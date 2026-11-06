# UnrealLocalization

Export Crowdin translations to an Unreal Engine project with the command-line interface.

The configuration is a JSON file containing the Crowdin project ID, the Unreal project path, and optional language rules:

```json
{
  "project_id": 735873,
  "project_path": "/path/to/UnrealProject/MyProject.uproject",
  "project_export_path": "/path/to/UnrealProject/Localization/MyProject",
  "languages_code_rename": {
    "es-ES": "es",
    "pt-PT": "pt",
    "zh-CN": "zh-Hans",
    "zh-TW": "zh-Hant"
  },
  "languages_code_to_exclude": ["en"]
}
```

See [`mmvs_localization.example.json`](./mmvs_localization.example.json) for an example.

- `project_id` (required): a positive integer identifying the Crowdin project.
- `project_path` (required): a non-empty path to the Unreal `.uproject` file.
- `project_export_path` (required): a non-empty path to the destination folder for exported translations.
- `languages_code_rename` (optional): an object mapping language folder names to their new names. Defaults to `{}` (no renaming).
- `languages_code_to_exclude` (optional): a list of language folder names to remove after renaming. Defaults to `[]` (no exclusions).

Missing required fields, invalid value types, unsafe language folder names, and unknown fields produce a configuration error before authentication or export.

Both paths support **absolute and relative paths**. Relative paths are interpreted relative to the JSON file, not the terminal's working directory or the `.uproject` file. For a JSON stored in the Unreal project's `Config` folder, you can use `"project_path": "../MyProject.uproject"` and `"project_export_path": "../Localization/MyProject"`. The example above uses generic Linux absolute paths; on Windows, use paths such as `"C:/Projects/MyProject/MyProject.uproject"` and `"C:/Projects/MyProject/Localization/MyProject"`. Use `/` or escape backslashes as `\\` in JSON on Windows.

## Crowdin authentication

Install the dependencies:

```shell
python -m pip install -r requirements.txt
```

On the first export, if no token is stored, the tool displays the Crowdin token creation URL and asks you to paste your Personal Access Token. It saves the token in the system credential store and continues the export. Subsequent exports reuse the saved token, including when running with F5.

You can also save or replace the token explicitly:

```shell
python run_mmvs_localization.py auth login
```

The token is entered without being displayed and is not saved in the project configuration or source files. The tool uses the system credential store through Python's `keyring` library; on Linux, a Secret Service or KWallet backend must be available and unlocked. No plaintext-file fallback is used.

Create your token in [Crowdin account settings](https://crowdin.com/settings#api-key) with only the permissions required for exporting translations. This is manual token authentication, not OAuth: no application registration is required. If the token expires or is revoked, replace it using `auth login`. Token entry requires an interactive terminal with hidden input support.

Minimum scope for the current tool: **Translations (`project.translation`) - Read only**. Select only this scope, not **All scopes** or **Read and Write**, and choose an expiration date for your token. Both [Build Project Translation and Download Project Translations](https://support.crowdin.com/developer/api/v2/) require this read-only scope. Extraction and copying into Unreal are local operations and require no additional Crowdin scopes. See [Crowdin scope documentation](https://support.crowdin.com/developer/understanding-scopes/).

Remove the saved token when it is no longer needed:

```shell
python run_mmvs_localization.py auth logout
```

## Run from the command line

On Windows, using PowerShell:

```powershell
py P:\github_repos\other_projects\UnrealLocalization\run_mmvs_localization.py export "M:\MMVS_ProjectFiles_v2\UnrealProject\Config\mmvs_localization.json"
```

On Linux, using Bash:

```bash
python3 /path/to/UnrealLocalization/run_mmvs_localization.py export "/path/to/UnrealProject/Config/mmvs_localization.json"
```

If you run `run_mmvs_localization.py` without arguments, it prompts for the configuration file path. The VS Code **MMVS Localization** F5 launch configuration uses this prompt.

## Tests

```shell
python -m unittest discover -s tests
```