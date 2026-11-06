# UnrealLocalization

Export Crowdin translations to an Unreal Engine project with the command-line interface.

The configuration is a JSON file containing the Crowdin project ID:

```json
{
  "project_id": 735873
}
```

See [`mmvs_localization.example.json`](./mmvs_localization.example.json) for an example.

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