def mirror_matrix(matrix: list[list[int]]) -> list[list[int]]:
   result = []

   for num_list in matrix:
       result.append(num_list[::-1])
   return result
