import re
from typing import List
from vnnv.config import console
from rich.panel import Panel


def markdown_to_latex(lines: List[List[str]]) -> List[str]:
    """
    @todo: Docstring for markdown_to_latex

    /lines/ @todo

    """
    regex_dict = {
        'heading': r'(#+)\s(?P<text>.*)',
        'code': r'(```|~~~)(?P<text>.*)',
        'hide': r'(?P<text>^([lL][iI][nN][kK])|^([tT][aA][gG][sS]))',
        'inline_link': r'^\!\[(?P<text>.*?)\]\((?P<path>.*?)\)',
        'hyper_link': r'^\[(?P<text>.*?)\]\((?P<path>.*?)\)',
        'list':
        r'^((?P<star>\*[\s]{1,3})|(?P<number>^(\d\.)[\s]{1,3}))(?P<text>.*)',
        'listend': r'^(\W)|^(?![\s\S]|^(\n))'
    }
    level_to_heading = {
        '1': 'chapter',
        '2': 'section',
        '3': 'subsubsection',
        '4': 'paragraph',
        '5': 'subparagraph'
    }

    latex = ''
    codeblock = False
    list = False
    list_type = None
    for lines in lines:
        for i, line in enumerate(lines):
            # Convert the markdown headers to latex
            match = re.match(regex_dict['heading'], line)
            if match:
                if not codeblock:
                    level = len(match.group(1))
                    latex += '\\' + level_to_heading[str(
                        level)] + '{' + match.group('text') + '}\n'
                    continue
                else:
                    pass

            # Convert codeblock
            match = re.match(regex_dict['code'], line)
            if match:
                if not codeblock:
                    codeblock = True
                    # language = match.group(1)
                    latex += '\\begin{comment}\n'
                    continue
                elif codeblock:
                    codeblock = False
                    latex += '\\end{comment}\n'
                    continue

            match = re.match(regex_dict['list'], line)
            if match:
                if not list:
                    list = True
                    if match.group('star'):
                        list_type = 'itemize'
                        latex += '\\begin{itemize}\n'
                        latex += '\\item ' + match.group('text') + '\n'
                        continue
                    elif match.group('number'):
                        list_type = 'enumerate'
                        latex += '\\begin{enumerate}\n'
                        latex += '\\item ' + match.group('text') + '\n'
                        continue
                elif list:
                    latex += '\\item ' + match.group('text') + '\n'
                    continue

            if list:
                match = re.search(regex_dict['listend'], line)
                if match:
                    list = False
                    if list_type == 'itemize':
                        latex += '\\end{itemize}\n'
                        latex += line
                        continue
                    elif list_type == 'enumerate':
                        latex += '\\end{enumerate}\n'
                        latex += line
                        continue
            latex += line
    latex = typeset_markdown_to_latex(latex)
    return latex


def typeset_markdown_to_latex(latex):
    # console.print(MATH)
    BOLD_REGEX = r'\*\*([\S\s]+?)\*\*'
    ITALIC_REGEX = r'(?<!\*)\*([\S\s]+?)\*(?!\*)'
    UNDERLINE_REGEX = r'\_([\S\s]+?)\_'
    regex_list = [(BOLD_REGEX, r'\\textbf{\1}'),
                  (ITALIC_REGEX, r'\\textit{\1}'),
                  (UNDERLINE_REGEX, r'\\underlatex{\1}')]



    for regex, replace in regex_list:

        def math_and_link_check(match, latex=latex, regex=regex, replace=replace):
            inside_math = False
            MATH = re.findall(r'(?:\\\(|\\\[)([\s\S]*?)(?:\\\]|\\\))', latex)
            LINKS = re.findall(r'', latex)
            console.print(MATH)
            upper_sub_match = match.group(0)
            console.print('upper_sub_match:', upper_sub_match)
            for i, math in enumerate(MATH):
                console.print('math: ', math)
                if set(upper_sub_match).issubset(set(math)):
                    # console.print(Panel.fit(upper_sub_match, 'is a subset of math str: ', math, style='succes'))
                    # console.print(Panel(upper_sub_match, 'is a subset of math str: ', math, style='succes'))
                    console.print(Panel.fit(upper_sub_match + ' is a subset of math str: ' + math, style='error'))
                    inside_math = True
            if not inside_math:
                upper_sub_replace = re.sub(regex, replace, upper_sub_match)
                return upper_sub_replace
            else:
                return match.group(0)

        latex = re.sub(regex, math_and_link_check, latex)
    # latex = re.sub(ITALIC_REGEX, , latex)
    # latex = re.sub(UNDERlatex_REGEX, , latex)
    return latex


def vnnv_flashcards_to_apy(flashcards) -> str:
    """
    @todo: Docstring for vnnv_flashcards_to_apy

    /flashcards/ @todo

    """
    # console.print(flashcards)
    # for flashcard in flashcards:
    #     for field in flashcard

    vnnv_fields_keys = [
        list(flashcard['fields'].keys()) for flashcard in flashcards
    ]
    # console.print(vnnv_fields_keys)
    vnnv_fields_values = [
        list(flashcard['fields'].values()) for flashcard in flashcards
    ]
    # console.print(vnnv_fields_values)

    lines = ''
    lines += 'model: Cloze\n'

    # console.print(flashcards)
    for i, fc in enumerate(flashcards):
        lines += '# Note ' + str(i + 1) + '\n'
        # console.print(flashcards[i]['tags'])
        lines += 'tags: ' + ' '.join(fc['tags']) + '\n'
        lines += 'deck: ' + fc['deck'] + '\n'
        for j in range(len(vnnv_fields_keys)):
            # console.print(fc)
            # console.print(j)
            lines += '## ' + vnnv_fields_keys[i][j] + '\n'
            field = vnnv_fields_values[i][j]
            field = re.sub(
                r'<question>\n([\s\S]*?)</question>',
                r"\1<hr style='height:2px;border-width:0;color:gray;background-color:gray'>",
                field)
            field = re.sub(r'<answer>([\s\S]*?)</answer>',
                           r"<span style='font-size:30px'>\1</span>", field)
            lines += field + '\n'

            # @todo: copy library links to anki media collection

    return lines
    # apy_notes = [
    #     '# Note ' + str(i + 1) + '\n' +
    #     'tags: ' + ' '.join(flashcard['tags']) + '\n' +
    #     'deck: ' + flashcard['deck'] + '\n' +
    #     '## ' + vnnv_fields_keys[i][0] + '\n' +
    #     vnnv_fields_values[i][0] + '\n' +
    #     '## ' + vnnv_fields_keys[i][1] + '\n' +
    #     vnnv_fields_values[i][1] + '\n'
    #     for i, flashcard in enumerate(flashcards)
    # ]
    # console.print(''.join(apy_notes))
