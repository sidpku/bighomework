to_attack=False
def attack(stat):
    me_attack_path,me_attack_distance=find_path(stat,operate='me_to_path',pathstat=stat['now']['bands'],pathmark=stat['now']['enemy']['id'],outputmark='suppose')
    enemy_home_path,enemy_home_distance=find_path(stat,operate='enemy_to_home')
    enemy_me_path,enemy_me_distance=find_path(stat,operate='enemy_to_path',pathstat=me_attack_path,pathmark='suppose')
    if me_attack_distance<enemy_home_distance and me_attack_distance<enemy_me_distanc11e:
        is_attack=True
    else:
        pass

def evaluate_d(stat):
    n=abs(stat['now']['me']['x']-stat['now']['enemy']['x'])+abs(stat['now']['me']['y']-stat['now']['enemy']['y'])
    if n>=20:
        return n*2//5
    elif n>=12 and n<20:
        return n//3
    else:
        return n//4
