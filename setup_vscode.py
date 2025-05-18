import pathlib
import json


# Define base directory
BASE_DIR = pathlib.Path(__file__).parent


def create_settings_json():
    # Define settings dict
    od = {}

    # Editor and coding settings
    od["editor.rulers"] = [
        120,
    ]
    od["editor.defaultFormatter"] = "ms-python.black-formatter"
    od["python.languageServer"] = "Pylance"
    od["python.analysis.diagnosticSeverityOverrides"] = {"reportShadowedImports": "none"}

    # Linter settings
    od["black-formatter.args"] = ["--line-length", "120"]
    od["flake8.args"] = ["--max-line-length", "120", "--per-file-ignores", "__init__.py:F401,F403"]

    # Create .vscode folder
    vsc_dir = BASE_DIR / ".vscode"
    vsc_dir.mkdir(exist_ok=True)

    # Write file
    vsc_file = vsc_dir / "settings.json"
    with open(vsc_file, "w") as fp:
        json.dump(od, fp, indent=4)
        fp.write("\n")


def create_extensions_json():
    # Define settings dict
    od = dict()

    # Recommended VSCode extensions
    od["recommendations"] = [
        "ms-python.python",  # Python support
        "ms-python.debugpy",  # Python debugger
        "ms-python.black-formatter",  # Code formatter
        "ms-python.flake8",  # Code style formatter
        "ms-python.vscode-pylance",  # Language server
    ]

    # Create .vscode folder
    vsc_dir = BASE_DIR / ".vscode"
    vsc_dir.mkdir(exist_ok=True)

    # Write file
    vsc_file = vsc_dir / "extensions.json"
    with open(vsc_file, "w") as fp:
        json.dump(od, fp, indent=4)
        fp.write("\n")


def create_launch_json():
    # Define settings dict
    od = dict()

    # VScode specific settings
    od["version"] = "0.2.0"

    # Debug configurations
    od["configurations"] = [
        # Debug current file
        {
            "name": "python: current file",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
        },
    ]

    # Create .vscode folder
    vsc_dir = BASE_DIR / ".vscode"
    vsc_dir.mkdir(exist_ok=True)

    # Write file
    vsc_file = vsc_dir / "launch.json"
    with open(vsc_file, "w") as fp:
        json.dump(od, fp, indent=4)
        fp.write("\n")


# Run
create_extensions_json()
create_settings_json()
create_launch_json()
