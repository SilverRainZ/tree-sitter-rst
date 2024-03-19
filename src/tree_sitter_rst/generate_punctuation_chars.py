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


def generate_c_chars_define(name: str, chars: str) -> str:
    INDENT = ' ' * 2
    c_chars = ['const int32_t punctuation_chars_%s[] = {' % name ]
    c_char_ranges = ['const int32_t punctuation_char_%s_range[][2] = {' % name]
    range_start = None
    for i, ch in enumerate(chars):
        if range_start is not None:
            if ch == '-':
                continue # skip range sign
            if is_ascii(ch):
                raise Exception("expect unicode, found ascii: %s" % ch)
            c_char_ranges.append(INDENT + "{ %s, %s }" % (c_repr(range_start), c_repr(ch)))
            range_start = None

        if not is_ascii(ch) and i != len(chars)-1 and chars[i+1] == '-':
            range_start = ch
            continue

        c_chars.append(INDENT + c_repr(ch) + ',')
            
    c_chars.append('};')
    c_char_ranges.append('};')

    return '\n'.join(c_chars + [''] + c_char_ranges)

if __name__ == '__main__':
    print('#ifndef TREE_SITTER_RST_PUNCTUATION_CHARS_H_')
    print('#define TREE_SITTER_RST_PUNCTUATION_CHARS_H_')
    print(generate_c_chars_define('openers', openers))
    print(generate_c_chars_define('delimiters', delimiters))
    print(generate_c_chars_define('closers', closers))
    print('#endif /* ifndef TREE_SITTER_RST_PUNCTUATION_CHARS_H_ */')
