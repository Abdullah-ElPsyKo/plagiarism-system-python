import filecmp
from pathlib import Path
import re
from cst_comments import *
from check_with_ast import *

def compare_files_in_directories(dir_check): # dir_check is a path to a directory
    dir_check = Path(dir_check)
    student_dirs = [x for x in dir_check.iterdir() if x.is_dir()]

    results = []
    plagiarized_comments = []

    for i, dir1 in enumerate(student_dirs):
        for dir2 in student_dirs[i+1:]:
            plagiarized_files = find_identical_files(dir1, dir2)
            if plagiarized_files:
                results.append((dir1.name, dir2.name, plagiarized_files))
            comment_results = check_content(dir1, dir2, plagiarized_files)
            plagiarized_comments.append(comment_results)

    return (results, plagiarized_comments)


def find_identical_files(dir1, dir2):
    files_dir1 = list(dir1.glob('**/*.*'))
    files_dir2 = list(dir2.glob('**/*.*'))

    matches = []
    for file1 in files_dir1:
        for file2 in files_dir2:
            if file1.name == file2.name and filecmp.cmp(file1, file2, shallow=False):
                matches.append(file1.name)
    return matches


def check_content(dir1, dir2, identical_files=None):
    dir1 = Path(dir1)
    dir2 = Path(dir2)
    files_dir1 = list(dir1.glob('**/*.py'))
    files_dir2 = list(dir2.glob('**/*.py'))

    identical_comments = set()
    ast_check = []

    for file1 in files_dir1:
        with open(file1, 'r') as f1:
            file1_content = f1.read()
            file1_comments = set(re.findall(r'#(.*)', file1_content))
            for file2 in files_dir2:
                if file1.name == file2.name and file1.name in identical_files:
                    continue
                with open(file2, 'r') as f2:
                    file2_content = f2.read()
                    ast_check.append((file1.name, file2.name, are_asts_identical(file1_content, file2_content)))
                    identical_cst = check_cst_comments(file1_content, file2_content)
                    file2_comments = set(re.findall(r'#(.*)', file2_content))
                    identical_comments.update(file1_comments.intersection(file2_comments))
    return (dir1.name, dir2.name, identical_comments, identical_cst, ast_check)





if __name__ == "__main__":
    check_path = "C:\\Users\\ASUS\\OneDrive - AP Hogeschool Antwerpen\\School\\Python\\blok 5\\analyse"
    print(compare_files_in_directories(check_path))