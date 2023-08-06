# Four letter config

“conf is just a four letter word”

Tiny package providing a module to handle four letter (JSON, YAML) files
for configuration, and a CLI to convert between these two file formats.

## Requirements

[PyYAML](https://pypi.org/project/PyYAML/)


## Installation

```
pip install four-letter-config
```

Installation in a virtual environment or with the `--user` oprtion is recommended.


## Usage

### Compare two files

```
python -m four_letter_config compare [ --diff ] <file_1> <file_2>
```

Each file may be a JSON or YAML file. The contents are sorted and compared.

Use the `--diff` option to get an output similar to that of the **diff** program.

### Translate JSON to YAML or vice versa

```
python -m four_letter_config translate [ --overwrite ] <file_1> <file_2>
```

Writes the contents from file_1 to file_2.

Use the `--overwrite` option to overwrite an existing file.

### Module Usage

Please refer to the reference documentation [in this repository](./docs/reference.md)
or [on GitLab Pages](https://blackstream-x.gitlab.io/four-letter-config/reference/).


## Issues, feature requests

Please open an issue [here](https://gitlab.com/blackstream-x/four-letter-config/-/issues)
if you found a bug or have a feature suggestion.
