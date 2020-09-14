import re
import difflib
from pathlib import Path
from typing import List
from vnnv.config import console
from rich.panel import Panel


# taken from https://stackoverflow.com/questions/14128763/how-to-find-the-overlap-between-2-sequences-and-return-it
def get_overlap(s1, s2):
    s = difflib.SequenceMatcher(None, s1, s2)
    pos_a, pos_b, size = s.find_longest_match(0, len(s1), 0, len(s2))
    return s1[pos_a:pos_a + size]


def markdown_to_latex(lines_and_links: List[List[str]]) -> List[str]:
    """
    @todo: Docstring for markdown_to_latex

    /lines/ @todo

    """
    regex_dict = {
        'heading': r'(#+)\s(?P<text>.*)',
        'code': r'(```|~~~)(?P<language>.*)',
        'hide': r'(?P<text>^([lL][iI][nN][kK])|^([tT][aA][gG][sS]))',
        'inline_link': r'^\!\[(?P<text>.*?)\]\((?P<url>.*?)\)',
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
    vnnv_anki = False
    list = False
    list_type = None
    all_links = []
    for lines, links in lines_and_links:
        all_links += links
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
                    if match.group('language') == '{.vnnv_anki}':
                        latex += '\\begin{verbatim}\n'
                        vnnv_anki = True
                    else:
                        latex += '\\begin{comment}\n'
                    continue
                elif codeblock:
                    codeblock = False
                    if vnnv_anki:
                        vnnv_anki = False
                        latex += '\\end{verbatim}\n'
                        continue
                    latex += '\\end{comment}\n'
                    continue

            # @todo: Convert here flashcards someday

            # Convert inline links to images/pdfs here
            match = re.match(regex_dict['inline_link'], line)
            if match:
                text = match.group('text')
                url = match.group('url')
                match = re.match(r'.*?(\..*$)', url)
                if match:
                    suffix = match.group(1)
                    if suffix != '.pdf':
                        latex += '\n\\begin{figure}[h!]\n\centering\n' + '\\fbox{\\includegraphics[width=\\textwidth, height=0.4\\textheight, keepaspectratio]{' + url.replace(
                            '\ ', ' '
                        ) + '}}\n' + '\\caption{' + text + '}\n' + '\\end{figure}\n'
                    else:
                        latex += '\\includepdf[scale=0.92, pages=-, pagecommand=\subsection{' + text + '}, offset= 0 -2cm]{' + url.replace(
                            r'\\ ', ' ') + '}\n'
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
    # print(latex)
    latex = typeset_markdown_to_latex(latex, all_links)
    print(latex)
    return latex


def typeset_markdown_to_latex(latex, links):
    # console.print(MATH)
    BOLD_REGEX = r'\*\*([\S\s]+?)\*\*'
    ITALIC_REGEX = r'(?<!\*)\*([\S\s]+?)\*(?!\*)'
    UNDERSCORE_REGEX = r'(?<![\\])\_([^\_]+?)\_'
    LINK_REGEX = r'(?<![\\\w+\{\}])\[([\s\S]+?)\](?![\\\(\{\}])'
    regex_list = [(BOLD_REGEX, r'\\textbf{\1}'),
                  (ITALIC_REGEX, r'\\textit{\1}'), (LINK_REGEX, '')]
    #(UNDERSCORE_REGEX, r'\\underline{\1}')]
    if links:
        link_info = {}
        for link in links:
            match = re.match(
                r'\[(?P<text>.*)\]: (?P<url>(?P<internet>https?\:\/\/)?.+?(?P<suffix>\.\w{1,5})?$)',
                link)
            if match:
                link = match.group(0)
                link_info[link] = {}
                link_info[link]['text'] = match.group('text')
                link_info[link]['url'] = match.group('url')
                link_info[link]['suffix'] = match.group('suffix')
                link_info[link]['internet'] = match.group('internet')

    console.print(link_info)
    link_regex = False
    for regex, replace in regex_list:
        if regex == LINK_REGEX:
            link_regex = True

        def math_and_link_check(match,
                                latex=latex,
                                regex=regex,
                                replace=replace,
                                links=link_info,
                                link_regex=link_regex):
            inside_math = False
            MATH = re.findall(r'((?:\\\(|\\\[)[\s\S]*?(?:\\\]|\\\)))', latex)
            # console.print(MATH)
            upper_sub_match = match.group(0)
            console.print('upper_sub_match:', upper_sub_match)
            math_delimiters = ['\\[', '\\]', '\\(', '\\)']
            for i, math in enumerate(MATH):
                console.print('math: ', math)
                if upper_sub_match in math:
                    inside_math = True
                    break

                overlap = get_overlap(upper_sub_match, math)
                for math_delimiter in math_delimiters:
                    if math_delimiter in overlap:
                        inside_math = True
                        break
                    else:
                        console.print(overlap)
                        console.print(
                            Panel.fit('no overlapping delimitter',
                                      style='succes'))
            if not inside_math:
                if link_regex:
                    console.print('Need info on the link! ' +
                                  match.group(0).replace('[', r'\\['),
                                  style='warning')
                    for preamble_link in links.keys():
                        console.print(
                            'subset:',
                            match.group(0).replace('[', r'\\['),
                            links[preamble_link]['text'].replace('[', r'\\['))
                        if match.group(1) in links[preamble_link]['text']:
                            if links[preamble_link]['internet'] is not None:
                                replace = r'\\href{' + links[preamble_link][
                                    'url'].replace('\ ', ' ') + r'}{' + links[
                                        preamble_link]['text'] + r'}\n'
                                break
                            else:
                                replace = r'\\href{run:../../../../../../' + links[
                                    preamble_link]['url'].replace(
                                        '\ ', ' ') + r'}{' + links[
                                            preamble_link]['text'] + r'}\n'
                                break

                    # for link in links:
                    # if link_info:
                    #     if link_info.group('internet'):
                    #         replace = r'\\href\{\1\}'
                upper_sub_replace = re.sub(regex, replace.replace('_', '\\_'),
                                           upper_sub_match)
                return upper_sub_replace
            else:
                return match.group(0)

        latex = re.sub(regex, math_and_link_check, latex)
        if regex == LINK_REGEX:
            link_regex = False

    # latex = re.sub(ITALIC_REGEX, , latex)
    # latex = re.sub(UNDERlatex_REGEX, , latex)
    latex = latex.replace('%', '\%')
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
        for j in range(len(vnnv_fields_keys[i])):
            # console.print(fc)
            # console.print(j)
            lines += '## ' + vnnv_fields_keys[i][j] + '\n'
            field = vnnv_fields_values[i][j]
            field = re.sub(
                r'<question>\n([\s\S]*?)</question>',
                r"<span style='font-size:30px'>\1</span><hr style='height:2px;border-width:0;color:gray;background-color:gray'>",
                field)
            field = re.sub(r'<answer>([\s\S]*?)</answer>',
                           r"<span style='font-size:30px'>\1</span>", field)
            field = field.replace(r"{{", r"{ {")
            field = field.replace(r"}}", r"} }")
            field = re.sub(r'<cloze>([\s\S]*?)</cloze>', r"{{c1::\1}}", field)
            image_urls = re.findall(r'\!\[[^]]*?\]\(([^\)]*?)\)', field)
            for url in image_urls:
                name = Path(url).name
                field = re.sub(r'\!\[[^]]*?\]\(' + url + r'\)',
                               r'<img src="' + name + '">', field)
            lines += field + '\n'

            # @todo: copy library links to anki media collection

    # console.print(lines)
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
