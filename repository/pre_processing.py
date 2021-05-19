def edit_symbol_spacing(string: str) -> str:
    _str = ''
    for c in string:
        if _is_symbol(c):
            _str += f' {c} '
            continue
        _str += c
    return _str


def _is_symbol(character: str) -> bool:
    PERSIAN_SYMBOL = ['!', '"', '#', '(', ')', '*', ',', '-', '.', '/', ':', '[', ']', '«', '»', '،', '؛', '؟',
                      '+', '=', '_', '-', '&', '^', '%', '$', '#', '@', '!', '~', '"', "'", ':', ';', '>', '<',
                      '.', ',', '/', '\\', '|', '}', '{', '-', 'ـ', ]
    if character in PERSIAN_SYMBOL:
        return True
    return False
