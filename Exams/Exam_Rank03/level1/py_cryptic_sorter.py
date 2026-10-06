def cryptic_sorter(strings: list[str]) -> list[str]:
   for i in range(len(strings)):
       for j in range(len(strings) - 1):
           a = strings[j]
           b = strings[j + 1]


           va = sum(1 for c in a.lower() if c in "aeiou")
           vb = sum(1 for c in b.lower() if c in "aeiou")


           if (len(a), a.lower(), va) > (len(b), b.lower(), vb):
               strings[j], strings[j + 1] = strings[j + 1], strings[j]
   return strings

