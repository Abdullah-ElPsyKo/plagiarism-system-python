import jinja2 as j2

env = j2.Environment(
    loader=j2.FileSystemLoader("."),
    autoescape=j2.select_autoescape(),
)

students = ["student 1", "student 2", "student 3"]

# dict[str, dict[str, list[str]]]
report_matrix = {f"student_{student[0]}": {f"student_{other_student[0]}": ["/"] for other_student in enumerate(students, start=1)} for student in enumerate(students, start=1)}

report_matrix['student_1']['student_2'] = ['dezelfde verdachte fout']
report_matrix['student_3']['student_1'] = ['dezelfde verdachte fout']

mapped_matrix = [[report_matrix[student1][student][0] for student in report_matrix] for student1 in report_matrix] 
all_students = [student for student in report_matrix]

template = env.get_template('outputtemplate.html')

html_content = template.render(students=all_students, report_matrix=mapped_matrix)

output_file_name = 'report.html'  # of vraag de gebruiker om een bestandsnaam
with open(output_file_name, 'w') as file:
    file.write(html_content)