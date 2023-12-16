import jinja2

authors = ["author 1", "author 2", "author 3"]

# dict[str, dict[str, list[str]]]
report = {author: {other_author: None for other_author in author} for author in authors}

for author in authors:
    for other_author in authors:
        report[author][other_author] = ["/"]

report['author 1']['author 2'] = ['dezelfde verdachte fout']
report['author 3']['author 1'] = ['dezelfde verdachte fout']

