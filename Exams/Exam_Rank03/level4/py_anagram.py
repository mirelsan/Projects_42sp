def anagram(s1: str, s2: str) -> bool:
    clean_s1 = sorted(s1.lower().replace(" ", ""))
    clean_s2 = sorted(s2.lower().replace(" ", ""))

    return(clean_s1 == clean_s2)

if __name__ == "__main__":
    print(anagram("listen", "silent"))
    print(anagram("", ""))
    print(anagram("abc", "abcc"))