
'''
Each of the functions in this file takes a single line of input
and transforms the line in some way.
'''


def replace_markers(line, marker, tag):
    """Replace matching Markdown markers with HTML tags."""
    result = ""
    position = 0

    while position < len(line):
        start = line.find(marker, position)

        if start == -1:
            result += line[position:]
            break

        end = line.find(marker, start + len(marker))

        if end == -1 or end == start + len(marker):
            result += line[position:]
            break

        result += line[position:start]
        content = line[start + len(marker):end]
        result += f"<{tag}>{content}</{tag}>"
        position = end + len(marker)

    return result


def compile_headers(line):
    '''
    Convert markdown headers into <h1>,<h2>,etc tags.

    >>> compile_headers('# This is the main header')
    '<h1> This is the main header</h1>'
    >>> compile_headers('## This is a sub-header')
    '<h2> This is a sub-header</h2>'
    >>> compile_headers('### This is a sub-header')
    '<h3> This is a sub-header</h3>'
    >>> compile_headers('#### This is a sub-header')
    '<h4> This is a sub-header</h4>'
    >>> compile_headers('##### This is a sub-header')
    '<h5> This is a sub-header</h5>'
    >>> compile_headers('###### This is a sub-header')
    '<h6> This is a sub-header</h6>'
    >>> compile_headers('      # this is not a header')
    '      # this is not a header'
    '''
    for level in range(6, 0, -1):
        marker = "#" * level
        if line.startswith(marker + " "):
            return f"<h{level}>{line[level:]}</h{level}>"
    return line


def compile_italic_star(line):
    '''
    Convert "*italic*" into "<i>italic</i>".

    >>> compile_italic_star('*This is italic!* This is not italic.')
    '<i>This is italic!</i> This is not italic.'
    >>> compile_italic_star('*This is italic!*')
    '<i>This is italic!</i>'
    >>> compile_italic_star('This is *italic*!')
    'This is <i>italic</i>!'
    >>> compile_italic_star('This is not *italic!')
    'This is not *italic!'
    >>> compile_italic_star('*')
    '*'
    '''
    return replace_markers(line, "*", "i")


def compile_italic_underscore(line):
    '''
    Convert "_italic_" into "<i>italic</i>".

    >>> compile_italic_underscore('_This is italic!_ This is not italic.')
    '<i>This is italic!</i> This is not italic.'
    >>> compile_italic_underscore('_This is italic!_')
    '<i>This is italic!</i>'
    >>> compile_italic_underscore('This is _italic_!')
    'This is <i>italic</i>!'
    >>> compile_italic_underscore('This is not _italic!')
    'This is not _italic!'
    >>> compile_italic_underscore('_')
    '_'
    '''
    return replace_markers(line, "_", "i")


def compile_strikethrough(line):
    '''
    Convert "~~strikethrough~~" to "<ins>strikethrough</ins>".

    >>> compile_strikethrough('~~This is strikethrough!~~ This is not strikethrough.')
    '<ins>This is strikethrough!</ins> This is not strikethrough.'
    >>> compile_strikethrough('~~This is strikethrough!~~')
    '<ins>This is strikethrough!</ins>'
    >>> compile_strikethrough('This is ~~strikethrough~~!')
    'This is <ins>strikethrough</ins>!'
    >>> compile_strikethrough('This is not ~~strikethrough!')
    'This is not ~~strikethrough!'
    >>> compile_strikethrough('~~')
    '~~'
    '''
    return replace_markers(line, "~~", "ins")


def compile_bold_stars(line):
    '''
    Convert "**bold**" to "<b>bold</b>".

    >>> compile_bold_stars('**This is bold!** This is not bold.')
    '<b>This is bold!</b> This is not bold.'
    >>> compile_bold_stars('**This is bold!**')
    '<b>This is bold!</b>'
    >>> compile_bold_stars('This is **bold**!')
    'This is <b>bold</b>!'
    >>> compile_bold_stars('This is not **bold!')
    'This is not **bold!'
    >>> compile_bold_stars('**')
    '**'
    '''
    return replace_markers(line, "**", "b")


def compile_bold_underscore(line):
    '''
    Convert "__bold__" to "<b>bold</b>".

    >>> compile_bold_underscore('__This is bold!__ This is not bold.')
    '<b>This is bold!</b> This is not bold.'
    >>> compile_bold_underscore('__This is bold!__')
    '<b>This is bold!</b>'
    >>> compile_bold_underscore('This is __bold__!')
    'This is <b>bold</b>!'
    >>> compile_bold_underscore('This is not __bold!')
    'This is not __bold!'
    >>> compile_bold_underscore('__')
    '__'
    '''
    return replace_markers(line, "__", "b")


