import filecmp
from pathlib import Path
import re


def compare_files_in_directories(dir_check): # dir_check is a path to a directory
    dir_check = Path(dir_check)
    student_dirs = [x for x in dir_check.iterdir() if x.is_dir()]

    results = []
    plagiarized_comments = []
    for i, dir1 in enumerate(student_dirs):
        for dir2 in student_dirs[i+1:]:
            plagiarized_files = compare_two_directories(dir1, dir2)
            if plagiarized_files:
                results.append((dir1.name, dir2.name, plagiarized_files))
            else:
                plagiarized_comments.append(check_comments(dir1, dir2))
    return (results, plagiarized_comments)


def compare_two_directories(dir1, dir2):
    files_dir1 = list(dir1.glob('**/*.*'))
    files_dir2 = list(dir2.glob('**/*.*'))

    matches = []
    for file1 in files_dir1:
        for file2 in files_dir2:
            if file1.name == file2.name and filecmp.cmp(file1, file2, shallow=False):
                matches.append(file1.name)
    return matches


def check_comments(dir1, dir2):
    dir1 = Path(dir1)
    dir2 = Path(dir2)
    files_dir1 = list(dir1.glob('**/*.py'))
    files_dir2 = list(dir2.glob('**/*.py'))
    for file1 in files_dir1:
        for file2 in files_dir2:
            with open(file1, 'r') as f1 , open(file2, 'r') as f2:
                file1_comments = set(re.findall(r'#(.*)', f1.read()))
                file2_comments = set(re.findall(r'#(.*)', f2.read()))
                identical_comments = file1_comments.intersection(file2_comments)
    return (dir1.name, dir2.name, identical_comments)


if __name__ == "__main__":
    check_path = "C:\\Users\\ASUS\\OneDrive - AP Hogeschool Antwerpen\\School\\Python\\blok 5\\project\\analyse"
    print(compare_files_in_directories(check_path))