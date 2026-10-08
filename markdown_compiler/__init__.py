
'''
This file contains functions that work on entire documents at a time
(and not line-by-line).
'''

from markdown_compiler.util.line_functions import (
    compile_headers,
    compile_strikethrough,
    compile_bold_stars,
    compile_bold_underscore,
    compile_italic_star,
    compile_italic_underscore,
    compile_code_inline,
    compile_images,
    compile_links,
)


def compile_lines(text):
    r'''
    Apply all markdown transformations to the input text.

    >>> compile_lines('This is a **bold** _italic_ `code` test.\nAnd *another line*!\n')
    '<p>\nThis is a <b>bold</b> <i>italic</i> <code>code</code> test.\nAnd <i>another line</i>!\n</p>'

    >>> compile_lines("""
    ... This is a **bold** _italic_ `code` test.
    ... And *another line*!
    ... """)
    '\n<p>\nThis is a <b>bold</b> <i>italic</i> <code>code</code> test.\nAnd <i>another line</i>!\n</p>'

    >>> print(compile_lines("""
    ... This is a **bold** _italic_ `code` test.
    ... And *another line*!
    ... """))
    <BLANKLINE>
    <p>
    This is a <b>bold</b> <i>italic</i> <code>code</code> test.
    And <i>another line</i>!
    </p>

    >>> print(compile_lines("""
    ... *paragraph1*
    ...
    ... **paragraph2**
    ...
    ... `paragraph3`
    ... """))
    <BLANKLINE>
    <p>
    <i>paragraph1</i>
    </p>
    <p>
    <b>paragraph2</b>
    </p>
    <p>
    <code>paragraph3</code>
    </p>

    >>> print(compile_lines("""
    ... ```
    ... x = 1*2 + 3*4
    ... ```
    ... """))
    <BLANKLINE>
    <pre>
    x = 1*2 + 3*4
    </pre>
    <BLANKLINE>

    >>> print(compile_lines("""
    ... Consider the following code block:
    ... ```
    ... x = 1*2 + 3*4
    ... ```
    ... """))
    <BLANKLINE>
    <p>
    Consider the following code block:
    <pre>
    x = 1*2 + 3*4
    </pre>
    </p>

    >>> print(compile_lines("""
    ... Consider the following code block:
    ... ```
    ... x = 1*2 + 3*4
    ... print('x=', x)
    ... ```
    ... And here's another code block:
    ... ```
    ... print(this_is_a_variable)
    ... ```
    ... """))
    <BLANKLINE>
    <p>
    Consider the following code block:
    <pre>
    x = 1*2 + 3*4
    print('x=', x)
    </pre>
    And here's another code block:
    <pre>
    print(this_is_a_variable)
    </pre>
    </p>

    >>> print(compile_lines("""
    ... ```
    ... for i in range(10):
    ...     print('i=',i)
    ... ```
    ... """))
    <BLANKLINE>
    <pre>
    for i in range(10):
        print('i=',i)
    </pre>
    <BLANKLINE>


    >>> compile_lines('1. Apple\n')
    '<ol>\n<li>Apple</li>\n</ol>'

    >>> compile_lines('1. Apple\n2. Banana\n3. Cherry\n')
    '<ol>\n<li>Apple</li>\n<li>Banana</li>\n<li>Cherry</li>\n</ol>'

    >>> compile_lines('Hello\n\n1. Apple\n2. Banana\n\nGoodbye\n')
    '<p>\nHello\n</p>\n<ol>\n<li>Apple</li>\n<li>Banana</li>\n</ol>\n<p>\nGoodbye\n</p>'

    '''
    lines = text.split('\n')
    new_lines = []
    in_paragraph = False
    in_code = False
    in_list = False

    for line in lines:
        stripped = line.strip()

        # Handle fenced code blocks.
        if stripped.startswith('```'):
            if in_list:
                new_lines.append('</ol>')
                in_list = False

            if in_code:
                new_lines.append('</pre>')
                in_code = False
            else:
                new_lines.append('<pre>')
                in_code = True
            continue

        # Preserve original indentation inside code blocks.
        if in_code:
            new_lines.append(line)
            continue

        line = stripped

        # Identify ordered list items.
        dot = line.find('. ')
        is_list_item = dot > 0 and line[:dot].isdigit()

        if is_list_item:
            if in_paragraph:
                new_lines.append('</p>')
                in_paragraph = False

            if not in_list:
                new_lines.append('<ol>')
                in_list = True

            item = line[dot + 2:]
            item = compile_headers(item)
            item = compile_strikethrough(item)
            item = compile_bold_stars(item)
            item = compile_bold_underscore(item)
            item = compile_italic_star(item)
            item = compile_italic_underscore(item)
            item = compile_code_inline(item)
            item = compile_images(item)
            item = compile_links(item)

            new_lines.append(f'<li>{item}</li>')
            continue

        if in_list:
            new_lines.append('</ol>')
            in_list = False

            # A blank line after a list is a separator.
            if line == '':
                continue

        if line == '':
            if in_paragraph:
                new_lines.append('</p>')
                in_paragraph = False
            else:
                new_lines.append('')
            continue

        if line[0] != '#' and not in_paragraph:
            in_paragraph = True
            line = '<p>\n' + line

        line = compile_headers(line)
        line = compile_strikethrough(line)
        line = compile_bold_stars(line)
        line = compile_bold_underscore(line)
        line = compile_italic_star(line)
        line = compile_italic_underscore(line)
        line = compile_code_inline(line)
        line = compile_images(line)
        line = compile_links(line)

        new_lines.append(line)

    if in_list:
        new_lines.append('</ol>')

    return '\n'.join(new_lines)


def markdown_to_html(markdown, add_css):
    '''
    Convert the input markdown into valid HTML,
    optionally adding CSS formatting.

    >>> assert(markdown_to_html('this *is* a _test_', False))
    >>> assert(markdown_to_html('this *is* a _test_', True))
    '''

    html = '''
<html>
<head>
    <style>
    ins { text-decoration: line-through; }
    </style>
    '''

    if add_css:
        html += '''
<link rel="stylesheet" href="https://izbicki.me/css/code.css" />
<link rel="stylesheet" href="https://izbicki.me/css/default.css" />
        '''

    html += '''
</head>
<body>
    ''' + compile_lines(markdown) + '''
</body>
</html>
    '''

    return html


def minify(html):
    r'''
    Collapse whitespace in a plain-text sample.

    >>> minify('       ')
    ''
    >>> minify('   a    ')
    'a'
    >>> minify('   a    b        c    ')
    'a b c'
    >>> minify('a b c')
    'a b c'
    >>> minify('a\nb\nc')
    'a b c'
    >>> minify('a \nb\n c')
    'a b c'
    >>> minify('a\n\n\n\n\n\n\n\n\n\n\n\n\n\nb\n\n\n\n\n\n\n\n\n\n')
    'a b'
    '''
    return ' '.join(html.split())


def convert_file(input_file, add_css):
    '''
    Convert the input markdown file into an HTML file.
    If the input filename is README.md,
    the output filename will be README.html.
    '''

    # Validate the input file.
    if input_file[-3:] != '.md':
        raise ValueError('input_file does not end in .md')

    # Read the Markdown file.
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown = f.read()

    # Compile Markdown without minifying code-block whitespace.
    html = markdown_to_html(markdown, add_css)

    # Save the HTML output.
    with open(input_file[:-2] + 'html', 'w', encoding='utf-8') as f:
        f.write(html)
