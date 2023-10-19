import os
import sys
import copy
import math
import random

from asplblock import Nilad, Monad, Dyad, Infiniad

if len(sys.argv) == 2:
    outf = sys.argv[1]
elif len(sys.argv) == 3 and sys.argv[1][0] == "-":
    for flag in sys.argv[1][1:]:
        if flag == "a":
            infl = f"{os.path.dirname(__file__)}/{sys.argv[2]}"
        elif flag == "f":
            infl = f"{sys.argv[2]}"
        else:
            raise TypeError("This flag is not correct!")
            sys.exit(1)

with open(infl) as file:
    code = file.read()

temp = ["", "", "", "", ""]
Stack = []
Variables = {}

def aspl_map(arr, block):
    global Stack
    narr = []
    for i in arr:
        Stack.append(i)
        aspl_parse(block.code)
        narr.append(Stack[-1])
        Stack.pop()
    return narr

def list_gr(l1, l2):
    narr = []
    for i, j in list(zip(l1, l2)):
        narr.append(int(i < j))
    return narr

def list_lt(l1, l2):
    narr = []
    for i, j in list(zip(l1, l2)):
        narr.append(int(i > j))
    return narr

def aspl_ssplit(string, ln):
    return [string[i:i+ln] for i in range(0, len(string), ln)]

def aspl_operat(ms, oper):
    if oper == "*":
        while len(ms) > 1:
            ms[-2] *= ms[-1]
            ms.pop()
        return ms[0]

def aspl_digits(snum):
    if all([i in "0123456789" for i in snum]):
        return 1
    return 0


