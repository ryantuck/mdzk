import os

DOCS_DIR = 'notes'
COMPILED_DIR = 'compiled/docs'

def _is_tag(word):
    # TODO: improve with regex
    return (word.startswith('#') and not set(word) == set('#')) or word.startswith('+')

def _format_tag(tag):
    tag_clean = tag.strip('#+.,').replace('-', ' ')
    note = tag.strip('#+,.').strip('+')
    return f'[{tag_clean}]({note}.md)'


def _maybe_format(word):
    if _is_tag(word):
        return _format_tag(word)
    return word

def flesh_out_note(note):
    filename = f'{note}.md'
    with open(os.path.join(DOCS_DIR, filename)) as f:
        body = f.read()
    words = [_maybe_format(w) for w in body.split()]
    fmt_body = ' '.join(words)
    return fmt_body

def compile_notes():
    for filename in os.listdir(DOCS_DIR):
        note_name = os.path.splitext(filename)[0]
        compiled_body = flesh_out_note(note_name)
        with open(f'{COMPILED_DIR}/{note_name}.md', 'w') as f:
            f.write(compiled_body)


        print(os.path.join(DOCS_DIR, filename))


def main():
    compile_notes()


if __name__ == '__main__':
    main()
