def string_sculptor(text: str) -> str:
    to_low: bool = True
    res: str = ""
    for char in text:
        if char.isalpha():
            if to_low:
                res += char.lower()
                to_low = False
            else:
                res += char.upper()
                to_low = True
        else:
            res += char
            if char.isspace():
                to_low = True
    return res


if __name__ == "__main__":
    print(string_sculptor("hello"))
    print(string_sculptor("Hello World"))
    print(string_sculptor("abc123def"))
    print(string_sculptor("Python3.9!"))
    print(string_sculptor(""))