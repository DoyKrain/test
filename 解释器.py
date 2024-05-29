from lexicalanalysis import lexer
from 中间代码 import IntermediateCode


class relolver:
    def __init__(self, gencode):
        self.gencode = gencode  # 存储四元式
        self.output = []

    def main1(self):
        stack = {}
        pc = 0
        while True:
            i = self.gencode[pc]
            op = i[0]
            if op == 'main':
                pc = pc + 1
            elif op == '=':
                if str(i[1]).isdigit():
                    stack[i[3]] = int(i[1])
                else:
                    if i[1] in ['read()', 'read']:
                        print("请输入一个数字：")
                        stack[i[3]] = int(input())
                    elif not i[1].isdigit():
                        stack[i[3]] = stack[i[1]]
                    else:
                        stack[i[3]] = stack[i[1]] +stack[i[3]]
                pc = pc + 1
            elif op == '+':
                if i[1].isdigit() and i[2].isdigit():
                    stack[i[3]] = int(i[1]) + int(i[2])
                elif not i[1].isdigit() and i[2].isdigit():
                    stack[i[3]] = stack[i[1]] + int(i[2])
                elif i[1].isdigit() and not i[2].isdigit():
                    stack[i[3]] = int(i[1]) + stack[i[2]]
                elif not i[1].isdigit() and not i[2].isdigit():
                    stack[i[3]] = stack[i[1]] + stack[i[2]]
                pc = pc + 1
            elif op == '-':
                if i[1].isdigit() and i[2].isdigit():
                    stack[i[3]] = int(i[2]) - int(i[1])
                elif not i[1].isdigit() and i[2].isdigit():
                    stack[i[3]] = int(i[2]) - stack[i[1]]
                elif i[1].isdigit() and not i[2].isdigit():
                    stack[i[3]] = stack[i[2]] - int(i[1])
                elif not i[1].isdigit() and not i[2].isdigit():
                    stack[i[3]] = stack[i[2]] - stack[i[1]]
                pc = pc + 1
            elif op == '*':
                if i[1].isdigit() and i[2].isdigit():
                    stack[i[3]] = int(i[1]) * int(i[2])
                elif not i[1].isdigit() and i[2].isdigit():
                    stack[i[3]] = stack[i[1]] * int(i[2])
                elif i[1].isdigit() and not i[2].isdigit():
                    stack[i[3]] = int(i[1]) * stack[i[2]]
                elif not i[1].isdigit() and not i[2].isdigit():
                    stack[i[3]] = stack[i[1]] * stack[i[2]]
                pc = pc + 1
            elif op == '/':
                if i[1].isdigit() and i[2].isdigit():
                    stack[i[3]] = int(i[1]) / int(i[2])
                elif not i[1].isdigit() and i[2].isdigit():
                    stack[i[3]] = stack[i[1]] / int(i[2])
                elif i[1].isdigit() and not i[2].isdigit():
                    stack[i[3]] = int(i[1]) / stack[i[2]]
                elif not i[1].isdigit() and not i[2].isdigit():
                    stack[i[3]] = stack[i[1]] / stack[i[2]]
                pc = pc + 1
            elif op == '%':
                if i[2].isdigit() and i[1].isdigit():
                    stack[i[3]] = int(i[2]) % int(i[1])
                elif not i[2].isdigit() and i[1].isdigit():
                    stack[i[3]] = stack[i[2]] % int(i[1])
                elif i[2].isdigit() and not i[1].isdigit():
                    stack[i[3]] = int(i[2]) % stack[i[1]]
                elif not i[2].isdigit() and not i[1].isdigit():
                    stack[i[3]] = stack[i[2]] % stack[i[1]]
                pc = pc + 1
            elif op == '<':
                if i[2].isdigit():
                    if stack[i[1]] < int(i[2]):
                        pc = int(i[3]) - 1
                    else:
                        pc = pc + 1
                else:
                    if stack[i[1]] < stack[i[2]]:
                        pc = int(i[3]) - 1
                    else:
                        pc = pc + 1
            elif op == '<=':
                if i[2].isdigit():
                    if stack[i[1]] <= int(i[2]):
                        pc = int(i[3]) - 1
                    else:
                        pc = pc + 1
                else:
                    if stack[i[1]] <= stack[i[2]]:
                        pc = int(i[3]) - 1
                    else:
                        pc = pc + 1
            elif op == '>=':
                if i[2].isdigit():
                    if stack[i[1]] >= int(i[2]):
                        pc = int(i[3]) - 1
                else:
                    if stack[i[1]] >= stack[i[2]]:
                        pc = int(i[3]) - 1
                    else:
                        pc = pc + 1
            elif op == '>':
                if i[2].isdigit():
                    if stack[i[1]] > int(i[2]):
                        pc = int(i[3]) - 1
                    else:
                        pc = pc + 1
                else:
                    if stack[i[1]] > stack[i[2]]:
                        pc = int(i[3]) - 1
                    else:
                        pc = pc + 1
            elif op == '==':
                if i[1].isdigit():
                    if int(i[1]) == int(i[2]):
                        pc = int(i[3]) - 1
                        continue
                else:
                    if stack[i[1]] == int(i[2]):
                        pc = int(i[3]) - 1
                        continue
                pc = pc + 1
            elif op == '!=':
                if stack[i[1]] != int(i[2]):
                    pc = int(i[3]) - 1
                pc = pc + 1
            elif op == '!':
                pass
            elif op == '&&':
                if not i[1].isdigit() and not i[2].isdigit():
                    if stack[i[1]] != 0 and stack[i[2]] != 0:
                        stack[i[3]] = 1
                    else:
                        stack[i[3]] = 0
                if i[1].isdigit() and i[2].isdigit():
                    if int(i[1]) != 0 and int(i[2]) != 0:
                        stack[i[3]] = 1
                    else:
                        stack[i[3]] = 0
                if not i[1].isdigit() and i[2].isdigit():
                    if stack[i[1]] != 0 and int(i[2]) != 0:
                        stack[i[3]] = 1
                    else:
                        stack[i[3]] = 0
                if i[1].isdigit() and not i[2].isdigit():
                    if int(i[1]) != 0 and stack[i[2]] != 0:
                        stack[i[3]] = 1
                    else:
                        stack[i[3]] = 0
                pc = pc + 1
            elif op == '||':
                if not i[1].isdigit() and not i[2].isdigit():
                    if stack[i[1]] != 0 or stack[i[2]] != 0:
                        stack[i[3]] = 1
                    else:
                        stack[i[3]] = 0
                if i[1].isdigit() and i[2].isdigit():
                    if int(i[1]) != 0 or int(i[2]) != 0:
                        stack[i[3]] = 1
                    else:
                        stack[i[3]] = 0
                if not i[1].isdigit() and i[2].isdigit():
                    if stack[i[1]] != 0 or int(i[2]) != 0:
                        stack[i[3]] = 1
                    else:
                        stack[i[3]] = 0
                if i[1].isdigit() and not i[2].isdigit():
                    if int(i[1]) != 0 or stack[i[2]] != 0:
                        stack[i[3]] = 1
                    else:
                        stack[i[3]] = 0
                pc = pc + 1
            elif op == '':
                if i[3] != '':
                    pc = int(i[3]) - 1
                elif i[3] == '':
                    pc = pc + 1
            elif op == 'write':
                print(stack[i[2]])
                self.output.append(stack[i[2]])
                # print(self.output)
                if i[3] != '':
                    pc = int(i[3]) - 1
                    continue
                else:
                    pc = pc + 1
            elif op == 'read':
                pc = pc + 1
            elif op == 'if':
                if i[3] != '':
                    pc = int(i[3]) - 1
                else:
                    pc = pc + 1
            elif op == 'else':
                pc = int(i[3]) - 1
            elif op == 'for':
                pc = int(i[3]) - 1
            elif op == 'while':
                pc = int(i[3]) - 1
            elif op == 'do-while':
                pc = int(i[3]) - 1
            elif op == 'sys':
                break
        return self.output
            # print(stack)


if __name__ == '__main__':
    f = open("tesst/test0.1.txt", 'r', encoding='UTF-8-sig')
    words = f.read()
    a = lexer(words)
    res, error = a.token()
    n = IntermediateCode(res)
    gencode, const_variable = n.main0()
    sd = relolver(gencode)
    sd.main1()
    for i in res:
        print(i)
    print("-----------------")
    for i in gencode:
        print(i)
