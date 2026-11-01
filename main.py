import argparse
import ast
import io
import logging
import os
import sys
import tokenize

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
        description="Extracts and formats code docstrings and comments into a uniform Markdown style."
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

def _docstring_entries(tree):
    entries = []

    def visit(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                owner = f"{prefix}{child.name}" if prefix else child.name
                # get_docstring cleans the text: it expands tabs and strips the uniform indent. What lands in the Markdown is therefore not the docstring exactly as written in the source, which matters if a reader compares the two side by side.
                doc = ast.get_docstring(child)
                if doc:
                    kind = 'class docstring' if isinstance(child, ast.ClassDef) else 'function docstring'
                    entries.append({'owner': owner, 'kind': kind, 'text': doc, 'lineno': child.lineno})
                # Only functions, async functions, and classes get an owner entry. A docstring shaped string sitting in an if block or assigned to a variable is invisible to this walk, however much it reads like documentation.
                visit(child, f"{owner}.")
            else:
                visit(child, prefix)

    module_doc = ast.get_docstring(tree)
    if module_doc:
        # The module entry is appended after the walk and carries a fixed line number of 1, then the sort in extract puts it first. A file that opens with a comment block before its docstring will show the module entry ahead of that earlier comment, because the sort is stable and the module line number is invented.
        entries.append({'owner': 'module', 'kind': 'module docstring', 'text': module_doc, 'lineno': 1})
    visit(tree, '')
    return entries

def _comment_entries(source):
    entries = []
    block = []
    block_start = None
    last_line = None

    def flush():
        nonlocal block, block_start
        if block:
            entries.append({'owner': 'comment', 'kind': 'comment', 'text': '\n'.join(block), 'lineno': block_start})
            block = []
            block_start = None

    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for tok in tokens:
            if tok.type == tokenize.COMMENT:
                line_no = tok.start[0]
                # A comment block is just consecutive lines. One blank line, or one line of code, splits what a person reads as one note into two entries, and a trailing comment on a code line starts a block of its own.
                if block and last_line is not None and line_no == last_line + 1:
                    block.append(tok.string)
                else:
                    flush()
                    block = [tok.string]
                    block_start = line_no
                last_line = line_no
    except tokenize.TokenError as e:
        logger.error(f"Parse error: {e}")
        sys.exit(1)
    flush()
    return entries

def extract_docstrings(file_path):
    """
    Extracts docstrings and comment blocks from the provided Python file.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        list: A list of entries, each a dict with owner, kind, and text, in source order.
    """
    try:
        with open(file_path, 'r') as file:
            source = file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred while extracting docstrings: {e}")
        sys.exit(1)

    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError as e:
        logger.error(f"Parse error in {file_path}: {e}")
        sys.exit(1)

    # Docstrings and comments come from two different parses of the same text, ast for one and tokenize for the other, and neither knows about the other list. A hash line inside a docstring is never double counted, because tokenize treats the whole string as one token.
    entries = _docstring_entries(tree) + _comment_entries(source)
    # Sorting is by first line only. A long docstring and a comment that sits inside its line range keep whatever order the sort leaves them in, so entries can interleave oddly in a dense file.
    entries.sort(key=lambda entry: entry['lineno'])
    return entries

def save_docstrings_to_markdown(entries, output_file):
    """
    Saves the extracted entries to a Markdown file.

    Args:
        entries (list): A list of entry dicts with owner, kind, and text.
        output_file (str): Path to the output Markdown file.
    """
    try:
        with open(output_file, 'w') as file:
            for index, entry in enumerate(entries, start=1):
                file.write(f"## Entry {index}: {entry['owner']} ({entry['kind']})\n\n")
                file.write(f"```\n{entry['text']}\n```\n\n")
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

    if os.path.realpath(output_file) == os.path.realpath(file_path):
        logger.error("Output file must not equal the input file.")
        sys.exit(1)

    logger.info(f"Extracting docstrings from {file_path}")
    entries = extract_docstrings(file_path)
    logger.info(f"Extracted {len(entries)} entries")

    # A file with no docstrings and no comments exits 1 and writes nothing. I would rather fail that way than leave an empty Markdown file that looks like a finished extraction.
    if not entries:
        logger.error("Nothing extracted: no docstrings or comments were found.")
        sys.exit(1)

    logger.info(f"Saving docstrings to {output_file}")
    save_docstrings_to_markdown(entries, output_file)

if __name__ == '__main__':
    main()
