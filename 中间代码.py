from lexicalanalysis import lexer
import sys  # 导入sys模块

sys.setrecursionlimit(3000)  # 将默认的递归深度修改为3000


class IntermediateCode:
    def __init__(self, res):
        self.res = res
        self.token = []
        self.sentences = []
        self.begin_end = {}  # 所有文法集合
        self.b_e = {}
        self.un_end = []  # 非终结符
        self.end = []  # 终结符
        self.FIRST = {}  # first集
        self.FOLLOW = {}  # follow集
        self.first_1 = {}  # 候选式对应first集
        self.t = str  # 每次取出的token值
        self.count = 0  # 记录遍历位置
        self.gencode = []  # 存储四元式
        self.const_varible = []  # 存储变量和常量
        self.style = ''  # 用于存储变量或常量类型
        self.resu = []
        self.r = 0

    def getFirst(self, mem):
        for m in self.b_e[mem]:
            m = m.split(' ')
            # 产生式如A→ab，a→vt，或A→ε
            if m[0] not in self.un_end:
                self.FIRST[mem].append(m[0])
                self.first_1[mem + '→' + ' '.join(m)].append(m[0])
            else:
                # 产生式如A→Xb，将X的first集加进A中，如果X的first集为ε，则依次往下找
                lenth = 0
                while lenth < len(m):
                    if m[lenth] in self.un_end:
                        if len(self.FIRST[m[lenth]]) == 0:
                            self.getFirst(m[lenth])
                        self.FIRST[mem] += self.FIRST[m[lenth]]
                        t = self.FIRST[m[lenth]][:]
                        if 'ε' in self.FIRST[m[lenth]]:
                            t.remove('ε')
                            self.first_1[mem + '→' + ' '.join(m)] += t
                            lenth += 1
                            if lenth == len(m):
                                self.first_1[mem + '→' + ' '.join(m)].append('ε')
                        else:
                            self.first_1[mem + '→' + ' '.join(m)] += t
                            break
                    else:
                        break
            self.first_1[mem + '→' + ' '.join(m)] = list(set(self.first_1[mem + '→' + ' '.join(m)]))
        self.FIRST[mem] = list(set(self.FIRST[mem]))

    def initail(self, sentences):
        i = 0
        for str in sentences:
            part_begin = str.split("→")[0]
            part_end = str.split("→")[1]
            self.begin_end[part_begin] = part_end
            if i == 0:
                self.FOLLOW[part_begin] = ['#']
            else:
                self.FOLLOW[part_begin] = []
            self.FIRST[part_begin] = []
            i += 1
        for mem in self.FIRST:
            tmp = self.begin_end[mem].split('|')
            if mem not in self.b_e:
                self.b_e[mem] = tmp
            # self.getFirst(mem)
        self.un_end = list(self.b_e.keys())
        self.un_end.sort(key=list(self.b_e.keys()).index)
        self.first_1 = {i + '→' + ''.join(j): list() for i in self.un_end for j in self.b_e[i]}
        for mem in self.FIRST:
            for m in self.b_e[mem]:
                m = m.split(' ')
                for i in m:
                    if i not in self.un_end and i not in self.end:
                        self.end.append(i)
        for _ in range(2):
            for mem in self.FIRST:
                self.getFirst(mem)

    def getFollow(self, mem):
        for can in self.b_e[mem]:
            can = can.split(' ')
            # print(can)
            for i in range(len(can)):
                if can[i] in self.un_end:
                    # 产生式B->αAaβ，把a加入到Follow(A)中
                    if i + 1 < len(can) and can[i + 1] not in self.un_end:
                        self.FOLLOW[can[i]].append(can[i + 1])
                    # β->αA，Follow(B)加入到Follow(A)中
                    elif i + 1 == len(can):
                        self.FOLLOW[can[i]] += self.FOLLOW[mem]
                    # B->αAβ，把First(β)中的非$元素加入到Follow(A)中
                    elif can[i + 1] in self.un_end:
                        if 'ε' in self.b_e[can[i + 1]]:
                            # B--->$,Follow(B)加入到Follow(A)中
                            self.FOLLOW[can[i]] += self.FOLLOW[mem]
                            # print(self.FOLLOW[can[i + 1]])
                        temp = self.FIRST[can[i + 1]][:]
                        if 'ε' in temp:
                            temp.remove('ε')
                        self.FOLLOW[can[i]] += temp
                    self.FOLLOW[can[i]] = list(set(self.FOLLOW[can[i]]))

    # 得到每次的 token 值
    def GetNextToken(self):
        self.t = self.token[self.count]
        self.count += 1
        # print(self.sentences[self.count-1])

    # token匹配
    def match(self, x):
        if x == self.t:
            self.GetNextToken()
        else:
            print('匹配', x, '错误！')
        if len(self.t) == 0:
            print('program未写完！！！')

    # 出口回溯
    def exit(self, s):
        for i in range(len(self.gencode) - 1, -1, -1):
            if s in self.gencode[i]:
                if type(self.gencode[i][3]) == str and len(self.gencode[i][3]) == 0:
                    temp = self.gencode.pop(i)
                    temp.pop()
                    temp.append(len(self.gencode) + 2)
                    self.gencode.insert(i, temp)
                    break

    # 函数定义形参列表→函数定义形参|ε
    def hanshudingyixingcanliebiao(self):
        if self.t in self.first_1['函数定义形参列表→函数定义形参']:
            self.hanshudingyixingcan()
        elif self.t in self.FOLLOW['函数定义形参列表']:
            pass
        else:
            print('匹配函数定义形参列表错误！！')

    # 函数定义→常量类型 变量 201 函数定义形参列表 202 221 语句表 222|107 变量 201 函数定义形参列表 202 221 DD 222
    def hanshudingyi(self):
        if self.t in self.first_1['函数定义→常量类型 变量 201 函数定义形参列表 202 221 语句表 222']:
            self.changliangleixing()
            self.bianliang()
            self.match('201')
            self.hanshushengmingxingcanliebiao()
            self.match('202')
            self.match('221')
            self.yujubiao()
            self.match('222')
        elif self.t in self.first_1['函数定义→107 变量 201 函数定义形参列表 202 221 DD 222']:
            self.match('107')
            self.bianliang()
            self.match('201')
            self.hanshudingyixingcanliebiao()
            self.match('202')
            self.match('221')
            self.DD()
            self.match('222')
        else:
            print('匹配函数定义错误！！')

    # block→函数定义 block|ε
    def hanshukuai(self):
        if self.t in self.first_1['block→函数定义 block']:
            self.hanshudingyi()
            self.hanshukuai()
        elif self.t in self.FOLLOW['block']:
            pass
        else:
            # print(self.sentences[self.count - 1])
            print('匹配block错误！！')

    # 算数表达式→项 A
    def suanshubiaodashi(self):
        if self.t in self.first_1['算数表达式→项 A']:
            self.xiang()
            self.A()
        else:
            # print(self.sentences[self.count-1])
            print('匹配算数表达式错误！！')

    # 因子→201 算数表达式 202|常量|变量 G
    def yinzi(self):
        if self.t == '201':
            self.match('201')
            self.suanshubiaodashi()
            self.match('202')
            self.gencode.append(['=', len(self.gencode) + 1, '', str(len(self.gencode) + 2)])
        elif self.t in self.first_1['因子→常量']:
            self.changliang()
        elif self.t in self.first_1['因子→变量 G']:
            self.bianliang()
            self.G()
        else:
            print('匹配因子错误！！')

    # 项→因子 B
    def xiang(self):
        if self.t in self.first_1['项→因子 B']:
            self.yinzi()
            self.B()
        else:
            print('匹配项错误！！')

    # 关系运算符→211|212|213|214|215|216
    def guanxiyunsuanfu(self):
        if self.t == '211':
            self.match('211')
        elif self.t == '212':
            self.match('212')
        elif self.t == '213':
            self.match('213')
        elif self.t == '214':
            self.match('214')
        elif self.t == '215':
            self.match('215')
        elif self.t == '216':
            self.match('216')
        else:
            print('匹配关系运算符错误！！')

    # 单变量声明→变量 U
    def danbianliangshengming(self):
        if self.t in self.first_1['单变量声明→变量 U']:
            self.bianliang()
            self.const_varible.append([self.style, self.sentences[self.count - 2], '变量'])
            self.U()
        else:
            print('匹配单变量声明错误！！')

    # 变量声明表→单变量声明 Q
    def bianliangshengmingbiao(self):
        if self.t in self.first_1['变量声明表→单变量声明 Q']:
            self.danbianliangshengming()
            self.Q()
        else:
            print('匹配变量声明表错误！！')

    # 函数声明形参→变量类型 V
    def hanshushengmingxingcan(self):
        if self.t in self.first_1['函数声明形参→变量类型 V']:
            self.changliangleixing()
            self.V()
        else:
            print('匹配函数声明形参错误！！')

    # 实参→表达式 K
    def shican(self):
        if self.t in self.first_1['实参→表达式 K']:
            self.biaodashi()
            self.K()
        else:
            print('匹配实参错误！！')

    # 实参列表→实参|ε
    def shicanliebiao(self):
        if self.t in self.first_1['实参列表→实参']:
            self.shican()
        elif self.t in self.FOLLOW['实参列表']:
            pass
        else:
            # print(self.sentences[self.count - 1])
            print('匹配实参列表错误！！')

    # return语句→106 CC
    def returnyuju(self):
        if self.t == '106':
            self.match('106')
            self.CC()
        else:
            print('匹配return语句错误！！')

    # 语句表→105 常量类型 常量声明表 definexpr X|变量类型 N definexpr X|107 变量 201 函数声明形参列表 202 223 definexpr X|变量 W X|Y X|221 语句表 222 X|ε
    def yujubiao(self):
        if self.t == '105':
            self.match('105')
            self.changliangleixing()
            self.changliangshengmingbiao()
            self.shengmingyuju()
            self.X()
        elif self.t in self.first_1['语句表→变量类型 N definexpr X']:
            self.changliangleixing()
            self.N()
            self.shengmingyuju()
            self.X()
        elif self.t in self.first_1['语句表→107 变量 201 函数声明形参列表 202 223 definexpr X']:
            self.match('107')
            self.bianliang()
            self.match('201')
            self.hanshushengmingxingcanliebiao()
            self.match('202')
            self.match('223')
            self.shengmingyuju()
            self.X()
        elif self.t in self.first_1['语句表→变量 W X']:
            self.bianliang()
            self.W()
            self.X()
        elif self.t in self.first_1['语句表→Y X']:
            self.Y()
            self.X()
        elif self.t in self.first_1['语句表→221 语句表 222 X']:
            self.match('221')
            self.yujubiao()
            self.match('222')
            self.X()
        elif self.t in self.FOLLOW['语句表']:
            pass
        else:
            print('匹配语句表错误！！')

    # 复合语句→221 语句表 222
    def fuheyuju(self):
        if self.t == '221':
            self.match('221')
            self.yujubiao()
            self.match('222')
        else:
            print('匹配复合语句错误！！')

    # 循环语句表→循环语句 AA
    def xunhuanyujubiao(self):
        if self.t in self.first_1['循环语句表→循环语句 AA']:
            self.xunhuanyuju()
            self.AA()
        else:
            print('匹配循环语句表错误！！')

    # loopcomplex→221 循环语句表 222
    def xunhuanyongfuheyuju(self):
        if self.t == '221':
            self.match('221')
            self.xunhuanyujubiao()
            self.match('222')
        else:
            print('匹配loopcomplex错误！！')

    # do-while语句→109 loopcomplex 110 201 表达式 202 223
    def dowhileyuju(self):
        if self.t == '109':
            self.match('109')
            num = len(self.gencode)
            self.xunhuanyongfuheyuju()
            self.match('110')
            self.match('201')
            self.biaodashi()
            self.match('202')
            self.match('223')
            temp = self.gencode.pop()
            temp.pop()
            temp.append(num + 1)
            self.gencode.append(temp)
            self.gencode.append(['do-while', '', '', len(self.gencode) + 2])
        else:
            print('匹配do-while语句错误！！')

    # while语句→110 201 表达式 202 循环语句
    def whileyuju(self):
        if self.t == '110':
            self.match('110')
            self.match('201')
            num = len(self.gencode)
            self.biaodashi()
            temp = self.gencode.pop()
            temp.pop()
            temp.append(len(self.gencode) + 3)
            self.gencode.append(temp)
            self.gencode.append(['while', '', '', ''])
            self.match('202')
            self.xunhuanyuju()
            self.gencode.append(['', '', '', ''])
            temp = self.gencode.pop()
            temp.pop()
            temp.append(num + 1)
            self.gencode.append(temp)
            self.exit('while')
        else:
            print('匹配while语句错误！！')

    # 循环语句→语句
    def xunhuanyuju(self):
        if self.t in self.first_1['循环语句→语句']:
            self.yuju()
        else:
            print('匹配循环语句错误！！')

    # for语句→113 201 表达式 223 表达式 223 表达式 202 循环语句
    def foryuju(self):
        if self.t == '113':
            self.match('113')
            self.match('201')
            self.biaodashi()
            self.match('223')
            # 记录当前布尔表达式的位置，i++ 执行完要跳转到这里
            num = len(self.gencode)
            self.biaodashi()
            # [<=, i, N, '12']
            # ['for', '', '', '']
            # []
            # []
            temp = self.gencode.pop()
            temp.pop()
            # temp.append(len(self.gencode) + 3)
            temp.append(len(self.gencode) + 6)
            self.gencode.append(temp)
            # 错误出口
            self.gencode.append(['for', '', '', ''])
            self.match('223')
            self.biaodashi()
            self.match('202') # 加一个四元式，让 x = x + 1 执行后跳转到判断语句
            self.gencode.append(['', '', '', num + 1])
            self.xunhuanyuju()
            if temp[3] == '':
                temp.pop()
                temp.append(num + 1)
                self.gencode.append(temp)
            else:
                self.gencode.append(['', '', '', num + 3]) # temp.pop() temp.append(num + 3)  self.gencode.append(temp)
            self.exit('for')
        else:
            print('匹配for语句失败！！')

    # 语句→definexpr|执行语句
    def yuju(self):
        if self.t in self.first_1['语句→definexpr']:
            self.shengmingyuju()
        elif self.t in self.first_1['语句→执行语句']:
            self.zhixingyuju()
        else:
            print('匹配语句失败！！')

    # if语句→111 201 表达式 202 语句 Z
    def ifyuju(self):
        if self.t == '111':
            self.match('111')
            self.match('201')
            self.biaodashi()
            temp = self.gencode.pop()
            temp.pop()
            temp.append(len(self.gencode) + 3)
            self.gencode.append(temp)
            self.gencode.append(['if', '', '', ''])
            self.match('202')
            self.yuju()
            self.Z()

    # 控制语句→if语句|for语句|while语句|do-while语句
    def kongzhiyuju(self):
        if self.t in self.first_1['控制语句→if语句']:
            self.ifyuju()
        elif self.t in self.first_1['控制语句→for语句']:
            self.foryuju()
        elif self.t in self.first_1['控制语句→while语句']:
            self.whileyuju()
        elif self.t in self.first_1['控制语句→do-while语句']:
            self.dowhileyuju()
        else:
            print('匹配数据处理语句错误！！')

    # 数据处理语句→变量 W
    def shujuchuliyuju(self):
        if self.t in self.first_1['数据处理语句→变量 W']:
            self.bianliang()
            self.W()
        else:
            print('匹配数据处理语句错误！！')

    # 执行语句→数据处理语句|控制语句|复合语句
    def zhixingyuju(self):
        if self.t in self.first_1['执行语句→数据处理语句']:
            self.shujuchuliyuju()
        elif self.t in self.first_1['执行语句→控制语句']:
            self.kongzhiyuju()
        elif self.t in self.first_1['执行语句→复合语句']:
            self.fuheyuju()

    # 常量声明表→常量 219 S
    def changliangshengmingbiao(self):
        if self.t in self.first_1['常量声明表→常量 219 S']:
            self.bianliang()
            self.const_varible.append([self.style, self.sentences[self.count - 2], '常量'])
            if self.sentences[self.count] == "'" or self.sentences[self.count] == '"':
                self.gencode.append(['=', self.sentences[self.count + 1], '', self.sentences[self.count - 2]])
            else:
                self.gencode.append(['=', self.sentences[self.count], '', self.sentences[self.count - 2]])
            self.match('219')
            self.S()
        else:
            print('匹配常量声明表错误！！')

    # 函数定义形参→变量类型 变量 FF
    def hanshudingyixingcan(self):
        if self.t in self.first_1['函数定义形参→变量类型 变量 FF']:
            self.changliangleixing()
            self.bianliang()
            self.FF()
        else:
            print('匹配函数定义形参错误！！')

    # FF→224 函数定义形参|ε
    def FF(self):
        if self.t == '224':
            self.match('224')
            self.hanshudingyixingcan()
        elif self.t in self.FOLLOW['FF']:
            pass
        else:
            print('匹配FF错误！！')

    # EE→DD|ε
    def EE(self):
        if self.t in self.first_1['EE→DD']:
            self.DD()
        elif self.t in self.FOLLOW['EE']:
            pass
        else:
            print('匹配EE错误！！')

    # DD→变量类型 N definexpr EE
    def DD_candidate_2(self):
        self.changliangleixing()
        self.N()
        self.shengmingyuju()
        self.EE()

    # DD→107 变量 201 函数声明形参列表 202 223 definexpr EE
    def DD_candidate_3(self):
        self.match('107')
        self.bianliang()
        self.match('201')
        self.hanshushengmingxingcanliebiao()
        self.match('202')
        self.match('223')
        self.shengmingyuju()
        self.EE()

    # DD→105 常量类型 常量声明表 definexpr EE
    def DD_candidate_1(self):
        self.match('105')
        self.changliangleixing()
        self.changliangshengmingbiao()
        self.shengmingyuju()
        self.EE()

    # DD→105 常量类型 常量声明表 definexpr EE|变量类型 N definexpr EE|107 变量 201 函数声明形参列表 202 223 definexpr EE|执行语句 EE|ε
    def DD(self):
        if self.t == '105':
            self.DD_candidate_1()
        elif self.t in self.first_1['DD→变量类型 N definexpr EE']:
            self.DD_candidate_2()
        elif self.t == '107':
            self.DD_candidate_3()
        elif self.t in self.first_1['DD→执行语句 EE']:
            self.zhixingyuju()
            self.EE()
        elif self.t in self.FOLLOW['DD']:
            pass
        else:
            print('匹配DD错误！！')

    # CC→223|表达式 223
    def CC(self):
        if self.t == '223':
            self.match('223')
        elif self.t in self.first_1['CC→表达式 223']:
            self.biaodashi()
            self.match('223')
        else:
            print('匹配CC失败！！')

    # BB→112 循环语句|ε
    def BB(self):
        if self.t == '112':
            self.match('112')
            self.xunhuanyuju()
        elif self.t in self.FOLLOW['BB']:
            pass
        else:
            print('匹配BB失败！！')

    # AA→循环语句表|ε
    def AA(self):
        if self.t in self.first_1['AA→循环语句表']:
            self.xunhuanyujubiao()
        elif self.t in self.FOLLOW['AA']:
            pass
        else:
            print('匹配AA失败！！')

    # Z→112 语句|ε
    def Z(self):
        if self.t == '112':
            self.gencode.append(['else', '', '', ''])
            self.exit('if')
            self.match('112')
            self.yuju()
            self.exit('else')
        elif self.t in self.FOLLOW['Z']:
            self.exit('if')
            pass
        else:
            print('匹配Z失败！！')

    # Y→控制语句|return语句
    def Y(self):
        if self.t in self.first_1['Y→控制语句']:
            self.kongzhiyuju()
        elif self.t in self.first_1['Y→return语句']:
            self.returnyuju()
        else:
            print('匹配Y失败！！')

    # X→语句表|ε
    def X(self):
        if self.t in self.first_1['X→语句表']:
            self.yujubiao()
        elif self.t in self.FOLLOW['X']:
            pass
        else:
            print('匹配X失败！！')

    # W→219 表达式 223|201 实参列表 202 223
    def W(self):
        bl = self.sentences[self.count - 2]
        num = self.count
        if self.t == '219':
            self.match('219')
            num1 = self.count
            self.biaodashi()
            num2 = self.count
            if num2 - num1 == 1:
                self.gencode.append(['=', self.sentences[self.count - 2], '', bl])
            else:
                s = ''
                for i in range(num1 - 1, num2 - 1):
                    s += self.sentences[i]
                self.gencode.append(['=', s, '', bl])
            self.match('223')
        elif self.t == '201':
            self.match('201')
            self.shicanliebiao()
            if self.sentences[num] == ')':
                self.gencode.append([bl, '', '', ''])
            else:
                s = ''
                for i in range(num, self.count - 1):
                    s += self.sentences[i]
                self.gencode.append([bl, '', s, ''])
            self.match('202')
            self.match('223')

    # V→224 函数声明形参|ε
    def V(self):
        if self.t == '224':
            self.match('224')
            self.hanshushengmingxingcan()
        elif self.t in self.FOLLOW['V']:
            pass
        else:
            print('匹配V错误！！')

    # U→219 表达式|ε
    def U(self):
        if self.t == '219':
            bl = self.sentences[self.count - 2]
            self.match('219')
            self.biaodashi()
            # self.gencode.append(['=', len(self.gencode) + 1, '', bl])
            self.gencode.append(['=', self.sentences[self.count - 2], '', bl])
        elif self.t in self.FOLLOW['U']:
            pass
        else:
            print('匹配U错误！！')

    # T→223|224 常量声明表
    def T(self):
        if self.t == '223':
            self.match('223')
        elif self.t == '224':
            self.match('224')
            self.changliangshengmingbiao()
        else:
            print('匹配T错误！！')

    # S→常量 T
    def S(self):
        if self.t in self.first_1['S→常量 T']:
            self.changliang()
            self.T()
        else:
            print('匹配S错误！！')

    # R→常量|表达式
    def R(self):
        if self.t in self.first_1['R→常量']:
            self.changliang()
        elif self.t in self.first_1['R→表达式']:
            self.biaodashi()
        else:
            # print(self.sentences[self.count-1])
            print('匹配R错误！！')

    # Q→223|224 变量声明表
    def Q(self):
        if self.t == '223':
            self.match('223')
        elif self.t == '224':
            self.match('224')
            self.bianliangshengmingbiao()
        else:
            print('匹配Q错误！！')

    # K→224 实参|ε
    def K(self):
        if self.t == '224':
            self.match('224')
            self.shican()
        elif self.t in self.FOLLOW['K']:
            pass
        else:
            print('匹配K失败！！')

    # H→E F|ε
    def H(self):
        if self.t in self.first_1['H→E F']:
            self.E()
            self.F()
        elif self.t in self.FOLLOW['H']:
            pass
        else:
            print('匹配H失败！！')

    # G→201 实参列表 202|ε
    def G(self): # 看看变量后面跟的是不是()，如果是就是调用的函数
        bl = self.sentences[self.count - 2]
        num = self.count
        if self.t == '201':
            self.match('201')
            self.shicanliebiao()
            if self.sentences[self.count] != ')':
                string = ''
                for i in range(num, self.count - 1):
                    string += self.sentences[i]
                self.gencode.append([bl, '', string, ''])
            else:
                self.gencode.append([bl, '', '', ''])
            self.match('202')
        elif self.t in self.FOLLOW['G']:
            pass
        else:
            print('匹配G失败！！')

    # D→219 表达式
    def D_candidate_2(self):
        bl = self.sentences[self.count - 2]
        self.match('219')
        num1 = self.count
        self.biaodashi()
        num2 = self.count
        if num2 - num1 == 1:
            self.gencode.append(['=', self.sentences[self.count - 2], '', bl])
        else:
            s = ''
            for i in range(num1 - 1, num2 - 1):
                s += self.sentences[i]
            self.gencode.append(['=', s, '', bl])

    # D→G B A C
    def D_candidate_1(self):
        self.G() # 看看变量后面跟的是不是()，如果是就是调用的函数
        self.B() # * / %
        self.A() # + -
        self.C() # >=  >  <=  <

    # D→G B A C|219 表达式
    def D(self):
        if self.t in self.first_1['D→G B A C']: # >、<、>=、+、-、*、/、(
            self.D_candidate_1()
        elif self.t == '219': # =
            self.D_candidate_2()
        elif self.t in self.FOLLOW['D']:
            pass
        else:
            print('匹配D失败！！')

    # C→218 布尔表达式
    def C_candidate_3(self):
        self.match('218')
        self.gencode.append(
            [self.sentences[self.count - 2], self.sentences[self.count - 3], self.sentences[self.count - 1],
             self.sentences[self.count - 3] + '||' + self.sentences[self.count - 1]])
        self.buerbiaodashi()

    # C→217 布尔项 F
    def C_candidate_2(self):
        self.gencode.append([self.sentences[self.count - 1], self.sentences[self.count - 2], self.sentences[self.count],
                             self.sentences[self.count - 2] + '&&' + self.sentences[self.count]])
        self.match('217')
        self.buerxiang()
        self.F()

    # C→关系运算符 项 A H
    def C_candidate_1(self):
        num1 = self.count - 2
        self.guanxiyunsuanfu()
        num2 = self.count - 2
        s = ''
        for i in range(num1, num2):
            s += self.sentences[i]
        if self.resu:
            s = self.resu[0]
            self.resu = None
            # print(self.resu)
        self.gencode.append([self.sentences[self.count - 2], s, self.sentences[self.count - 1],
                             s + self.sentences[self.count - 2] + self.sentences[self.count - 1]])
        self.xiang()
        self.A()
        self.H()

    # C→关系运算符 项 A H|217 布尔项 F|218 布尔表达式|ε
    def C(self): # >=  >  <=  <
        if self.t in self.first_1['C→关系运算符 项 A H']:
            self.C_candidate_1()
        elif self.t == '217': # &&
            self.C_candidate_2()
        elif self.t == '218': # ||
            self.C_candidate_3()
        elif self.t in self.FOLLOW['C']:
            pass
        else:
            print('匹配C失败！！')

    # B→206 项|207 项|208 项|ε
    def B(self): # * / %
        tmp = self.sentences[self.count - 2]
        s = ''
        if self.t == '206':  # *
            self.match('206')
            num1 = self.count - 1
            self.xiang()
            num2 = self.count - 1
            for i in range(num1, num2):
                s += self.sentences[i]
            result = tmp + '*' + s
            self.resu.append(result)
            self.r = self.r + 1
            self.gencode.append(['*', s, tmp, result])
        elif self.t == '207':  # /
            self.match('207')
            num1 = self.count - 1
            self.xiang()
            num2 = self.count - 1
            for i in range(num1, num2):
                s += self.sentences[i]
            result = tmp + '/' + s
            self.resu.append(result)
            self.r = self.r + 1
            self.gencode.append(['/', s, tmp, result])
        elif self.t == '208':  # %
            self.match('208')
            num1 = self.count - 1
            self.xiang()
            num2 = self.count - 1
            for i in range(num1, num2):
                s += self.sentences[i]
            result = tmp + '%' + s
            self.resu.append(result)
            self.r = self.r + 1
            self.gencode.append(['%', s, tmp, result])
        elif self.t in self.FOLLOW['B']:
            pass
        else:
            print('匹配B失败！！')

    # A→209 算数表达式|210 算数表达式|ε
    def A(self): # + -
        tmp = self.sentences[self.count - 2]
        s = ''
        if self.t == '209':  # +
            self.match('209')
            num1 = self.count - 1
            self.suanshubiaodashi()
            num2 = self.count - 1
            for i in range(num1, num2):
                s += self.sentences[i]
                if self.r >= 2:
                    tmp = self.resu[self.r - 2]
                    self.r = self.r - 1
            self.gencode.append(['+', s, tmp, tmp + '+' + s])
        elif self.t == '210':  # -
            self.match('210')
            num1 = self.count - 1
            self.suanshubiaodashi()
            num2 = self.count - 1
            for i in range(num1, num2):
                s += self.sentences[i]
            if self.r >= 2:
                tmp = self.resu[self.r - 2]
                self.r = self.r - 1
            self.gencode.append(['-', s, tmp, tmp + '-' + s])
        elif self.t in self.FOLLOW['A']:
            pass
        else:
            print('匹配A失败！！')

    # 表达式→205! 布尔表达式 E F
    def biaodashi_candidate_4(self):
        self.match('205')
        self.gencode.append(['!', '', self.sentences[self.count - 1], len(self.gencode) + 2])
        self.buerbiaodashi()
        self.E()
        self.F()

    # 表达式→变量 D
    def biaodashi_candidate_3(self):
        self.bianliang()
        self.D()

    # 表达式→常量 B A C
    def biaodashi_candidate_2(self):
        self.changliang()
        self.B()
        self.A()
        self.C()

    # 表达式→201 算数表达式 202 B A C
    def biaodashi_candidate_1(self):
        self.match('201')
        self.suanshubiaodashi()
        self.match('202')
        self.B()
        self.A()
        self.C()

    # 表达式→201( 算数表达式 )202 B A C|常量 B A C|变量 D|205! 布尔表达式 E F
    def biaodashi(self):
        if self.t == '201':
            self.biaodashi_candidate_1()
        elif self.t in self.first_1['表达式→常量 B A C']: # 常量
            self.biaodashi_candidate_2()
        elif self.t in self.first_1['表达式→变量 D']:
            self.biaodashi_candidate_3()
        elif self.t == '205':
            self.biaodashi_candidate_4()
        else:
            print('表达式匹配错误！！')

    # 布尔因子→表达式
    def bueryinzi(self): # 表达式不带 =，布尔表达式类似于  a != 1 、 a < 10
        if self.t in self.first_1['布尔因子→表达式']:
            self.biaodashi()
        else:
            print('匹配布尔因子错误！！')

    # 布尔项→布尔因子 E
    def buerxiang(self):
        if self.t in self.first_1['布尔项→布尔因子 E']:
            self.bueryinzi()
            self.E()
        else:
            print('匹配布尔项错误！！')

    # 布尔表达式→布尔项 F
    def buerbiaodashi(self):
        if self.t in self.first_1['布尔表达式→布尔项 F']:
            self.buerxiang()
            self.F()
        else:
            print('匹配布尔表达式错误！！')

    # F→218 布尔表达式|ε ||
    def F(self):
        if self.t == '218':
            self.match('218')
            temp = self.gencode.pop()
            temp.pop()
            temp.append(len(self.gencode) + 3)
            self.gencode.append(temp)
            self.gencode.append(['', '', '', ''])
            temp = self.gencode.pop()
            temp.pop()
            temp.append(len(self.gencode) + 3)
            self.gencode.append(temp)
            i = len(self.gencode)
            self.buerbiaodashi()
            self.gencode.append(['', '', '', ''])
            temp = self.gencode.pop()
            temp.pop()
            temp.append(len(self.gencode) + 3)
            self.gencode.insert(i, temp)

        elif self.t in self.FOLLOW['F']:
            pass
        else:
            print('匹配F失败！！')

    # E→217 布尔表达式|ε &&
    def E(self):
        if self.t == '217':
            self.match('217')
            temp = self.gencode.pop()
            temp.pop()
            temp.append(len(self.gencode) + 4)
            self.gencode.append(temp)
            i = len(self.gencode)
            self.buerbiaodashi()
            self.gencode.append(['', '', '', ''])
            temp = self.gencode.pop()
            temp.pop()
            temp.append(len(self.gencode) + 3)
            self.gencode.insert(i, temp)

        elif self.t in self.FOLLOW['E']:
            pass
        else:
            print('匹配E失败！！')

    # J→1 225|6 225
    def J(self):
        if self.t == '1':
            self.match('1')
            self.match('225')
        elif self.t == '6':
            self.match('6')
            self.match('225')

    # I→1 227|6 227
    def I(self):
        if self.t == '1':
            self.match('1')
            self.match('227')
        elif self.t == '6':
            self.match('6')
            self.match('227')

    # 常量→3|2|227 I|225 J
    def changliang(self):
        if self.t == '3':
            self.match('3')
        elif self.t == '2':
            self.match('2')
        elif self.t == '227':
            self.I()
        elif self.t == '225':
            self.J()

    # P→219 R|ε
    def P(self):
        if self.t in self.first_1['P→219 R']:
            if self.sentences[self.count] == "'" or self.sentences[self.count] == '"':
                self.gencode.append(['=', self.sentences[self.count + 1], '', self.sentences[self.count - 2]])
            else:
                self.gencode.append(['=', self.sentences[self.count], '', self.sentences[self.count - 2]])
            self.match('219')
            self.R()
        elif self.t in self.FOLLOW['P']:
            pass
        else:
            print('匹配P错误！！')

    # O→201 函数声明形参列表 202 223
    def O_candidate_2(self):
        bl = self.sentences[self.count - 2]
        num = self.count
        # self.const_varible.append([self.style, self.sentences[self.count - 2], '函数'])
        self.match('201')
        self.hanshushengmingxingcanliebiao()
        if self.sentences[num] == ')':
            self.const_varible.append([self.style, bl, '', '函数'])
        else:
            string = ''
            for i in range(num, self.count - 1):
                string += self.sentences[i]
            self.const_varible.append([self.style, bl, string, '函数'])
        self.match('202')
        self.match('223')

    # O→P Q
    def O_candidate_1(self):
        self.P()
        self.Q()

    # O→P Q|201 函数声明形参列表 202 223
    def O(self):
        if self.t in self.first_1['O→P Q']:
            self.const_varible.append([self.style, self.sentences[self.count - 2], '变量'])
            self.O_candidate_1()
        elif self.t in self.first_1['O→201 函数声明形参列表 202 223']:
            self.O_candidate_2()
        elif self.t in self.FOLLOW['O'] and 'ε' in self.FIRST['0']:
            self.Q()
        else:
            print('匹配O错误！！')

    # N→变量 O
    def N_candidate(self):
        self.bianliang()
        self.O()

    # N→变量 O
    def N(self):
        if self.t in self.first_1['N→变量 O']:
            self.N_candidate()
        else:
            print('匹配N错误！！！')

    # 变量类型|常量类型→101|102|103
    def changliangleixing(self):
        if self.t == '101':
            self.match('101')
            self.style = 'char'
        elif self.t == '102':
            self.match('102')
            self.style = 'int'
        elif self.t == '103':
            self.match('103')
            self.style = 'float'
        else:
            print('匹配常量类型错误！！！')

    # 函数声明形参列表→函数声明形参|ε
    def hanshushengmingxingcanliebiao(self):
        bl = self.sentences[self.count - 3]
        num = self.count - 1
        if self.t in self.first_1['函数声明形参列表→函数声明形参']:
            self.hanshushengmingxingcan()
            temp = ''
            for i in range(num, self.count - 1):
                temp += self.sentences[i]
            self.gencode.append([bl, '', temp, len(self.gencode) + 1])
        elif self.t in self.FIRST['函数声明形参列表']:
            self.gencode.append([bl, '', '', len(self.gencode) + 1])
        else:
            print('匹配函数声明形参列表错误！！！')

    # 变量→1|6
    def bianliang(self): # 匹配一个变量
        if self.t == '1':
            self.match('1')
        elif self.t == '6':
            self.match('6')
        else:
            print('匹配变量错误！！')

    # definexpr→107 变量 201 函数声明形参列表 202 223 definexpr
    def shengmingyuju_candidate_3(self):
        self.match('107')
        self.bianliang()
        self.match('201')
        self.hanshushengmingxingcanliebiao()
        self.match('202')
        self.match('223')
        self.shengmingyuju()

    # definexpr→变量类型 N definexpr
    def shengmingyuju_candidate_2(self):
        self.changliangleixing()
        self.N()
        self.shengmingyuju()

    # definexpr→105 常量类型 常量声明表 definexpr
    def shengmingyuju_candidate_1(self):
        self.match('105')
        self.changliangleixing()
        self.changliangshengmingbiao()
        self.shengmingyuju()

    # definexpr→105 常量类型 常量声明表 definexpr|变量类型 N definexpr|107 变量 201 函数声明形参列表 202 223 definexpr|ε
    def shengmingyuju(self):
        if self.t == '105': # const
            self.shengmingyuju_candidate_1()
        elif self.t in self.first_1['definexpr→变量类型 N definexpr']:
            self.shengmingyuju_candidate_2()
        elif self.t == '107': # void 函数声明
            self.shengmingyuju_candidate_3()
        elif 'ε' in self.FIRST['definexpr'] and self.t in self.FOLLOW['definexpr']:
            pass
        else:
            print('匹配definexpr错误！！')

    # program→definexpr 127 201 202 复合语句 block
    def chengxu_candidate_1(self):
        self.shengmingyuju()
        self.match('127')
        self.gencode.append(['main', '', '', ''])
        self.match('201')
        self.match('202')
        self.fuheyuju()
        self.gencode.append(['sys', '', '', ''])
        self.hanshukuai()

    # program→127 201 202 复合语句 block
    def chengxu_candidate_2(self):
        self.match('127')
        self.gencode.append(['main', '', '', ''])
        self.match('201')
        self.match('202')
        self.fuheyuju()
        self.gencode.append(['sys', '', '', ''])
        self.hanshukuai()

    # 递归下降
    def recursive_descent(self, start):
        if self.t in self.first_1[start + '→' + 'definexpr 127 201 202 复合语句 block']:
            self.chengxu_candidate_1()
        elif self.t == '127':
            self.chengxu_candidate_2()
        else:
            # print(self.sentences[self.count-1])
            print('error from program')

    def main0(self):
        for mem in self.res:
            self.token.append(str(mem[2]))
            self.sentences.append(mem[1])
        self.token.append('#')
        self.sentences.append('#')
        file = open('文法.txt', 'r', encoding='utf-8')
        s = file.read()
        sentences = s.split('\n')
        self.initail(sentences)
        for _ in range(2):
            for key in self.b_e:
                self.getFollow(key)
        jud = 1
        if jud:
            # 递归下降
            start = 'program'
            self.GetNextToken()
            self.recursive_descent(start)
            c = 0
            for i in self.gencode:
                c = c + 1
                # print(f"{c}: {i}")
            # print(self.const_varible)
            return self.gencode, self.const_varible


if __name__ == '__main__':
    # f = open("./test/test1.5-1.txt", 'r', encoding='UTF-8-sig')
    f = open("tesst/test0.3.txt", 'r', encoding='UTF-8-sig')
    # f = open("./tesst/test4.1-2.txt", 'r', encoding='gb18030')
    words = f.read()
    a = lexer(words)
    res, error = a.token()
    n = IntermediateCode(res)
    n.main0()
    print(n.res)
    print(n.gencode)
