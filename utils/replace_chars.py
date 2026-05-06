def replace_chars(str: str, char: str, index: int = 0, count: int = 1 ) -> str:
    return str[:index] + char * count + str[(index + count):]