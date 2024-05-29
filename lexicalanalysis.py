# 关键字
keyword = {'char': 101, 'int': 102, 'float': 103, 'break': 104, 'const': 105, 'return': 106,
           'void': 107, 'continue': 108, 'do': 109, 'while': 110, 'if': 111, 'else': 112,
           'for': 113, 'begin': 114, 'bool': 115, 'end': 116, 'false': 117, 'integer': 118,
           'real': 121, 'then': 122, 'to': 123, 'true': 124, 'var': 125, 'string': 126, 'main': 127}

# 界符，运算等符号
operator = {'(': 201, ')': 202, '[': 203, ']': 204, '!': 205, '*': 206, '/': 207, '%': 208, '+': 209,
            '-': 210, '<': 211, '<=': 212, '>': 213, '>=': 214, '==': 215, '!=': 216, '&&': 217, '||': 218,
            '=': 219, '{': 221, '}': 222, ';': 223, ',': 224, '"': 225, '--': 226, "'": 227, '|': 228,
            '&': 229, '\n': 230, '\t': 231}
# 十六进制表达
hex = 'abcdefABCDEF'
# 八进制表达
Oct = '01234567'


# 1，6：标识符，2：数字
# 状态1：正常标识符
# "引号里的字符(串)":9
class lexer(object):
    def __init__(self, words):
        self.words = words
        self.signal = 0  # 用于记录之前是否有未完结注释
        self.line = 0  # 用于记录多行注释的起始行
        self.res = []  # 全部结果展示
        self.error = []  # 记录所有出错项

    def digit_judge(self, word, i):
        a = 1
        if len(word) == a:
            self.error.append([i, word, 'digit inputting error'])
            return a
        else:
            if word[a] == '+' or word[a] == '-':
                a += 1
            while a < len(word) and word[a] != ' ' and word[a] not in operator:
                if word[a].isdigit():
                    a += 1
                else:
                    while a < len(word) and word[a] != ' ' and word[a] not in operator:
                        a += 1
                    self.error.append([i, word[:a], 'digit inputting error'])
                    return a
            self.res.append([i, word[:a], 2])
            return a

    # 数据类型及正误判断
    def isDigit(self, word, i):
        a = 0
        tmp1 = 0  # tmp1用作判断0前面有没有小数点的判断，0为没有，1则有
        tmp2 = 0  # tmp2用作判断e前面有没有小数点的判断，0为没有，1则有
        while a < len(word) and word[a] != ' ' and word[a] not in operator:
            # 如果最后只剩一个数字输入
            if len(word) == 1:
                self.res.append([i, word[a], 2])
                return a + 1
            # 开头数字为0
            if word[a] == '0':
                # 如果是单个0的输入
                if word[a + 1] == ' ' or word[a + 1] in operator:
                    print(f"[数字：{word[a]}]")
                    self.res.append([i, word[a], 2])
                    return a + 1
                a += 1
                # 如果紧跟着是小数点且之前没有小数点
                if word[a] == '.' and tmp1 == 0:
                    # 改变小数点标识符为1
                    tmp1 = 1
                    a += 1
                    if a - 1 == len(word) or word[a] == ' ' or word[a] in operator:
                        self.error.append([i, word[:a], '标点符号错误'])
                        return a
                    while a < len(word) and word[a] != ' ' and word[a] not in operator:
                        if word[a].isdigit() or word[a] == 'e':
                            # 科学计数法的判断
                            if word[a] == 'e' and a > 2:
                                if tmp2 == 0:
                                    tmp2 = 1
                                    a += self.digit_judge(word, i)
                                else:
                                    while a < len(word) and word[a] != ' ' and word[a] not in operator:
                                        a += 1
                                    self.error.append([i, word[:a], '标点符号错误'])
                                    return a
                            elif word[a] == 'e' and a <= 2:
                                while a < len(word) and word[a] != ' ' and word[a] not in operator:
                                    a += 1
                                self.error.append([i, word[:a], 'digit inputting error'])
                                return a
                            a += 1
                        else:
                            while a < len(word) and word[a] != ' ' and word[a] not in operator:
                                a += 1
                            self.error.append([i, word[:a], 'digit inputting error'])
                            return a
                    self.res.append([i, word[:a], 3])
                    return a
                # 如果不是小数点且之前也没有
                elif tmp1 == 0:
                    # 二进制判断
                    if word[a] == 'b' or word[a + 1] == 'B':
                        a += 1
                        while len(word) > a and (word[a] == '0' or word[a] == '1'):
                            a += 1
                        if a >= len(word) and word[a] == ' ' and word[a] in operator:
                            self.res.append([i, word[:a], 2])
                            return a
                        else:
                            while a < len(word) and word[a] != ' ' and word[a] not in operator:
                                a += 1
                            self.error.append([i, word[:a], 'digit inputting error'])
                            return a
                    # 十六进制判断
                    if word[a] == 'x' or word[a + 1] == 'X':
                        a += 1
                        while len(word) > a and (word[a].isdigit() or word[a] in hex):
                            a += 1
                        if a >= len(word) or word[a] == ' ' or word[a] in operator:
                            self.res.append([i, word[:a], 2])
                            return a
                        else:
                            while a < len(word) and word[a] != ' ' and word[a] not in operator:
                                a += 1
                            self.error.append([i, word[:a], 'digit inputting error'])
                            return a
                    # 八进制判断
                    if word[a] in Oct:
                        a += 1
                        while len(word) > a and word[a] in Oct:
                            a += 1
                        if a >= len(word) or word[a] == ' ' or word[a] in operator:
                            self.res.append([i, word[:a], 2])
                            return a
                        else:
                            while a < len(word) and word[a] != ' ' and word[a] not in operator:
                                a += 1
                            self.error.append([i, word[:a], 'digit inputting error'])
                            return a
                    else:
                        while a < len(word) and word[a] != ' ' and word[a] not in operator:
                            a += 1
                        self.error.append([i, word[:a], 'digit inputting error'])
                        return a
                # 如果是小数点但之前已经有过小数点
                elif word[a] == '.':
                    while a < len(word) and word[a] != ' ' and word[a] not in operator:
                        a += 1
                    self.error.append([i, word[:a], 'digit inputting error'])
                    return a
                else:
                    while a < len(word) and word[a] != ' ' and word[a] not in operator:
                        if word[a].isdigit():
                            a += 1
                        else:
                            while a < len(word) and word[a] != ' ' and word[a] not in operator:
                                a += 1
                            print(f"[数字输入错误：{word[:a]}]")
                            self.error.append([i, word[:a], 'digit inputting error'])
                            return a
                    self.res.append([i, word[:a], 103])
                    return a
            # 开头为非0数字
            else:
                while a < len(word) and word[a] != ' ' and word[a] not in operator:
                    if word[a] == 'e':
                        if tmp2 == 0:
                            tmp2 = 1
                            a += self.digit_judge(word[a:], i)
                            # print(self.res)
                        else:
                            while a < len(word) and word[a] != ' ' and word[a] not in operator:
                                a += 1
                            self.error.append([i, word[:a], 'digit inputting error'])
                            return a
                    elif word[a] == '.':
                        if tmp1 == 0 and a < len(word) - 1 and word[a + 1].isdigit():
                            a += 1
                            tmp1 = 1
                        else:
                            while a < len(word) and word[a] != ' ' and word[a] not in operator:
                                a += 1
                            self.error.append([i, word[:a], 'digit inputting error'])
                            return a
                    elif word[a].isdigit() and len(word) > a - 1:
                        a += 1
                    else:
                        while a < len(word) and word[a] != ' ':
                            a += 1
                        self.error.append([i, word[:a], 'digit inputting error'])
                        return a
                self.res.append([i, word[:a], 2])
                return a

    # 标识符正误判断
    def judge_Alpha(self, word, i):
        a = 0
        if len(word) == 1:
            # 单单一个‘_’的情况
            if word[a] == '_':
                self.error.append([i, word[:a], 'word inputting error'])
                return a + 1
            else:
                # 名称为一个字母的标识符:'a'
                self.res.append([i, word, 1])
                return a + 1
        else:
            # 判断下一位是什么
            a += 1
            # 如果后面接的是空格或操作符，就终态
            if word[a] in operator or word[a] == ' ':
                if word[a - 1] == '_':
                    print(f"[{i},{word[0]},标识符错误]")
                    self.error.append([i, word[0], 'word inputting error'])
                    return a
                else:
                    self.res.append([i, word[0], 1])
                    return a

            while a < len(word) and word[a] != ' ' and word[a] not in operator:
                if word[a].isalpha() or word[a] == '_' or word[a].isdigit():
                    a += 1
                else:
                    while a < len(word) and word[a] != ' ' and word[a] in operator:
                        a += 1
                    self.error.append([i, word[:a], '标识符错误'])
                    return a
            if word[:a] in keyword:
                self.res.append([i, word[:a], keyword[word[:a]]])
            else:
                if len(word[:a]) == 1:
                    self.res.append([i, word[:a], 1])
                else:
                    self.res.append([i, word[:a], 6])
            return a

    # 界符判断
    def judge_oprator(self, i, word):
        a = 1
        if len(word) == 1:
            if word[0] in operator:
                self.res.append([i, word[0], operator[word[0]]])
            else:
                self.error.append([i, word[0], '操作符错误'])
        else:
            # 判断注释
            if word[0] == '/':
                if word[1] == '/':
                    a = len(word)
                    return a
                elif word[1] == '*':
                    self.signal = 1
                    self.line = i
                    a = len(word)
                    return a
                else:
                    self.res.append([i, word[0], operator[word[0]]])
                    return a
            elif word[0] == '>' or word[0] == '<' or word[0] == '=' or word[0] == '!':
                if word[1] == '=':
                    self.res.append([i, word[:2], operator[word[:2]]])
                    a = 2
                    return a
                else:
                    self.res.append([i, word[0], operator[word[0]]])
                    return a
            elif word[0] == '|':
                if len(word) > 1:
                    if word[1] == '|':
                        self.res.append([i, word[:2], operator[word[:2]]])
                        a = 2
                        return a
                else:
                    self.res.append([i, word[0], operator[word[0]]])
                    return a
            elif word[0] == '&':
                if len(word) > 1:
                    if word[1] == '&':
                        self.res.append([i, word[:2], operator[word[:2]]])
                        a = 2
                        return a
                else:
                    self.res.append([i, word[0], operator[word[0]]])
                    return a
            elif word[0] == "'":
                while a < len(word) and word[a] != "'":
                    a += 1
                if a < len(word):
                    self.res.append([i, word[0], operator[word[0]]])
                    if len(word[1:a]) == 1:
                        self.res.append([i, word[1:a], 1])
                    else:
                        self.res.append([i, word[1:a], 6])
                    self.res.append([i, word[a], operator[word[a]]])
                    a += 1
                else:
                    self.error.append([i, word, "界符错误"])
            elif word[0] == '"':
                while a < len(word) and word[a] != '"':
                    # print(word[a])
                    a += 1
                if a < len(word):
                    self.res.append([i, word[0], operator[word[0]]])
                    if len(word[1:a]) == 1:
                        self.res.append([i, word[1:a], 1])
                    else:
                        self.res.append([i, word[1:a], 6])
                    self.res.append([i, word[a], operator[word[a]]])
                    a += 1
                else:
                    self.error.append([i, word, '标点符号错误'])
            else:
                if word[0] in operator:
                    if operator[word[0]] != 231:
                        self.res.append([i, word[0], operator[word[0]]])
                else:
                    self.error.append([i, word[0], '界符错误'])
        return a

    def token(self):
        # 将输入代码按行隔开
        words = self.words.split('\n')
        # 遍历每行代码
        for i in range(0, len(words)):
            # 一行一行读取
            num = 0  # current index
            word = words[i]
            # 如果之前已经有注释了，则进入下列判断
            if self.signal == 1:
                if len(word) >= 2:
                    if word[len(word) - 2] == '*' and word[len(word) - 1] == '/':
                        self.signal = 0
                        print(word)
                        print(f"[注释结束]")
                    # 如果多行注释不完全闭合，直接返回不再检查
                elif len(word) == 0:
                    print('')
                    self.res.append([i, '', "空行"])
                elif i >= len(words) - 1:
                    print(word)
            # 没有注释，则进行词法判断
            else:
                # 当num下标小于word长度时，就一位一位的判断
                while num < len(word):
                    # 把代码中间空格挖掉
                    if word[num] == ' ':
                        num += 1
                    # 标识符判断
                    elif word[num].isalpha() or word[num] == '_':
                        a = self.judge_Alpha(word[num:], i)
                        num += a
                    # 符号判断
                    elif word[num] in operator:
                        a = self.judge_oprator(i, word[num:])
                        num += a
                    # 数字的判断
                    elif word[num].isdigit():
                        a = self.isDigit(word[num:], i)
                        num += a
                    # 其他类型均算为错误
                    else:
                        a = num
                        while a < len(word) and word[a] != ' ' and word[a] not in operator:
                            a += 1
                        print(f"[{word[num:a]}, 非法字符]")
                        self.error.append([i, word[num:a], "非法字符"])
                        num = a
            for i in self.res:
                if i[2] == 231:
                    self.res.remove(i)
        return self.res, self.error


if __name__ == '__main__':
    f = open("tesst\\test0.1.txt", 'r', encoding='UTF-8-sig')
    words = f.read()
    a = lexer(words)
    res, error = a.token()
    for i in res:
        print(i)


