import filecmp
from pathlib import Path

def compare_files_in_directories(dir_check):
    dir_check = Path(dir_check)
    student_dirs = [x for x in dir_check.iterdir() if x.is_dir()] # get all directories in dir_check

    results = []
    for i, dir1 in enumerate(student_dirs):
        for dir2 in student_dirs[i+1:]:
            plagiarized_files = compare_two_directories(dir1, dir2)
            if plagiarized_files:
                results.append((dir1.name, dir2.name, plagiarized_files))
    return results

def compare_two_directories(dir1, dir2):
    files_dir1 = list(dir1.glob('**/*.*'))
    files_dir2 = list(dir2.glob('**/*.*'))

    matches = []
    for file1 in files_dir1:
        for file2 in files_dir2:
            if file1.name == file2.name and filecmp.cmp(file1, file2, shallow=False):
                matches.append(file1.name)
    return matches


if __name__ == "__main__":
    print(compare_files_in_directories('./analyse/'))