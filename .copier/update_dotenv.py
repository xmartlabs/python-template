from pathlib import Path
import json

# Update the .env file with the answers from the .copier-answers.yml file
root_path = Path(__file__).parent.parent
answers_path = Path(__file__).parent / ".copier-answers.yml"
answers = json.loads(answers_path.read_text())
env_example_path = root_path / ".env.example"
env_content = env_example_path.read_text()
lines = []
for line in env_content.splitlines():
    for key, value in answers.items():
        upper_key = key.upper()
        if line.startswith(f"{upper_key}="):
            if " " in value:
                content = f"{upper_key}={value!r}"
            else:
                content = f"{upper_key}={value}"
            new_line = line.replace(line, content)
            lines.append(new_line)
            break
    else:
        lines.append(line)
env_example_path.write_text("\n".join(lines))

# this creates a .env file with the same content as the .env.example file.
env_file_path = root_path / ".env"
env_file_path.write_text(env_example_path.read_text())