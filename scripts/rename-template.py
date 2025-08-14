
import argparse
import glob
import os

paths_to_replace = [
    "src/**/*.py",
    "tests/**/*.py",
    "Dockerfile",
    ".env.example",
    ".devcontainer/**/*",
    "uv.lock",
    "pyproject.toml",
    ".github/workflows/python-app.yml",
    "scripts/**/*",
    "scripts/**/*",
    ".env"
]

def rename_template(new_project_name: str):
    for path in paths_to_replace:
        files = glob.glob(path, recursive=True)
        for file in files:
            if not os.path.isfile(file) or file.__contains__("rename-template.py"):
                continue
            with open(file, "r") as f:
                content = f.read()
            content = content.replace("python-template", new_project_name)
            content = content.replace("python_template", new_project_name.replace("-", "_"))
            with open(file, "w") as f:
                f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("new_project_name", type=str)
    args = parser.parse_args()
    rename_template(args.new_project_name)
