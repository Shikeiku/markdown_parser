import re
from pathlib import Path

try:
    if Path('/Users/mike/Documents/markdown_notes/tags').exists():
        tags = Path('/Users/mike/Documents/markdown_notes/tags')
except:
    print('the tags file in your note is misplaced.')

# print(str(tags.parent))

t = open(str(tags), 'r')
lines = t.readlines()

TAG_REGEX = r'\/\^([@a-zA-Z0-9\_\-\s]+)\$\/'
TAG_REGEX_PRIMARY = r'(^[a-zA-Z0-9\_\-]+)'
FILE_REGEX = r'\t(([\d\_\-hm]+s\_)?([a-zA-Z0-9\_\-]+\.[a-z]+))'


def get_tags():
    fzf_info = {}
    for i in range(len(lines)):
        # print(lines[i])
        tags = re.findall(TAG_REGEX, lines[i])
        primary_tag = re.findall(TAG_REGEX_PRIMARY, lines[i])
        filename = re.findall(FILE_REGEX, lines[i])
        if tags != []:
            # print(tags[0].replace('@', '').split(' '))
            tags = tags[0].replace('@', '').split(' ')
            empty_flag = 'lowered'
        else:
            tags = primary_tag
            empty_flag = 'raised'

        if filename != []:
            # print(filename)
            full_name = filename[0][0]
            # print(filename[0][0])
            date_string = filename[0][1]
            # print(filename[0][1])
            name = filename[0][2]
            # print(filename[0][2])
            if full_name not in fzf_info:
                fzf_info[full_name] = {
                    'tags': tags,
                    'name': name,
                    'date': date_string
                }
            elif empty_flag == 'lowered':
                fzf_info[full_name] = {
                    'tags': tags,
                    'name': name,
                    'date': date_string
                }
        # print(tags)
        # print(tags.group(0))
        # print(tags.group(1))
    # print(fzf_info)
    return fzf_info


def print_fzf_lines(fzf_info):
    # print(fzf_info)
    print_data = []
    for fn in fzf_info.keys():
        # print(fn, tags)
        for tag in fzf_info[fn]['tags']:
            if tag != '':
                print_data.append([
                    tag, fzf_info[fn]['name'], " ".join([
                        '@' + tag for tag in fzf_info[fn]['tags'] if tag != ''
                    ]), ' ' + fzf_info[fn]['date']
                ])

    col_width = max(len(word) for row in print_data[0:2]
                    for word in row) + 5  # padding
    for row in print_data:
        print("".join(word.ljust(col_width) for word in row))


fzf_info = get_tags()
# print(fzf_info)
print_fzf_lines(fzf_info)
