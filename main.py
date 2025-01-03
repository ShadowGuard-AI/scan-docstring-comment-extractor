import argparse
import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_argparse():
    """
    Sets up the command-line argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Extracts and formats code docstrings into a uniform Markdown style."
    )
    parser.add_argument(
        '--file-path', 
        required=True, 
        help='Specifies the path to the Python file containing the docstrings to be extracted.'
    )
    parser.add_argument(
        '--output-file', 
        required=True, 
        help='Specifies the path to the output Markdown file where the extracted docstrings will be saved.'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help='Enables verbose output, providing additional information during the extraction process.'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version='Scan-Docstring-Comment-Extractor 1.0', 
        help='Displays the version of the tool.'
    )
    return parser

def extract_docstrings(file_path):
    """
    Extracts docstrings from the provided Python file.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        list: A list of extracted docstrings.
    """
    docstrings = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            inside_docstring = False
            current_docstring = []

            for line in lines:
                if '"""' in line or "'''" in line:
                    if inside_docstring:
                        current_docstring.append(line.strip())
                        docstrings.append('\n'.join(current_docstring))
                        current_docstring = []
                        inside_docstring = False
                    else:
                        inside_docstring = True
                        current_docstring.append(line.strip())
                elif inside_docstring:
                    current_docstring.append(line.strip())
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred while extracting docstrings: {e}")
        sys.exit(1)

    return docstrings

def save_docstrings_to_markdown(docstrings, output_file):
    """
    Saves the extracted docstrings to a Markdown file.

    Args:
        docstrings (list): A list of extracted docstrings.
        output_file (str): Path to the output Markdown file.
    """
    try:
        with open(output_file, 'w') as file:
            for index, docstring in enumerate(docstrings, start=1):
                file.write(f"## Docstring {index}\n\n")
                file.write(f"```\n{docstring}\n```\n\n")
        logger.info(f"Docstrings successfully saved to {output_file}")
    except Exception as e:
        logger.error(f"An error occurred while saving docstrings: {e}")
        sys.exit(1)

def main():
    """
    Main function that orchestrates the extraction and saving of docstrings.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    file_path = args.file_path
    output_file = args.output_file

    if not os.path.isfile(file_path):
        logger.error(f"The specified file does not exist: {file_path}")
        sys.exit(1)

    logger.info(f"Extracting docstrings from {file_path}")
    docstrings = extract_docstrings(file_path)
    logger.info(f"Extracted {len(docstrings)} docstrings")

    logger.info(f"Saving docstrings to {output_file}")
    save_docstrings_to_markdown(docstrings, output_file)

if __name__ == '__main__':
    main()