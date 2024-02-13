# Python Plagiarism Detection Tool

## Overview
This Python Plagiarism Detection Tool is designed to assist educators and developers in identifying similarities between Python code submissions. It leverages file comparison, Abstract Syntax Tree (AST), Concrete Syntax Tree (CST) analysis, and spelling mistake detection in comments to provide a comprehensive review.

## Features
- **Identical File Detection:** Finds and reports files with identical content.
- **Syntax Tree Comparisons:** Utilizes both AST and CST for in-depth code similarity checks beyond mere textual comparison.
- **Spelling Mistake Identification:** Detects and reports spelling mistakes within code comments, aiding in the review of coding standards.

## Installation
To use this tool, clone the repository and install the required dependencies:

```
git clone https://github.com/YourRepo/PythonPlagiarismDetectionTool.git
cd PythonPlagiarismDetectionTool
pip install -r requirements.txt
```

## Usage
Run the tool from the command line by navigating to the project directory and executing:

```
python plagiarism_detector.py [path_to_directory_containing_student_submissions]
```

The tool will generate a report detailing the plagiarism findings, which can be viewed in a generated HTML file in the project directory.

## Dependencies
- Python 3.x
- [libcst](https://pypi.org/project/libcst/)
- [spellchecker](https://pypi.org/project/pyspellchecker/)

## License
This project is licensed under the MIT License - see the LICENSE file for details.
