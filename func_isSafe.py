def isSafe(stat,storage):
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
    #辅助函数部分
    #判断是否在制定路径上的函数
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


    #判断路径上的下一步是否安全的函数
    def isNextStepSafe(x,y,path,storage):
        '''
        辅助函数说明：判断路径上的下一个位置，通过比较'路径上下一个位置回到领地的最短距离'和'对方到我当前纸带的最短距离'，判断是否会产生危险
        传入函数说明：
            x:  int 当前纸卷横坐标
            y:  int 当前纸卷纵坐标
            path:   list[list]  二维列表，指定的路径
            storage:
        返回：
            True:   bool    如果指定路径上的下一个位置是安全的，就返回真
            False:  bool    如果指定路径上的下一个位置是危险的，就返回假
        version:
            0.1:    date:2018/6/5   sid 整体架构建立，调用的辅助函数getNextPosition、isNowSafe还不够完整。这两个函数都需要用到童的函数。
            0.2:    date:2018/6/7   sid getNextposition已经完成，同时考虑了找不到路径上下一个位置的情况，如果此时已经将所有的绕圈路径走完，
            那么返回危险，纸卷会生成逃跑路径，往家的方向逃一部，然后再次调用回到圈地路径的时候，会发现圈地路径已经没有了，这种情况怎么办？
        '''
        #得到路径上下一个位置坐标
        nextX,nextY=getNextPosition(x,y,path)
        if nextX==False:
            #找不到下一个位置坐标，直接返回危险（目的：在外层函数中实现回家）
            return False
        #进行安全的判断并返回
        return isNowSafe(nextX,nextY,stat,storage)   #isNowSafe返回bool 

    def isNowSafe(x,y,stat,torage):
        '''
        辅助函数说明：判断传入坐标的位置是否是安全的
        传入参数说明：
            x:  int
            y:  int
            storage:
        返回：
            True:   当前位置安全
            False:  当前位置危险
        version:
            0.1 date:2018/6/5   sid 创建，因为不知道getdistance函数具体的参数模板，暂时无法使用
        '''
        disMe2Home=getdistance(stat,operate='me_to_home')#当前位置我纸卷到领地的最短距离
        disHe2Me=getdistance(stat,operate='enemy_to_path',pathstat=mypaper,pathmark=myid)#敌人纸卷到我目前纸带的最短距离
        if disMe2Home<disHe2Me-1:
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
        if isOnTrack(x,y,path):
            #如果(x,y)在路径上，则按照北东南西的顺序，寻找下一个位置
            if isOnTrack(x,y-1,path):
                return  x,y-1
            elif isOnTrack(x+1,y,path):
                return x+1,y
            elif isOnTrack(x,y+1,path):
                return x,y+1
            elif isOnTrack(x-1,y,path):
                return x-1,y
            else:
                print("整个路径只剩下一个点了，没有下一个位置")           #！！！这是一个用来debug的语句，最后需要将他排除掉！！！
                '''
                这其实是一种存在的情况，如果圈地路径是闭合的，那么绕着圈地路径走完一圈，下一部就要走到自己纸带上的时候，就会出现没有下一个，暂定返回 False,Fasle 吧
                '''
                return False,False
        else:
            print("坐标（x,y）不在该路径上，不能找到该路径上的下一个位置")   #！！！这是一个用来debug的语句，最后需要将他删除掉！！！
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
    
    def back_track(myX,myY,stat,storage):
        '''
        辅助函数说明：返回一个到圈地路径的相对方向
        传入参数：
            myX:    int 当前的横坐标
            myY：   int 当前的纵坐标
            stat
            storage
        传出参数：
            'left'
            'right'
            'straight'
        version:
            0.1:    date:2018/6/7   sid     创建
        '''
        null,BackTrack=findpath()#当前到圈地路径的路
        nextX,nextY=getNextPosition(myX,myY,BackTrack)
        return getRelativeDirection(myX,myY,nextX,nextY,stat)


        

    #第一部分：声明本函数中定义的函数
    my_x=stat['now']['me']['x']
    my_y=stat['now']['me']['y']
    RoundTrack=storage['RoundTrack']    #这里需要自己后面将生成的路径放到storage中？？？这里如果还没生成roundtrack怎么办？
    no_tag=0    #路径二维数组中，将路径擦除就将它变成0
    try:
        EscapeTrack=storage['EscapeTrack']
    #判断是否在圈地路径上：
    if isOnTrack(my_x,my_y,RoundTrack):
        #已知在圈地路径上，判断圈地路径上下一个位置是否安全
        if isNextStepSafe():
            #安全，沿着路径走，返回下一个位置的绝对坐标
            nextX,nextY=getNextPosition(my_x,my_y,RoundTrack)
            #将当前位置的路径标记擦除
            RoundTrack[my_x][my_y]=no_tag
            #将坐标转换为相对方向
            dirc=getRelativeDirection(my_x,my_y,nextX,nextY,stat)
            #返回转向指令
            return dirc
        else:#不安全，返回逃跑路径，沿着逃跑路径走
            #创建逃跑路径，存到storage中
            null,storage['EscapeTrack']=findpath()
            #返回沿着逃跑路径走的一个方向（并将逃跑路径标记抹除）
            nextX,nextY=getNextPosition(my_x,my_y,storage['EscapeTrack'])
            storage['EscapeTrack'][my_x][my_y]=no_tag
            return  getRelativeDirection(my_x,my_y,nextX,nextY,stat)
    else:#如果不在圈地路径上
        if isOnTrack(my_x,my_y,EscapeTrack):
            #如果在逃跑路径上
            if isNowSafe(my_x,my_y,stat,storage):
                #调用函数back_track
                null,BackTrack=findpath()

               
                #将逃跑路径清空
                storage['EscapeTrack']=None
                return  back_track(my_x,my_y,stat,storage)
            else:#逃跑过程中一直处于不安全的状态
                #得到逃跑路径上的下一个坐标
                nextX,nextY=getNextPosition(my_x,my_y,EscapeTrack)
                #将当前位置的逃跑路径标记擦除
                EscapeTrack[my_x][my_y]=no_tag
                #转换为相对方向
                return getRelativeDirection(my_x,my_y,nextX,nextY,stat)
                #返回转向指令
        elif stat[my_x][my_y]:#如果不在逃跑路径上，那就是在领地中，或者是想要回到
            #调用函数back_track
            return back_track(my_x,my_y,stat,storage)


        


