def solve_problem_solving_easy(input):
    try:
        words=input[0]
        x=input[1]


        counts = {}
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1


        word_count = [(word, count) for word, count in counts.items()]
        word_count.sort(key=lambda item: (-item[1], item[0]))


        sorted_words = [word for word, count in word_count]

        return sorted_words[:x]
    except Exception as e:
        print("Failed to solve PSEASY due to exception:", e)
        return []




def solve_problem_solving_medium(input):
    try:
        stack = []
        result = ""
        i=0

        while(i< len(input)):
            char=input[i]

            if char.isdigit():
                # Extract digit count and push it to the stack
                count_str = ""
                while char.isdigit():
                    count_str += char
                    char = input[input.index(char) + 1]  # Move to next char
                i+=len(count_str)-1
               

                stack.append(int(count_str))
            elif char == ']':
                word=""
                t=stack.pop()
                while(t!= '['):
                    word=t+word
                    t=stack.pop()
                count = stack.pop()  # Get the count
                #  print(count)
                result =word*count # Repeat and prepend
                stack.append(result)
            else:
                stack.append(char)
            i+=1

        result=""
        while(len(stack)!=0):
            result=stack.pop()+result



        return result
    except Exception as e:
        print("Failed to solve PSMED due to exception:", e)
        return ''
    
   

def solve_problem_solving_hard(input):
    try:

        from math import comb

        return  comb(input[0]+input[1]-2, input[0]-1)
    except Exception as e:
        print("Failed to solve PSHARD due to exception:", e)
        return 0