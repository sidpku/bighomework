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
        finalpath   列表      路径列表，如[('mypath', 3, 2), ('mypath', 4, 2), ('mypath', 5, 2)]
        distance    字符串     路径长度
    版本：
        1.0：    童培峰
    存在问题：
        输出finalpath还不是二维列表，下一版本改进
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
    return finalpath, distance

if __name__=='__main__':
    stat={}
    me={}
    stat['me']=me
    stat['me']['id'] = 1
    stat['me']['x'] = 3
    stat['me']['y'] = 3
    enemy={}
    stat['enemy']=enemy
    stat['enemy']['id']=2
    stat['enemy']['x']=2
    stat['enemy']['y']=2
    stat['fields'] = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[1,0,0,0,0,0]]
    stat['bands'] = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,1,0,0,0,0],[0,1,1,1,0,0]]
    finalpath, distance = find_path(stat,'me_to_home')
    print(distance)
    print(finalpath)
