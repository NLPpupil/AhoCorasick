class State:
    def __init__(self,depth=0):
        """构造深度为depth的节点
        """
        self._depth = depth
        self.transition = dict() # 该状态的转移分支，字符到状态的字典
        self.emits = set() 
        self._index = 0 # 拿掉这行会报错

    def add_emit(self,keyword_id):
        """添加一个关键词
        """
        self.emits.add(keyword_id)
 

    def is_accepting_state(self):
        return self.depth >0 and self.emits 

    def set_failure(self,fail_state, failure):
        """设置failure函数

        fail_state -- 该状态的fail状态
        fail -- fail表
        """
        self.fail_state = fail_state
        failure[self.index] = fail_state.index 

    def transit(self,c,ignoreRootState=False):
        """根据字符c转移到下一个状态

        原则上，如果没有c这个分支，返回None。ignoreRootState是True的话表示初始状态也不例外
        如果ignoreRootState是False，表示初始状态没分支的话则转移到自身

        return -- 所转移到的状态
        """
        transit_to = self.transition.get(c)
        # 如果是初始状态，且没有c这个分支，且不忽略初始状态，则转移到自身
        if not ignoreRootState and not transit_to and self.depth == 0:
            transit_to = self
        return transit_to

    def move(self,c):
        """根据字符c转移到下一个状态。如果没有这个分支，则创建分支。
        """
        transit_to = self.transit(c,True)
        if not transit_to:
            transit_to = State(self.depth + 1)
            self.transition[c]= transit_to
        return transit_to

    @property
    def successors(self):
        """返回后继状态
        """
        return self.transition.values()

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self,index):
        self._index = index

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self,index):
        self._depth = depth


    

    def __str__(self):
        return "depth:{0}\n".format(self.depth)+\
               "emits:{0}\n".format(self.emits)+\
               "id:{0}\n".format(self.index)+\
               "transition:{0}\n".format(self.transition) 


