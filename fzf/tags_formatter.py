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

TAG_REGEX = r'{(?P<tags>[@a-zA-Z0-9\_\-\s\,]+)}'
TAG_REGEX_PRIMARY = r'(?P<ptag>^[a-zA-Z0-9\_\-]+)'
FILE_REGEX = r'\t(?P<parent>[\/a-zA-Z0-9_\-\@\#\%\!\$\^\&]*?)(?P<date_string_name>(?P<date_string>[\d\_\-hm]+s\_)?(?P<name>[a-zA-Z0-9\_\-]+\.[a-z]+))'


def get_tags():
    fzf_info = {}
    for i in range(len(lines)):
        # print(lines[i])
        tags = re.search(TAG_REGEX, lines[i])
        filename = re.search(FILE_REGEX, lines[i])

        if tags:
            # print(tags[0].replace('@', '').split(' '))
            tags = tags.group('tags').split(', ')
            # empty_flag = 'lowered'
        # elif not tags and primary_tag:
        #     tags = primary_tag.group('ptag').split()
        #     empty_flag = 'raised'

        if filename:
            if filename.group('date_string'):
                note_info = filename.groupdict()
            elif not filename.group('date_string'):
                note_info = filename.groupdict()
                note_info['date_string'] = ''

            note_info['tags'] = tags

            full_path = note_info['parent'] + note_info['date_string_name']

            if full_path not in fzf_info:
                fzf_info[full_path] = {
                    'name': note_info['name'],
                    'tags': note_info['tags'],
                    'date': note_info['date_string'],
                }
            # elif empty_flag == 'lowered':
            #     fzf_info[full_path] = {
            #         'name': note_info['name'],
            #         'tags': note_info['tags'],
            #         'date': note_info['date_string'],
            #     }

            # print(filename)
            # print(filename[0][0])
            # print(filename[0][1])
            # print(filename[0][2])
            # if full_name not in fzf_info:
            #     fzf_info[full_name] = {
            #         'tags': tags,
            #         'name': name,
            #         'date': date_string
            #     }
            # elif empty_flag == 'lowered':
            #     fzf_info[full_name] = {
            #         'tags': tags,
            #         'name': name,
            #         'date': date_string
            #     }
        # print(tags)
        # print(tags.group(0))
        # print(tags.group(1))
    # fzf_info = "i\'m actually what you are looking for in:"
    # print(note_info)
    # print(fzf_info)
    return fzf_info


def print_fzf_lines(fzf_info):
    # print(fzf_info)
    print_data = []
    for fn in fzf_info.keys():
        # print(fn, tags)
        # print(fzf_info[fn])
        # for tag in fzf_info[fn]['tags']:
        # if tag != '':
        print_data.append([
            fzf_info[fn]['name'], '{' +
            ", ".join([tag
                       for tag in fzf_info[fn]['tags'] if tag != '']) + '}',
            ' ' + fzf_info[fn]['date']
        ])

    col_width = max(len(word) for row in print_data[0:2]
                    for word in row) + 5  # padding
    for row in print_data:
        print("".join(word.ljust(col_width) for word in row))


fzf_info = get_tags()
# print(fzf_info)
print_fzf_lines(fzf_info)
