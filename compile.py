"""
Compile mdzk docs to mkdocs-friendly format.
"""
from dataclasses import dataclass
import os
import shutil

import yaml

COMPILED_DIR = "compiled/docs"


def read_config():
    with open("mdzk.yml") as f:
        return yaml.load(f)


cfg = read_config()
DOCS_DIR = os.path.expanduser(cfg["docs_dir"])


@dataclass
class Note:

    filename: str

    def note_name(self):
        return os.path.splitext(self.filename)[0]

    def compiled_body(self):
        return flesh_out_note(self.note_name())

    def is_docs_worthy(self):
        cfg = read_config()

        return any(
            f"[{i}]" in self.compiled_body() or self.note_name() == i
            for i in cfg.get("include", [])
        ) and not any(
            f"[{i}]" in self.compiled_body() or self.note_name() == i
            for i in cfg.get("exclude", [])
        )


def _is_tag(word):
    # TODO: improve with regex
    return (word.startswith("#") and not set(word) == set("#")) or word.startswith("+")


def _format_tag(tag):
    tag_clean = tag.strip("#+.,").replace("-", " ")
    note = tag.strip("#+,.").strip("+")
    return f"[{tag_clean}]({note}.md)"


def _maybe_format(word):
    if _is_tag(word):
        return _format_tag(word)
    return word


def flesh_out_note(note):
    filename = f"{note}.md"
    with open(os.path.join(DOCS_DIR, filename)) as f:
        body = f.read()
    rows = body.split("\n")
    fmt_rows = [" ".join([_maybe_format(w) for w in row.split()]) for row in rows]
    fmt_body = "\n".join(fmt_rows)
    return fmt_body


def notes():
    return sorted(f for f in os.listdir(DOCS_DIR) if not f.startswith("."))


def compile_notes():
    shutil.rmtree(COMPILED_DIR)
    os.makedirs(COMPILED_DIR)
    for filename in notes():
        n = Note(filename=filename)
        if not n.is_docs_worthy():
            continue
        with open(f"{COMPILED_DIR}/{n.note_name()}.md", "w") as f:
            print(os.path.join(DOCS_DIR, n.filename))
            f.write(n.compiled_body())


def main():
    compile_notes()


if __name__ == "__main__":
    main()
