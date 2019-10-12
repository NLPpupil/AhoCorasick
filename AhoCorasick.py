# v_1.2
from collections import namedtuple
import json
from collections import defaultdict

Match = namedtuple('Match','begin end keyword value')
class AhoCorasick:
    def __init__(self,keywords):
        """初始化

        keywords -- 一个关键词-值的字典。或字典文件，keyword和value以tab分开，一行一对
        """
        if type(keywords) is str:
            key_values = dict()
            with open(keywords) as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    fields = line.strip().split('\t')
                    length = len(fields)
                    if length == 2:
                        key_values[fields[0]] = fields[1]
                    elif length ==1:
                        key_values[fields[0]] = None
            keywords = key_values

        self.keywords = keywords
        self.goto_table = defaultdict(dict)
        self.output_table = dict()
        self.failure = dict()
        self.build()

    def construct_goto(self):
        """构建goto函数，同时部分构建output函数
        """
        new_state = 0
        def enter(kw):
            """insert into the goto_table graph a path that spells out kw
            """
            state, j = 0, 0
            nonlocal new_state

            # 如果之前已经有部分路径，先按照这个路径往下走
            if state in self.goto_table:
                for a in kw:
                    if a in self.goto_table[state]:
                        state = self.goto_table[state][a]
                        j += 1
                    else:
                        break

            # 无路可走后，开辟新路径
            for a in kw[j:]:
                new_state = new_state + 1
                self.goto_table[state][a] = new_state
                state = new_state

            # 终点状态添加kw
            self.output_table[state] = {kw}


        # 逐个在goto_table图上插入kw
        for kw in self.keywords:
            enter(kw)

        # 对于初始状态设置指向自身的转移
        alphabet = set(''.join(self.keywords))
        for a in alphabet:
            if a not in self.goto_table[0]:
                self.goto_table[0][a] = 0



    def construct_failure(self):
        """构建failure函数，同时完成output函数
        """
        
        queue = [] #append相当是enqueue，pop是deque

        # 将深度为1的节点的failure设为根节点
        for succ in self.goto_table[0].values():
            if succ != 0:
                self.failure[succ] = 0
                queue.append(succ)

        # 为深度 > 1 的节点建立failure表
        while queue:
            current_state = queue.pop()
            for character,succ in self.goto_table[current_state].items():
                queue.append(succ)
                backtrace = self.failure[current_state]

                while self.goto(backtrace,character) == None:
                    backtrace = self.failure.get(backtrace)
                    if not backtrace:
                        backtrace = 0
                    
                    
                fail_state = self.goto(backtrace,character)
                self.failure[succ] = fail_state
                self.output_table[succ] = self.output(succ) | self.output(fail_state)


    def build(self):
        """构建Aho-Corasick模式匹配机
        """

        # 构建goto函数，同时开始构建output函数
        self.construct_goto()

        # 构建failure函数，同时完成构建output函数
        self.construct_failure()


    def output(self,state):
        emits = self.output_table.get(state)
        return emits or set()

    def goto(self,state,character):
        succ = self.goto_table[state].get(character)

        if succ == None and state == 0: 
        # 出现这种情况是因为有未知词，即text中有自动机不包含的字符
            return 0
        else:
            return succ



    def process(self,text,longest_match=False,keyword_only=False,value_only=False):
        """处理text，逐个读入字符，遇到匹配时生成

        longest_match -- 生成最长的匹配
        keyword_only -- 只生成关键词
        value_only -- 只生成value
        """
        state = 0
        for i, character in enumerate(text):
            while self.goto(state,character)==None:
                state = self.failure[state]
            state = self.goto(state,character)
            emits = self.output(state)
            if emits:

                if longest_match:
                    longest_emit = max(emits, key=len)
                    if keyword_only:
                        yield longest_emit
                    else:
                        yield Match(i+1 - len(longest_emit),i+1,longest_emit,self.keywords[longest_emit])
                elif keyword_only:
                    for emit in emits:
                        yield emit
                elif value_only:
                    for emit in emits:
                        yield self.keywords[emit]
                else:
                    for emit in emits:
                        yield Match(i+1 - len(emit),i+1,emit,self.keywords[emit])



    def match(self,text):
        """处理text，逐个读入字符，遇到匹配返回True。

        """
        state = 0
        for i, character in enumerate(text):
            while self.goto(state,character)==None:
                state = self.failure[state]
            state = self.goto(state,character)
            if self.output(state):
                return True

        return False
            
    

           




    