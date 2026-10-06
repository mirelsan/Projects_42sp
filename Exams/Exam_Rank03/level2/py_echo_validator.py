def echo_validator(text: str) -> bool:
   clean = ""
   for ch in text:
       if ch.isalpha():
           clean += ch.lower()
   if clean != clean[::-1] or not clean:
       return False
   return True

if __name__ == "__main__":
    print(echo_validator("racecar"))
    print(echo_validator("A man a plan a canal Panama"))
    print(echo_validator("race a car"))
    print(echo_validator("Was it a car or a cat I saw"))
    print(echo_validator("hello"))
    print(echo_validator("Madam Im Adam"))
    print(echo_validator(""))