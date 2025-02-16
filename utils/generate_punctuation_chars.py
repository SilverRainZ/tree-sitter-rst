#!/usr/bin/env python3

from docutils.utils.punctuation_chars import openers, closers, delimiters

def is_ascii(ch):
    return ord(ch) <= 127

def c_repr(ch) -> str:
    if is_ascii(ch):
        if ch == "'":
            return "'\\''" # special case for single quote
        return repr(ch)
    return "L'" + ch.encode('unicode_escape').decode() + "'"


def generate_c_chars_define(name: str, chars: str) -> list[str]:
    INDENT = ' ' * 2
    c_chars = ['const int32_t %s[] = {' % name ]
    c_char_ranges = ['const int32_t %s_range[][2] = {' % name]
    range_start = None
    for i, ch in enumerate(chars):
        if range_start is not None:
            if ch == '-':
                continue # skip range sign
            if is_ascii(ch):
                raise Exception("expect unicode, found ascii: %s" % ch)
            c_char_ranges.append(INDENT + "{ %s, %s }," % (c_repr(range_start), c_repr(ch)))
            range_start = None

        if not is_ascii(ch) and i != len(chars)-1 and chars[i+1] == '-':
            range_start = ch
            continue

        c_chars.append(INDENT + c_repr(ch) + ',')
            
    c_chars.append('};')
    c_char_ranges.append('};')

    return c_chars + c_char_ranges

if __name__ == '__main__':
    lines = [
        '// This file is generated by `generate_punctuation_chars.py, DO NOT EDIT`',
        '',
        '#ifndef TREE_SITTER_RST_PUNCTUATION_CHARS_H_',
        '#define TREE_SITTER_RST_PUNCTUATION_CHARS_H_',
        '',
    ]

    lines.extend(generate_c_chars_define('start_chars', openers))
    lines.append('')

    lines.extend(generate_c_chars_define('delim_chars', delimiters))
    lines.append('')

    lines.extend(generate_c_chars_define('end_chars', closers))
    lines.append('')

    lines.append('#endif /* ifndef TREE_SITTER_RST_PUNCTUATION_CHARS_H_ */')

    print('\n'.join(lines))
