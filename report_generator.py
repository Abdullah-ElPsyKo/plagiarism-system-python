import jinja2 as j2
from pathlib import Path
from compare_files_dirs import *

env = j2.Environment(
    loader=j2.FileSystemLoader("."),
    autoescape=j2.select_autoescape(),
)

def check_plagiarism(path_to_dir):
    p = Path(f'{path_to_dir}')
    students = [x.name for x in p.iterdir() if x.is_dir()]
    students_dict = {i: student for i, student in enumerate(students, start=1)}

    report_matrix = {f"student_{author}": {f"student_{other_author}": ["/"] for other_author in students_dict} for author in students_dict}

    plagiarized_files = compare_files_in_directories(f'{path_to_dir}')

    for students in plagiarized_files:
        report_matrix[f"student_{list(students_dict.values()).index(students[0]) + 1}"][f"student_{list(students_dict.values()).index(students[1]) + 1}"] = [f'identieke file(s): {students[2]}']

    mapped_matrix = [[report_matrix[student1][student][0] for student in report_matrix] for student1 in report_matrix] 
    all_students = [student for student in report_matrix]

    return all_students, mapped_matrix


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