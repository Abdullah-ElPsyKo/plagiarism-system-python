import filecmp
from pathlib import Path
import re
from cst_comments import *
from check_with_ast import *

def compare_student_directories(root_dir):
    root_dir = Path(root_dir)
    student_dirs = [x for x in root_dir.iterdir() if x.is_dir()]

    plagiarism_results = []
    comment_plagiarism_results = []

    for i, dir1 in enumerate(student_dirs):
        for dir2 in student_dirs[i+1:]:
            identical_files = find_matching_files(dir1, dir2)
            if identical_files:
                plagiarism_results.append((dir1.name, dir2.name, identical_files))
            comment_results = compare_file_contents(dir1, dir2, identical_files)
            comment_plagiarism_results.append(comment_results)

    return plagiarism_results, comment_plagiarism_results

def find_matching_files(dir1, dir2):
    files_dir1 = list(dir1.glob('**/*.*'))
    files_dir2 = list(dir2.glob('**/*.*'))

    identical_files = []
    for file1 in files_dir1:
        for file2 in files_dir2:
            if file1.name == file2.name and filecmp.cmp(file1, file2, shallow=False):
                identical_files.append(file1.name)
    return identical_files

def compare_file_contents(dir1, dir2, matching_files):
    identical_comments = set()
    cst_checks = []
    ast_checks = []

    for file1 in get_python_files(dir1):
        file1_content, file1_comments = read_file_and_extract_comments(file1)
        for file2 in get_python_files(dir2):
            if file1.name != file2.name or file1.name not in matching_files:
                file2_content, file2_comments = read_file_and_extract_comments(file2)
                
                # Using the are_asts_identical function
                ast_check = are_asts_identical(file1_content, file2_content)
                if ast_check:
                    ast_checks.append((file1.name, file2.name))
                
                # Using the check_cst_comments function
                cst_check = check_cst_comments(file1_content, file2_content)
                if cst_check:
                    cst_checks.append((file1.name, file2.name))
                
                identical_comments.update(file1_comments.intersection(file2_comments))

    return (dir1.name, dir2.name, identical_comments, cst_checks, ast_checks)

def get_python_files(directory):
    return directory.glob('**/*.py')

def read_file_and_extract_comments(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    comments = set(re.findall(r'#(.*)', content))
    return content, comments

