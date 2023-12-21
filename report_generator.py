import jinja2 as j2
from pathlib import Path
from compare_files_dirs import *
from spelling_checker import *


env = j2.Environment(
    loader=j2.FileSystemLoader("."),
    autoescape=j2.select_autoescape(),
)


def check_plagiarism(path_to_dir):
    students_dir = Path(path_to_dir)
    
    # Creating a dictionary of student directories
    students = {i: student.name for i, student in enumerate(students_dir.iterdir(), start=1) if student.is_dir()}
    
    report_matrix = {f"student_{i}": {f"student_{j}": ["/"] for j in students} for i in students}
    
    plagiarized_files = compare_files_in_directories(students_dir)

    # Function to update matrix based on plagiarism report
    def update_matrix(student1, student2, content):
        key1 = f"student_{student1}"
        key2 = f"student_{student2}"
        content_str = f'identical {content} '
        if report_matrix[key1][key2] == ["/"]:
            report_matrix[key1][key2] = [content_str]
        else:
            report_matrix[key1][key2].append(content_str)

    # Update report matrix with plagiarism findings for identical files
    for author1, author2, identical_files in plagiarized_files[0]:
        idx1, idx2 = [list(students.values()).index(author) + 1 for author in [author1, author2]]
        if identical_files:
            update_matrix(idx1, idx2, f"file(s): {identical_files}")

    # Update report matrix with plagiarism findings for identical single line comments
    for author1, author2, comments, identical_cst, ast_result in plagiarized_files[1]:
        idx1, idx2 = [list(students.values()).index(author) + 1 for author in [author1, author2]]

        if comments:
            combined_comments = ' '.join(comments)
            combined_comments = f'variable = "{combined_comments}"'
            spelling_errors = check_spelling_errors(combined_comments)
            true_ast = {ast_checked for ast_checked in ast_result if ast_checked[2] == True}
            content = f"comment(s): {comments}. Identical spelling error(s): {spelling_errors}. Identical cst: {identical_cst}. The ASTs are identical: {true_ast}"
            update_matrix(idx1, idx2, content)

    mapped_matrix = [[report_matrix[f"student_{i}"][f"student_{j}"] for j in students] for i in students]

    return list(students.values()), mapped_matrix


def generate_report(all_students, mapped_matrix):
    template = env.get_template('outputtemplate.html')

    html_content = template.render(students=all_students, report_matrix=mapped_matrix)

    output_file_name = 'report.html'
    with open(output_file_name, 'w') as file:
        file.write(html_content)


def main():
    input_dir = input("Please enter the directory to check: ")
    all_students, mapped_matrix = check_plagiarism(f'{input_dir}')
    generate_report(all_students, mapped_matrix)


if __name__ == "__main__":
    main()