def compile_code_inline(line):
    '''
    Add <code> tags.

    >>> compile_code_inline('You can use backticks like this (`1+2`) to include code in the middle of text.')
    'You can use backticks like this (<code>1+2</code>) to include code in the middle of text.'
    >>> compile_code_inline('This is inline code: `1+2`')
    'This is inline code: <code>1+2</code>'
    >>> compile_code_inline('`1+2`')
    '<code>1+2</code>'
    >>> compile_code_inline('This example has html within the code: `<b>bold!</b>`')
    'This example has html within the code: <code>&lt;b&gt;bold!&lt;/b&gt;</code>'
    >>> compile_code_inline('this example has a math formula in the  code: `1 + 2 < 4`')
    'this example has a math formula in the  code: <code>1 + 2 &lt; 4</code>'
    >>> compile_code_inline('this example has a <b>math formula</b> in the  code: `1 + 2 < 4`')
    'this example has a <b>math formula</b> in the  code: <code>1 + 2 &lt; 4</code>'
    >>> compile_code_inline('```')
    '```'
    >>> compile_code_inline('```python3')
    '```python3'
    '''
    result = ""
    position = 0

    while position < len(line):
        start = line.find("`", position)

        if start == -1:
            result += line[position:]
            break

        end = line.find("`", start + 1)

        if end == -1:
            result += line[position:]
            break

        if end == start + 1:
            result += line[position:end + 1]
            position = end + 1
            continue

        result += line[position:start]
        content = line[start + 1:end]
        content = content.replace("<", "&lt;")
        content = content.replace(">", "&gt;")
        result += f"<code>{content}</code>"

        position = end + 1

    return result


def compile_links(line):
    '''
    Add <a> tags.

    >>> compile_links('Click on the [course webpage](https://github.com/mikeizbicki/cmc-csci040)!')
    'Click on the <a href="https://github.com/mikeizbicki/cmc-csci040">course webpage</a>!'
    >>> compile_links('[course webpage](https://github.com/mikeizbicki/cmc-csci040)')
    '<a href="https://github.com/mikeizbicki/cmc-csci040">course webpage</a>'
    >>> compile_links('this is wrong: [course webpage]    (https://github.com/mikeizbicki/cmc-csci040)')
    'this is wrong: [course webpage]    (https://github.com/mikeizbicki/cmc-csci040)'
    >>> compile_links('this is wrong: [course webpage](https://github.com/mikeizbicki/cmc-csci040')
    'this is wrong: [course webpage](https://github.com/mikeizbicki/cmc-csci040'
    '''
    result = ""
    position = 0

    while position < len(line):
        start = line.find("[", position)

        if start == -1:
            result += line[position:]
            break

        end_text = line.find("](", start)

        if end_text == -1:
            result += line[position:]
            break

        end_url = line.find(")", end_text + 2)

        if end_url == -1:
            result += line[position:]
            break

        result += line[position:start]

        label = line[start + 1:end_text]
        url = line[end_text + 2:end_url]

        result += f'<a href="{url}">{label}</a>'
        position = end_url + 1

    return result


def compile_images(line):
    '''
    Add <img> tags.

    >>> compile_images('[Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)')
    '[Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)'
    >>> compile_images('![Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)')
    '<img src="https://avatars1.githubusercontent.com/u/1052630?v=2&s=460" alt="Mike Izbicki" />'
    >>> compile_images('This is an image of Mike Izbicki: ![Mike Izbicki](https://avatars1.githubusercontent.com/u/1052630?v=2&s=460)')
    'This is an image of Mike Izbicki: <img src="https://avatars1.githubusercontent.com/u/1052630?v=2&s=460" alt="Mike Izbicki" />'
    '''
    result = ""
    position = 0

    while position < len(line):
        start = line.find("![", position)

        if start == -1:
            result += line[position:]
            break

        end_text = line.find("](", start)

        if end_text == -1:
            result += line[position:]
            break

        end_url = line.find(")", end_text + 2)

        if end_url == -1:
            result += line[position:]
            break

        result += line[position:start]

        alt = line[start + 2:end_text]
        url = line[end_text + 2:end_url]

        result += f'<img src="{url}" alt="{alt}" />'
        position = end_url + 1

    return result