def aspl_parse(cd):
    global Stack, Variables, temp
    c = list(cd) + ["EOF"]
    pos = 0

    while c[pos] != "EOF":
        if c[pos:pos+2] == ["\\", "["]:
            while c[pos:pos+2] != ["]", "\\"]:
                pos += 1

        elif c[pos] in "0123456789":
            while c[pos] in "0123456789":
                temp[0] += c[pos]
                pos += 1
            pos -= 1
            Stack.append(int(temp[0]))
            temp[0] = ""

        elif c[pos] == "\"":
            pos += 1
            while c[pos] != "\"":
                temp[0] += c[pos]
                pos += 1
            Stack.append(temp[0])
            temp[0] = ""

        elif c[pos] == "+":
            if (type(Stack[-2]) == int and type(Stack[-1]) == int) or \
                (type(Stack[-2]) == list and type(Stack[-1]) == list):
                Stack[-2] += Stack[-1]
                Stack.pop()
            elif (type(Stack[-2]) == list and type(Stack[-1]) == int) or\
                (type(Stack[-2]) == list and type(Stack[-1]) == str):
                Stack[-2].append(Stack[-1])
                Stack.pop()
            elif type(Stack[-2]) == list and type(Stack[-1]) == CodeBlock:
                Stack[-2] = aspl_map(Stack[-2], Stack[-1])
                Stack.pop()
            elif type(Stack[-2]) == str and type(Stack[-1]) == list:
                Stack[-2] += "".join(str(i) for i in Stack[-1])
                Stack.pop()
            elif type(Stack[-2]) == str and type(Stack[-1]) == int:
                Stack[-2] = "".join([chr(ord(i)+Stack[-1]) for i in Stack[-2]])
                Stack.pop()
    

        elif c[pos] == "-":
            if type(Stack[-2]) == int and type(Stack[-1]) == int:
                Stack[-2] -= Stack[-1]
                Stack.pop()
            elif type(Stack[-2]) == str and type(Stack[-1]) == int:
                Stack[-2] = Stack[-2][:-Stack[-1]]
                Stack.pop()
            elif type(Stack[-2]) == list and type(Stack[-1]) == int:
                for i in range(Stack[-1]):
                    Stack[-2].pop()
                Stack.pop()
    
        elif c[pos] == "*":
            if (type(Stack[-2]) == int and type(Stack[-1]) == int) or \
                (type(Stack[-2]) == str and type(Stack[-1]) == int) or \
                (type(Stack[-2]) == list and type(Stack[-1]) == int):
                Stack[-2] *= Stack[-1]
                Stack.pop()
            elif type(Stack[-2]) == str and type(Stack[-1]) == str:
                Stack[-2] = "".join([i*len(Stack[-1]) for i in Stack[-2]])
                Stack.pop()

        elif c[pos] == "/":
            if type(Stack[-2]) == int and type(Stack[-1]) == int:
                Stack[-2] /= Stack[-1]
                Stack.pop()
            elif type(Stack[-2]) == list and type(Stack[-1]) == int:
                Stack[-2] = aspl_ssplit(Stack[-2], Stack[-1])
                Stack.pop()

        elif c[pos] == "_":
            if type(Stack[-1]) == int:
                Stack[-1] *= -1
            elif type(Stack[-1]) == list:
                if len(Stack[-1]) == 1:
                    Stack[-1] = list(range(0, Stack[-1][0]+1))
                elif len(Stack[-1]) == 2:
                    Stack[-1] = list(range(Stack[-1][0], Stack[-1][1]+1))
                elif len(Stack[-1]) == 3:
                    Stack[-1] = list(range(Stack[-1][0], Stack[-1][1]+1, Stack[-1][2]))

        elif c[pos] == "%":
            if type(Stack[-1]) == list:
                Stack[-1] = list(set(Stack[-1]))
            elif type(Stack[-2]) == int and type(Stack[-1]) == int:
                Stack[-2] %= Stack[-1]
                Stack.pop()


        elif c[pos] == "<":
            if type(Stack[-2]) == int and type(Stack[-1]) == int:
                Stack.append(int(Stack[-2] < Stack[-1]))
                Stack.pop(-2)
                Stack.pop(-2)
            elif type(Stack[-2]) == list and type(Stack[-1]) == list:
                Stack.append(list_gr(Stack[-2], Stack[-1]))
                Stack.pop(-2)
                Stack.pop(-2)

        elif c[pos] == ">":
            if type(Stack[-2]) == int and type(Stack[-1]) == int:
                Stack.append(int(Stack[-2] > Stack[-1]))
                Stack.pop(-2)
                Stack.pop(-2)
            elif type(Stack[-2]) == list and type(Stack[-1]) == list:
                Stack.append(list_lt(Stack[-2], Stack[-1]))
                Stack.pop(-2)
                Stack.pop(-2)

        elif c[pos] == "=":
            Stack.append(int(Stack[-2] == Stack[-1]))
            Stack.pop(-2)
            Stack.pop(-2)

        elif c[pos] == "[":
            pos += 1
            while c[pos] != "]":
                temp[0] += c[pos]
                pos += 1
            Stack.append([])
            if temp[0] != "":
                for i in temp[0].split(" "):
                    if i == "":
                        continue
                    elif (i[0] == "-" and aspl_digits(i[1:])) or aspl_digits(i):
                        Stack[-1].append(int(i))
                    elif i[0] == "\"" and i[-1] == "\"" and len(i) >= 2:
                        Stack[-1].append(i[1:-1])

                temp[0] = ""

        elif c[pos] == ".":
            if type(Stack[-1]) == list:
                print("[", end = "")
                for i, j in enumerate(Stack[-1]):
                    if i == len(Stack[-1]) - 1:
                        print(f"{j}]", end = "")
                    else:
                        print(f"{j} ", end = "")

                Stack.pop()
            else:
                print(Stack.pop(), end = "")
        elif c[pos] == ",":
            print(chr(Stack.pop()), end = "")

        elif c[pos] == "{":
            pos += 1
            copd = 1
            while copd != 0:
                if c[pos] == "{":
                    copd += 1
                elif c[pos] == "}":
                    copd -= 1
                temp[0] += c[pos]
                pos += 1
            Stack.append(Nilad(temp[0][:-1]))
            temp[0] = ""
            pos -= 1

        elif c[pos] == "«":
            pos += 1
            copd = 1
            while copd != 0:
                if c[pos] == "«":
                    copd += 1
                elif c[pos] == "»":
                    copd -= 1
                temp[0] += c[pos]
                pos += 1
            Stack.append(Monad(temp[0][:-1]))
            temp[0] = ""
            pos -= 1

        elif c[pos] == "‘":
            pos += 1
            copd = 1
            while copd != 0:
                if c[pos] == "‘":
                    copd += 1
                elif c[pos] == "’":
                    copd -= 1
                temp[0] += c[pos]
                pos += 1
            Stack.append(Dyad(temp[0][:-1]))
            temp[0] = ""
            pos -= 1

        elif c[pos] == "“":
            pos += 1
            copd = 1
            while copd != 0:
                if c[pos] == "“":
                    copd += 1
                elif c[pos] == "”":
                    copd -= 1
                temp[0] += c[pos]
                pos += 1
            Stack.append(Infiniad(temp[0][:-1]))
            temp[0] = ""
            pos -= 1

        elif c[pos] == "!":
            if type(Stack[-1]) == int:
                Stack[-1] = math.factorial(Stack[-1])
            elif type(Stack[-1]) == list:
                Stack[-1].sort()
            elif type(Stack[-1]) == Nilad:
                aspl_parse(Stack.pop().code)
            elif type(Stack[-2]) == Monad:
                aspl_parse(Stack.pop(-2).code.replace(f"'{chr(0x3b1)}'", Stack[-1][0]))
            elif type(Stack[-2]) == Dyad:
                aspl_parse(Stack.pop(-2).code.replace(f"'{chr(0x3b1)}'", Stack[-1][0]).replace("'{0x3b2}'", Stack[-1][1]))
            elif type(Stack[-2]) == Infiniad:
                for i1, i2 in enumerate(Stack[-1]):
                    Stack[-2] = Stack[-2].replace(f"'{chr(0x3c9)}{i1}'", i2)


        elif c[pos] == "$":
            Stack.append(copy.deepcopy(Stack[-1]))
        elif c[pos] == "&":
            Stack.pop()
        elif c[pos] == "^":
            Stack[-2], Stack[-1] = Stack[-1], Stack[-2]
        elif c[pos] == "`":
            Stack.reverse()

        elif c[pos] == "~":
            Stack.append(int(input()))
        elif c[pos] == "@":
            Stack.append(str(input()))

        elif c[pos] == ":":
            pos += 1
            while c[pos] != " " and c[pos] != "\n" and c[pos] != "!" and c[pos] != "{" and c[pos] != "}" and c[pos] != "EOF":
                temp[0] += c[pos]
                pos += 1
            Variables[temp[0]] = Stack[-1]
            Stack.pop()
            temp[0] = ""
            pos -= 1

        elif c[pos] == ";":
            pos += 1
            while c[pos] != " " and c[pos] != "\n" and c[pos] != "!" and c[pos] != "{" and c[pos] != "}" and c[pos] != "EOF":
                temp[0] += c[pos]
                pos += 1
            Stack.append(Variables[temp[0]])
            temp[0] = ""
            pos -= 1

        elif c[pos] == "?":
            t1 = Stack.pop(-2)
            t2 = Stack.pop(-1)
            aspl_parse(t1.code)
            if Stack[-1] != 0:
                aspl_parse(t2.code)

        elif c[pos] == "¿":
            t1 = Stack.pop(-3)
            t2 = Stack.pop(-2)
            t3 = Stack.pop(-1)
            aspl_parse(t1.code)
            if Stack[-1] != 0:
                aspl_parse(t2.code)
            else:
                aspl_parse(t3.code)

        elif c[pos] == "#":
            t1 = Stack.pop(-2)
            t2 = Stack.pop(-1)
            aspl_parse(t1.code)
            while Stack[-1] != 0:
                aspl_parse(t2.code)
                aspl_parse(t1.code)

        elif c[pos] == "×":
            if type(Stack[-1]) == list:
                Stack[-1] = sum(Stack[-1])
            elif type(Stack[-2]) == int and type(Stack[-1]) == int:
                Stack[-2] **= Stack[-1]

        elif c[pos] == "÷":
            if type(Stack[-1]) == list:
                Stack[-1] = random.choice(Stack[-1])
            elif type(Stack[-2]) == int and type(Stack[-1]) == int:
                Stack[-2] = random.randint(Stack[-2], Stack[-1])
                Stack.pop()

        elif c[pos] == "¬":
            pos += 1
            while c[pos] != " " and c[pos] != "\n" and c[pos] != "!" and c[pos] != "{" and c[pos] != "}":
                temp[0] += c[pos]
                pos += 1
            if temp[0] == "and":
                Stack[-2] = int(Stack[-2] and Stack[-1])
                Stack.pop()
            elif temp[0] == "or":
                Stack[-2] = int(Stack[-2] or Stack[-1])
                Stack.pop()
            elif temp[0] == "not":
                Stack[-1] = int(not Stack[-1])
            elif temp[0] == "neq":
                Stack[-2] = int(Stack[-2] != Stack[-1])
                Stack.pop()
            elif temp[0] == "band":
                Stack[-2] = Stack[-2] & Stack[-1]
                Stack.pop()
            elif temp[0] == "bor":
                Stack[-2] = Stack[-2] | Stack[-1]
                Stack.pop()
            elif temp[0] == "leq":
                Stack[-2] = Stack[-2] <= Stack[-1]
                Stack.pop()
            elif temp[0] == "geq":
                Stack[-2] = Stack[-2] >= Stack[-1]
                Stack.pop()

            elif temp[0] == "sin":
                Stack[-1] = math.sin(Stack[-1])
            elif temp[0] == "cos":
                Stack[-1] = math.cos(Stack[-1])
            elif temp[0] == "tan":
                Stack[-1] = math.tan(Stack[-1])

            elif temp[0] == "bm":
                t1 = Stack[-2]
                t2 = Stack[-1]
                t3 = []
                for i in t1:
                    if i in t2:
                        t3.append(1)
                    else:
                        t3.append(0)
                Stack.pop()
                Stack[-1] = t3
            elif temp[0] == "nbm":
                t1 = Stack[-2]
                t2 = Stack[-1]
                t3 = []
                for i in t1:
                    if i not in t2:
                        t3.append(1)
                    else:
                        t3.append(0)
                Stack.pop()
                Stack[-1] = t3
            elif temp[0] == "fl":
                t1 = Stack[-2]
                t2 = Stack[-1]
                t3 = []
                for i in t1:
                    if i in t2:
                        t3.append(i)
                Stack.pop()
                Stack[-1] = t3
            elif temp[0] == "nfl":
                t1 = Stack[-2]
                t2 = Stack[-1]
                t3 = []
                for i in t1:
                    if i not in t2:
                        t3.append(i)
                Stack.pop()
                Stack[-1] = t3
            elif temp[0] == "ln":
                Stack[-1] = len(Stack[-1])

            elif temp[0] == "sum":
                Stack[-1] = sum(Stack[-1])
            elif temp[0] == "prod":
                Stack[-1] = aspl_operat(Stack[-1], "*")

        elif c[pos] == "v":
            rt = [Stack[-2], Stack[-1]]
            Stack.pop()
            Stack.pop()
            for i in range(rt[1]):
                aspl_parse(rt[0].code)
        elif c[pos:pos+2] == ["f", " "]:
            pos += 2
            rt = [Stack[-2], Stack[-1]]
            Stack.pop()
            Stack.pop()
            while c[pos] != " " and c[pos] != "\n" and c[pos] != "!" and c[pos] != "{" and c[pos] != "}" and c[pos] != "EOF":
                temp[1] += c[pos]
                pos += 1
            Variables[temp[1]] = 0
            for i in rt[1]:
                Variables[temp[1]] = i
                aspl_parse(rt[0].code)


#            temp[0] = ""


        pos += 1

# Uncomment for debugging
#        print(Stack, Variables)

aspl_parse(code)
