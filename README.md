# UnrealLocalization

Export Crowdin translations to an Unreal Engine project with the command-line interface.

The configuration is a JSON file containing the Crowdin project ID:

```json
{
  "project_id": 735873
}
```

See [`mmvs_localization.example.json`](./mmvs_localization.example.json) for an example.

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