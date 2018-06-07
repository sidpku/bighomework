def play(stat,storage):
    '''
    '''
    myid=stat['now']['me']['id']
    hisid=stat['now']['enemy']['id']

    set_track=storage['set_track']
    find_path=storage['find_path']
    is_safe=storage['is_safe']
    attack=storage['attack']
    evaluate_d=storage['evaluate_d']


    if storage['start']==Ture:
    	#调用秦晓宇的函数，生成路径
    	storage['to_start']=False

    attack(stat)
    if storage['to_attack']==True:
		null,AttackTrack=find_path(stat,operate='me_to_path',pathstat=stat['now']['bands'],pathmark=hisid-1,outputmark='t')#当前到圈地路径的路
		nextX,nextY=getNextPosition(myX,myY,BackTrack)
		return getRelativeDirection(myX,myY,nextX,nextY,stat)
	else:
		return is_safe(stat,storage)

def load(stat,storage):
    from random import choice

    #变量初始化区域
    storage['switch']=False
    storage['start']=True
    storage['to_attack']=False
    

    def attack(stat):
        '''
        辅助函数说明：攻击函数，用来判断什么时候攻击。当判断需要攻击的时候，将存储在storage中的to_attack关键词赋值为True
        传入参数：stat
        传出参数：无
        version:
            1.0:    date:2018/6/8   Guo 
        '''
        me_attack_path,me_attack_distance=find_path(stat,operate='me_to_path',pathstat=stat['now']['bands'],pathmark=stat['now']['enemy']['id'],outputmark='suppose')
        enemy_home_path,enemy_home_distance=find_path(stat,operate='enemy_to_home')
        enemy_me_path,enemy_me_distance=find_path(stat,operate='enemy_to_path',pathstat=me_attack_path,pathmark='suppose')
        if me_attack_distance<enemy_home_distance and me_attack_distance<enemy_me_distanc11e:
            storage['to_attack']=True	
        else:
            pass

    def evaluate_d(stat):
        '''
        辅助函数说明：距离d的生成函数
        传入参数：stat
        传出参数：
            d   int d的数值，用来建立圈地路径
        version:
            1.0:    date:2018/6/8   Guo 
        '''
        n=abs(stat['now']['me']['x']-stat['now']['enemy']['x'])+abs(stat['now']['me']['y']-stat['now']['enemy']['y'])
        if n>=20:
            return n*2//5
        elif n>=12 and n<20:
            return n//3
        else:
            return n//4

    def set_track(d=2, _id=1, fields=None):
        '''
        函数说明：更新圈地路径
        传入参数：
            d int 离开领地的距离
            _id int 我方的编号
            fields list[list[]] 二维数组，表示双方的领地
        中间变量：（太多了）
        返回：
            不返回值，生成的结果将保存在storage['track']中。结果为一个二维数组，0表示非路径，'t'表示路径
        Version:
            2.0: date:2018/6/7  by st   将本函数嵌入play
        '''
        # 预处理
        col, row, corner_list = len(fields), len(fields[0]), []
        border = [[0 for y in range(row)] for x in range(col)]  # 边界数组，用于识别角
        track = [[0 for y in range(row)] for x in range(col)]  # 路径数组

        # 上下扫描和左右扫描,将每一边向外扩展d的距离
        for x in range(col):
            for y in range(row):
                if fields[x][y] == _id:
                    count = 0
                    if y > 0 and fields[x][y - 1] != _id:
                        track[x][max(0, y - d)] += 1
                        count = 1
                    if y < row - 1 and fields[x][y + 1] != _id:
                        track[x][min(row - 1, y + d)] += 1
                        count = 1
                    border[x][y] += count
        for y in range(row):
            for x in range(col):
                if fields[x][y] == _id:
                    count = 0
                    if x > 0 and fields[max(0, x - 1)][y] != _id:
                        track[x - d][y] += 1
                        count = 1
                    if x < col - 1 and fields[x + 1][y] != _id:
                        track[min(col - 1, x + d)][y] += 1
                        count = 1
                    border[x][y] += count
                if border[x][y] == 2:
                    corner_list.append((x, y))
        # 将track中的值复制到border中（border原来的值已经没有意义）
        for x in range(col):
            for y in range(row):
                border[x][y] = track[x][y]
        # 处理角上的缺口
        for i in corner_list:
            x, y = i[0], i[1]
            n = max(0, y - d)  # m和n用于保证不出界
            if border[x][n] != 0:
                m = max(0, x - d)
                if border[m][y] != 0:
                    for a in range(m, x):
                        track[a][n] += 1
                    for a in range(n, y):
                        track[m][a] += 1
                m = min(col - 1, x + d)
                if border[m][y] != 0:
                    for a in range(x + 1, m + 1):
                        track[a][n] += 1
                    for a in range(n, y):
                        track[m][a] += 1
            n = min(row - 1, y + d)
            if border[x][n] != 0:
                m = max(0, x - d)
                if border[m][y] != 0:
                    for a in range(m, x):
                        track[a][n] += 1
                    for a in range(y + 1, n + 1):
                        track[m][a] += 1
                m = min(col - 1, x + d)
                if border[m][y] != 0:
                    for a in range(x + 1, m + 1):
                        track[a][n] += 1
                    for a in range(y + 1, n + 1):
                        track[m][a] += 1
        # 去掉多余路径标记(通过模拟纸卷的行动）
        x, y, stop, _min, min_x, min_y = 0, 0, False, float('inf'), 0, 0
        while x < col:  # 初始定位
            y = 0
            while y < row:
                if track[x][y] == 1:
                    min_x, min_y, stop = x, y, True
                    break
                elif 1 < track[x][y] < _min:
                    min_x, min_y = x, y
                y += 1
            if stop:
                break
            else:
                x += 1
        x, y = min_x, min_y
        final = [[0 for b in range(row)] for a in range(col)]  # 最终返回值

        # 路径评估函数（内部使用）
        def evaluate_dir(x, y, label=''):
            '''
            函数说明：以上方法可能生成一些岔路（尤其是领地有凹角、凹边、飞地甚至更糟的时候），本函数将评估出合适的路径
            传入参数：
                x,y  int,int  待处理的位置坐标
                label str 标记，即如何从上一个位置来到这里（向上、向下、向左、向右）
            返回：
                'left'or'right'or'up'or'down'or 'stop'
            '''
            if track[x][y] == 1:
                if label == 'up':
                    return label if y > 0 and track[x][y - 1] > 0 else 'stop'
                elif label == 'down':
                    return label if y < row - 1 and track[x][y + 1] > 0 else 'stop'
                elif label == 'left':
                    return label if x > 0 and track[x - 1][y] > 0 else 'stop'
                elif label == 'right':
                    return label if x < col - 1 and track[x + 1][y] > 0 else 'stop'
            dis, _dir = 1, {'up': 0, 'down': 0, 'left': 0, 'right': 0}
            while len(_dir) > 1:
                if 'up' in _dir:
                    _dir['up'] = track[x][y - dis] if y > dis - 1 else -1
                if 'down' in _dir:
                    _dir['down'] = track[x][y + dis] if y < row - dis else -1
                if 'left' in _dir:
                    _dir['left'] = track[x - dis][y] if x > dis - 1 else -1
                if 'right' in _dir:
                    _dir['right'] = track[x + dis][y] if x < col - dis else -1
                m = max(_dir.values())
                if m < 0:
                    break
                j = 0
                while j < len(_dir):
                    k = list(_dir.keys())[j]
                    if _dir[k] < m:
                        _dir.pop(k)
                    else:
                        j += 1
                dis += 1
            if 'up' in _dir:
                _dir['up'] = track[x][y - 1] if y > 0 else -1
            if 'down' in _dir:
                _dir['down'] = track[x][y + 1] if y < row - 1 else -1
            if 'left' in _dir:
                _dir['left'] = track[x - 1][y] if x > 0 else -1
            if 'right' in _dir:
                _dir['right'] = track[x + 1][y] if x < col - 1 else -1
            j = 0
            while j < len(_dir):
                k = list(_dir.keys())[j]
                if _dir[k] < 1:
                    _dir.pop(k)
                else:
                    j += 1
            if 'up' in _dir:
                return 'up'
            elif 'down' in _dir:
                return 'down'
            elif 'left' in _dir:
                return 'left'
            elif 'right' in _dir:
                return 'right'
            else:
                return 'stop'

        # 开始模拟纸卷运动
        prim_x, prim_y, prim_label = x, y, evaluate_dir(x, y)
        label = prim_label
        while True:
            label = evaluate_dir(x, y, label)
            final[x][y], track[x][y] = 1, -1
            if label == 'up':
                y -= 1
            elif label == 'down':
                y += 1
            elif label == 'left':
                x -= 1
            elif label == 'right':
                x += 1
            else:
                break
        x, y = prim_x, prim_y
        track[x][y] = 1
        dd = ['up', 'left', 'down', 'right']
        label = dd[(dd.index(prim_label) + 2) % 4]
        while True:
            label = evaluate_dir(x, y, label)
            final[x][y], track[x][y] = 1, -1
            if label == 'up':
                y -= 1
            elif label == 'down':
                y += 1
            elif label == 'left':
                x -= 1
            elif label == 'right':
                x += 1
            else:
                break
        for x in range(col):
            for y in range(row):
                if final[x][y]:
                    final[x][y] = 't'
        storage['track']=final

    
    def is_safe(stat,storage):
        '''
        本函数中定义的变量：
            1.  my_x,my_y:我纸卷的x坐标,我的纸卷的y坐标,为整型
            2.  RoundTrack:圈地路径，使用别名，方便写程序
        本函数中的辅助函数:
            见辅助函数部分，共有4个。辅助函数部分注释很详细。辅助函数部分，版本号小于1，则还不能够运行。
        输入参数:
            stat:
            storage:
        返回：
            'left' or 'right' or 'straight'     转向指令，即  左转|右转|直行
        version:
            0.1 date:2018/6/5   sid 将整体的架构写出来，辅助函数中有一些没完成，根函数（即isSafe函数，在这里用根函数代称）也没有写一些算法的实现，只是将算法用伪代码给写好了，然后明天需要找大家确定函数接口。
        '''

        #第一部分：声明本函数中定义的函数
        my_x=stat['now']['me']['x']
        my_y=stat['now']['me']['y']
        no_tag=0    #路径二维数组中，将路径擦除就将它变成0
        track_tag='t'
        switch=storage['switch']

        isOnTrack=storage['isOnTrack']
        isNowSafe=storage['isNowSafe']
        storage['isNextStepSafe']
        getNextPosition=storage['getNextPosition']
        getRelativeDirection=storage['getRelativeDiraction']
        back_track=storage['back_track']
        back_home=storage['back_home']

        try:
            RoundTrack=storage['track']
        except KeyError:
            RoundTrack=None
        if isOnTrack(my_x,my_y,RoundTrack):
            RoundTrack[my_x][my_y]=0
            nextX,nextY=getNextPosition(my_x,my_y,RoundTrack)
            if nextX==False:
                switch=True
                return back_home(my_x,my_y,stat)
            else:
                if isNextStepSafe(my_x,my_y,RoundTrack):
                    return getRelativeDirection(my_x,my_y,nextX,nextY,stat)
                else:
                    return back_home(my_x,my_y,stat,storage)
        elif stat['now']['fields'][my_x][my_y]==stat['now']['me']['id']:
            d=evaluate_d(stat) 
            switch=False
            set_track(d,stat['now']['me']['id'],stat['now']['fields'])
            return  back_track(my_x,my_y,stat)### waiting to write
        else:
            if switch==True:
                return back_home(my_x,my_y,stat)
            else:
                dirc=back_track
                if dirc:
                    return dirc
                else:
                    return back_home(my_x,my_y,stat)
    
    def isOnTrack(x,y,path):
        '''
        辅助函数说明：判断某一个坐标是否在指定的路径上，一个超级简单的函数
        传入参数说明：
            x:  int 横坐标
            y:  int 纵坐标
            path:   list[list]  二重列表，路径
        返回：
            True:   bool    若在指定路径上，返回真
            False:  bool    若不在指定路径上，返回假
        version:
            0.1 date:2018/6/5   sid 没有path中标记方式，暂时没法写，尚处于不能运行状态
            2.0 date:2018/6/7   sid 函数目前已完成。path中的标记用一个变量track_tag来代替，暂时这个变量存储‘t’,如果后续有变更可以更改。
            2.1 date:2018/6/7   sid 修正传入的坐标可能引起下标越界的情况。
        '''
        track_tag='t'
        try:
            return path[x][y]==track_tag
        except IndexError:
            return False    #如果下标越界，就返回False
        except TypeError:
            return False    #如果路径不存在，就返回False

    def isNowSafe(stat=stat,storage=storage):
        disMe2Home,null=find_path(stat,operate='me_to_home')#当前位置我纸卷到领地的最短距离
        myid=stat['now']['me']['id']
        disHe2Me,null=find_path(stat,operate='enemy_to_path',pathstat=stat['now']['bands'],pathmark=myid)#敌人纸卷到我目前纸带的最短距离
        if disMe2Home>disHe2Me-1:
            return False
        else:
            return True

    def isNextStepSafe(stat=stat,storage=storage):
        disMe2Home=find_path(stat,operate='me_to_home')#当前位置我纸卷到领地的最短距离
        disHe2Me=find_path(stat,operate='enemy_to_path',pathstat=stat['now']['bands'],pathmark=stat['now']['me']['id'])#敌人纸卷到我目前纸带的最短距离
        if disMe2Home>disHe2Me-2:
            return False
        else:
            return True

    #找到路径上下一个位置的函数
    def getNextPosition(x,y,path):
        '''
        辅助函数说明：根据当前位置和指定路径，返回下一个路径上下一个位置的横纵坐标。
        传入函数说明：
            x:  int
            y:  int
            path:   list[list[int]]
        返回：
            nextX,nextY int,int 下一个位置的横坐标，纵坐标 
            False,False bool,bool   如果不在路径上，或者找不到下一个路径，就返回False，False
        version:
            0.1：    date:2018/6/5   sid 建立架构，因为不知道path二维列表如何标记路径，还没有写具体的函数,还不能使用    
            1.0：    date:2018/6/7   sid 将代码补充完整，调用辅助函数isOnTrack.辅助函数的标记还是一个问题。同时增加找不到下一个位置的情况，就返回 False,False
        '''
        if isOnTrack(x,y-1,path):
            return  x,y-1
        elif isOnTrack(x+1,y,path):
            return x+1,y
        elif isOnTrack(x,y+1,path):
            return x,y+1
        elif isOnTrack(x-1,y,path):
            return x-1,y
        else:
            return False,False
            
    def getRelativeDirection(myX,myY,nextX,nextY,stat):
        '''
        辅助函数：纸卷和相邻点的坐标传入，可以返回相对方向
        传入参数：
            myX:    int 当前的横坐标
            myY:    int 当前的纵坐标
            nextX:  int 下一步的横坐标
            nextY:  int 下一步的纵坐标
            stat
        传出参数：
            'left'
            'right'
            'straight'
        version:
            1.0:    date:2018/6/7   sid 完成函数
        '''
        mydirection=stat['now']['me']['direction']
        moveX=nextX-myX
        moveY=nextY-myY
        if moveX==0:
            if moveY==1:
                newdirection=0
            else:
                newdirection=2
        elif moveX==1:
            newdirection=1
        else:
            newdirection=3
        relativedirection=newdirection-mydirection
        if relativedirection==1:
            return  'right'
        elif relativedirection==0:
            return 'straight'
        elif relativedirection==-1:
            return 'left'
        elif relativedirection==-3:
            return  'right' 
        elif relativedirection==3:
            return 'left'
    
    def back_track(myX,myY,stat):
        if isNextStepSafe():
            null,BackTrack=find_path(stat,operate='me_to_path',pathstat=storage['track'],pathmark='t',outputmark='t')#当前到圈地路径的路
            nextX,nextY=getNextPosition(myX,myY,BackTrack)
            return getRelativeDirection(myX,myY,nextX,nextY,stat)
        else:
            return False

    def back_home(myX,myY,stat):
        null,EscapeTrack=find_path(stat,operate='me_to_home',outputmark='t')
        nextX,nextY=getNextPosition(myX,myY,EscapeTrack)
        return getRelativeDirection(myX,myY,nextX,nextY,stat)

    def find_path(stat,operate='me_to_home',pathstat=None,pathmark=None,outputmark='mypath'):
        '''
        寻路函数，寻找me/enemy到达各自领地，对方纸带，或给定路径的长度和路径
        传入参数：
            stat
            operate     字符串     默认me_to_home，支持me_to_home, me_to_path, enemy_to_home, enemy_to_path
            pathstat    二维数组    默认None,自定义的路径信息，配合_to_path两operate使用
            pathmark    字符串     默认None,自定义路径信息中的路径标记
            outputmark  字符串     默认mypath,输出路径信息中的路径标记
        返回：
            outputpath   二维数组
            distance    字符串     路径长度
        版本：
            1.0：    童培峰
        存在问题：
            出现同样distance的不同路径时如何寻找最优解
        '''
        if operate == 'me_to_home':
            myid = stat['me']['id']
            myx = stat['me']['x']
            myy = stat['me']['y']
            statlist = stat['fields']
            fieldid = myid
        elif operate == 'enemy_to_home':
            myid = stat['enemy']['id']
            myx = stat['enemy']['x']
            myy = stat['enemy']['y']
            statlist = stat['fields']
            fieldid = myid
        elif operate == 'me_to_path':
            myid = stat['me']['id']
            myx = stat['me']['x']
            myy = stat['me']['y']
            if not pathstat:
                statlist = stat['bands']
                fieldid = stat['enemy']['id']
            else:
                statlist = pathstat
                fieldid = pathmark
        elif operate == 'enemy_to_path':
            myid = stat['enemy']['id']
            myx = stat['enemy']['x']
            myy = stat['enemy']['y']
            if not pathstat:
                statlist = stat['bands']
                fieldid = stat['me']['id']
            else:
                statlist = pathstat
                fieldid = pathmark

        col_length = len(stat['fields'])#可以用storage里的size替代
        row_length = len(stat['fields'][0])
        distance = col_length + row_length
        finalpath = []

        for x in range(col_length):
            for y in range(row_length):
                #判断是不是领地范围
                if statlist[x][y] == fieldid:
                    temp_distance = abs(x-myx) + abs(y-myy)#计算最短路径距离
                    #判断距离是否更小
                    if temp_distance <= distance:
                        #分四象限考虑
                        if x <= myx and y <= myy:#第二象限
                            #是不是边缘点
                            if statlist[x+1][y] != fieldid and statlist[x][y+1] != fieldid:#角落
                                path1 = [(outputmark,i,y) for i in range(x,myx) if stat['bands'][i][y]!=myid]
                                path2 = [(outputmark,myx,j) for j in range(y,myy) if stat['bands'][myx][j]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                                else:
                                    path1 = [(outputmark,x,j) for j in range(y,myy) if stat['bands'][x][j]!=myid]
                                    path2 = [(outputmark,i,myy) for i in range(x,myx) if stat['bands'][i][myy]!=myid]
                                    path = path1 + path2
                                    if len(path) == temp_distance:
                                        distance = temp_distance
                                        finalpath = path
                            elif statlist[x+1][y] != fieldid:#同上一
                                path1 = [(outputmark,i,y) for i in range(x,myx) if stat['bands'][i][y]!=myid]
                                path2 = [(outputmark,myx,j) for j in range(y,myy) if stat['bands'][myx][j]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                            elif statlist[x][y+1] != fieldid:#同上二
                                path1 = [(outputmark,x,j) for j in range(y,myy) if stat['bands'][x][j]!=myid]
                                path2 = [(outputmark,i,myy) for i in range(x,myx) if stat['bands'][i][myy]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                        elif x > myx and y <= myy:#第一象限
                            if statlist[x-1][y] != fieldid and statlist[x][y+1] != fieldid:#角落
                                path1 = [(outputmark,i,y) for i in range(myx+1,x+1) if stat['bands'][i][y]!=myid]
                                path2 = [(outputmark,myx,j) for j in range(y,myy) if stat['bands'][myx][j]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                                else:
                                    path1 = [(outputmark,x,j) for j in range(y,myy) if stat['bands'][x][j]!=myid]
                                    path2 = [(outputmark,i,myy) for i in range(myx+1,x+1) if stat['bands'][i][myy]!=myid]
                                    path = path1 + path2
                                    if len(path) == temp_distance:
                                        distance = temp_distance
                                        finalpath = path
                            elif statlist[x-1][y] != fieldid:
                                path1 = [(outputmark,i,y) for i in range(myx+1,x+1) if stat['bands'][i][y]!=myid]
                                path2 = [(outputmark,myx,j) for j in range(y,myy) if stat['bands'][myx][j]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                            elif statlist[x][y+1] != fieldid:
                                path1 = [(outputmark,x,j) for j in range(y,myy) if stat['bands'][x][j]!=myid]
                                path2 = [(outputmark,i,myy) for i in range(myx+1,x+1) if stat['bands'][i][myy]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                        elif x <= myx and y > myy:#第三象限
                            if statlist[x+1][y] != fieldid and statlist[x][y-1] != fieldid:#角落
                                path1 = [(outputmark,i,y) for i in range(x,myx) if stat['bands'][i][y]!=myid]
                                path2 = [(outputmark,myx,j) for j in range(myy+1,y+1) if stat['bands'][myx][j]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                                else:
                                    path1 = [(outputmark,x,j) for j in range(myy+1,y+1) if stat['bands'][x][j]!=myid]
                                    path2 = [(outputmark,i,myy) for i in range(x,myx) if stat['bands'][i][myy]!=myid]
                                    path = path1 + path2
                                    if len(path) == temp_distance:
                                        distance = temp_distance
                                        finalpath = path
                            elif statlist[x+1][y] != fieldid:#同上一
                                path1 = [(outputmark,i,y) for i in range(x,myx) if stat['bands'][i][y]!=myid]
                                path2 = [(outputmark,myx,j) for j in range(myy+1,y+1) if stat['bands'][myx][j]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                            elif statlist[x][y-1] != fieldid:#同上二
                                path1 = [(outputmark,x,j) for j in range(myy+1,y+1) if stat['bands'][x][j]!=myid]
                                path2 = [(outputmark,i,myy) for i in range(x,myx) if stat['bands'][i][myy]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                        else:#第四象限
                            if statlist[x-1][y] != fieldid and statlist[x][y-1] != fieldid:#角落
                                path1 = [(outputmark,i,y) for i in range(myx+1,x+1) if stat['bands'][i][y]!=myid]
                                path2 = [(outputmark,myx,j) for j in range(myy+1,y+1) if stat['bands'][myx][j]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                                else:
                                    path1 = [(outputmark,x,j) for j in range(myy+1,y+1) if stat['bands'][x][j]!=myid]
                                    path2 = [(outputmark,i,myy) for i in range(myx+1,x+1) if stat['bands'][i][myy]!=myid]
                                    path = path1 + path2
                                    if len(path) == temp_distance:
                                        distance = temp_distance
                                        finalpath = path
                            elif statlist[x-1][y] != fieldid:
                                path1 = [(outputmark,i,y) for i in range(myx+1,x+1) if stat['bands'][i][y]!=myid]
                                path2 = [(outputmark,myx,j) for j in range(myy+1,y+1) if stat['bands'][myx][j]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
                            elif statlist[x][y-1] != fieldid:
                                path1 = [(outputmark,x,j) for j in range(myy+1,y+1) if stat['bands'][x][j]!=myid]
                                path2 = [(outputmark,i,myy) for i in range(myx+1,x+1) if stat['bands'][i][myy]!=myid]
                                path = path1 + path2
                                if len(path) == temp_distance:
                                    distance = temp_distance
                                    finalpath = path
            outputpath = [[None for j in range(row_length)] for i in range(col_length)]
            for item in finalpath:
                outputpath[item[1]][item[2]]=item[0]
        return outputpath, distance

    storage['set_track']=set_track
    storage['find_path']=find_path
    storage['is_safe']=is_safe
    storage['attack']=attack
    storage['evaluate_d']=evaluate_d
    storage['isOnTrack']=isOnTrack
    storage['isNowSafe']=isNowSafe
    storage['isNextStepSafe']=isNextStepSafe
    storage['getNextPosition']=getNextPosition
    storage['getRelativeDiraction']=getRelativeDirection
    storage['back_track']=back_track
    storage['back_home']=back_home

    
