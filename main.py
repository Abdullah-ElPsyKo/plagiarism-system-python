import jinja2 as j2
from pathlib import Path
from compare_files_dirs import *
from spelling_checker import check_spelling_errors

env = j2.Environment(
    loader=j2.FileSystemLoader("."),
    autoescape=j2.select_autoescape(),
)


def get_student_directories(path_to_dir):
    students_dir = Path(path_to_dir)
    return {i: student.name for i, student in enumerate(students_dir.iterdir(), start=1) if student.is_dir()}


def initialize_report_matrix(students):
    return {f"student_{i}": {f"student_{j}": ["/"] for j in students} for i in students}


def update_report_matrix(report_matrix, idx1, idx2, content):
    key1, key2 = f"student_{idx1}", f"student_{idx2}"
    if report_matrix[key1][key2] == ["/"]:
        report_matrix[key1][key2] = [content]
    else:
        report_matrix[key1][key2].append(content)


def process_plagiarism_findings(plagiarized_files, students, report_matrix):
    for author1, author2, content in plagiarized_files[0]:
        idx1, idx2 = [list(students.values()).index(author) + 1 for author in [author1, author2]]
        update_report_matrix(report_matrix, idx1, idx2, f"file(s): {content}")

    for author1, author2, comments, identical_cst, ast_result in plagiarized_files[1]:
        idx1, idx2 = [list(students.values()).index(author) + 1 for author in [author1, author2]]
        # print(f"Similarity in Code Layout (Ignoring Comments): {identical_cst}, Similarity in Logic and Flow: {ast_result}")
        process_comment_analysis(comments, report_matrix, idx1, idx2, identical_cst, ast_result)


def process_comment_analysis(comments, report_matrix, idx1, idx2, identical_cst, ast_result):
    if comments:
        combined_comments = ' '.join(comments)
        combined_comments = f'variable = "{combined_comments}"'
        spelling_errors = check_spelling_errors(combined_comments)
        parts = []

        if comments:
            parts.append(f"comment(s): {comments}")

        if spelling_errors:
            parts.append(f"Spelling error(s): {spelling_errors}")

        if identical_cst is not None:  
            parts.append(f"Similarity in Code Layout: {identical_cst}")

        if ast_result is not None:  
            parts.append(f"Similarity in Logic and Flow: {ast_result}")

        content = ". ".join(parts)
        update_report_matrix(report_matrix, idx1, idx2, content)


def generate_report(all_students, mapped_matrix):
    template = env.get_template('outputtemplate.html')
    html_content = template.render(students=all_students, report_matrix=mapped_matrix)
    output_file_name = 'report.html'
    with open(output_file_name, 'w') as file:
        file.write(html_content)


def check_plagiarism(path_to_dir):
    students = get_student_directories(path_to_dir)
    report_matrix = initialize_report_matrix(students)
    plagiarized_files = compare_student_directories(Path(path_to_dir))
    process_plagiarism_findings(plagiarized_files, students, report_matrix)
    return list(students.values()), [[report_matrix[f"student_{i}"][f"student_{j}"] for j in students] for i in students]


def main():
    input_dir = input("Please enter the directory to check: ")
    try:
        all_students, mapped_matrix = check_plagiarism(input_dir)
        generate_report(all_students, mapped_matrix)
        print("Report generated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
