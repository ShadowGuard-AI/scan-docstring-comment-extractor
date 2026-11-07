## scan-Docstring-Comment-Extractor

### Description

scan-Docstring-Comment-Extractor is a tool for extracting and formatting code docstrings and comments into a more uniform Markdown style. Docstrings are taken from module, class, and function nodes with the `ast` module, each entry labelled with its owner. Hash comment blocks are collected with the `tokenize` module as their own entries, labelled as comments. Entries appear in source order, one numbered section and one fenced block per entry.

This tool uses only the Python standard library. No third party packages are required, and `requirements.txt` states that instead of naming a package.

A run that extracts nothing exits 1 with a nothing extracted status and writes no output file. A file that fails to parse exits 1 with a plain parse error line. The run also refuses at exit 1 when the resolved `--output-file` path equals the resolved `--file-path` path.

### Installation

```
git clone https://github.com/ShadowGuard-AI/scan-docstring-comment-extractor.git
cd scan-docstring-comment-extractor
pip install -r requirements.txt
```

### Usage

```
python3 main.py --file-path <python_file> --output-file <output_file> [--verbose] [--version]
```

### Command-Line Arguments

* **-h, --help:** Displays the help message and exits.
* **--file-path:** Specifies the path to the Python file containing the docstrings to be extracted. Required.
* **--output-file:** Specifies the path to the output Markdown file where the extracted docstrings will be saved. Required.
* **--verbose:** Enables verbose output, providing additional information during the extraction process.
* **--version:** Displays the version of the tool.

### Security Considerations

* Ensure that the input code is from a trusted source to avoid potential security risks.
* Review the extracted docstrings thoroughly to identify any potential vulnerabilities or security concerns.
* Maintain up-to-date versions of the tool and its dependencies to address any security patches or updates.

### License

This project is licensed under the GNU General Public License v3.0. See LICENSE.
