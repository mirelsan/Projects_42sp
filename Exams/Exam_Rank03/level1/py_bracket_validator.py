def bracket_validator(s: str) -> bool:
   pilha = []
   pares = {'[':']', '(':')', '{':'}'}

   for c in s:
       if c in pares:
           pilha.append(c)
       elif c in pares.values():
           if not pilha:
               return False
           aberto = pilha.pop()


           if pares[aberto] != c:
               return False

   return len(pilha) == 0
