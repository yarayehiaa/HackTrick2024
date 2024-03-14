def divide_string(string, budget):
   budget=int(budget)
   part_length = len(string) // budget
   remainder = len(string) % budget
   parts = []
   start = 0

   for i in range(budget):
      if i < remainder:
         part = string[start:start+part_length+1]
         start += part_length + 1
      else:
         part = string[start:start+part_length]
         start += part_length
      parts.append(part)
   return parts

   

string = "Secrets in spectrum."
result = divide_string(string,12)
print(result)

