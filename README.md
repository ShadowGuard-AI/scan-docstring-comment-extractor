## scan-Docstring-Comment-Extractor

### Description

scan-Docstring-Comment-Extractor is a tool for extracting and formatting code docstrings into a more uniform Markdown style. This tool is focused on providing functionality for analyzing source code to identify potential security vulnerabilities. It accomplishes this by utilizing Python libraries such as mypy and Bandit to perform code analysis and security checks, enhancing the readability and accessibility of code documentation.

### Installation

```
git clone https://github.com/ShadowStrikeHQ/scan-Docstring-Comment-Extractor.git
cd scan-Docstring-Comment-Extractor
pip install -r requirements.txt
```

### Usage

```
python main.py [args]
```

### Command-Line Arguments

* **-h, --help:** Displays the help message and exits.
* **-i, --input:** Specifies the input file or directory containing the code to be analyzed.
* **-o, --output:** Specifies the output file or directory to store the extracted docstrings.
* **-f, --format:** Specifies the output format. Options include "markdown" and "json".

### Security Considerations

* Ensure that the input code is from a trusted source to avoid potential security risks.
* Review the extracted docstrings thoroughly to identify any potential vulnerabilities or security concerns.
* Maintain up-to-date versions of the tool and its dependencies to address any security patches or updates.

### License

This project is licensed under the GNU General Public License v3.0.