def play(stat,storage):
    return storage['is_safe'](stat,storage)

def load(stat,storage):
    from random import choice

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

    def find_path(stat,storage,band):
        #band为所要去的条形区域[[]]
        path=[[]]
        return path

    def is_safe(stat,storage):
        if True:   #判断是否需要更新路径
            storage['set_track'](2,stat['now']['me']['id'],stat['now']['fields'])
        return choice('lrxxxx')

    storage['set_track']=set_track
    storage['find_path']=find_path
    storage['is_safe']=is_safe
