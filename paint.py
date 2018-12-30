#!/usr/bin/env py
import time
import requests
import math
from colorama import Fore, Back, Style, init

init()

class user:
    def __init__(self, cookie_dict, last_time):
        self.cookie_dict = cookie_dict
        self.last_time = last_time

class task:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.col = col

data = {'x': 0, 'y': 0, 'color': 0}
user_lst = []
task_que = []

def print_line():# 输出分割线
    print(Fore.MAGENTA + "==============================================================================")

times = 0
mlst = []
task_success = 0
task_success_que = []
#用户代理报头
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def check_task(point):
    #print(Fore.GREEN+"check_task({0},{1})".format(point.x,point.y))
    #对用到的全局变量的声明
    global times
    global mlst
    global task_success
    if times == 100:#每check这么多次就更新一次q
        times -= 100
    if times == 0:
        print(Fore.GREEN+"update q!")
        try:
            q = requests.get("https://www.luogu.org/paintBoard/board", cookies=user_lst[0].cookie_dict, headers=headers,timeout=20)
        except:
            time.sleep(0.01)
            q = requests.get("https://www.luogu.org/paintBoard/board", cookies=user_lst[0].cookie_dict, headers=headers,timeout=20)
        mlst = q.text.split('\n')#每一行分为一个字符串元素；字符串数组即为二维字符数组
    times += 1
    if mlst[point.x][point.y] == point.col:
        task_success += 1
        return True
    else:
        return False


with open("cookies.txt", "r") as cok:#打开cookies文件（注意文件末不要有空格）
    coks = cok.readlines()
    for i in coks:#对于每一行
        umid = i.split(' ')[0]
        clid = i.split(' ')[1]
        uid = i.split(' ')[2]
        uid = uid.replace('\n', '')
        user_lst.append(user(dict(UM_distinctid=umid, __client_id=clid, _uid=uid), time.time() - 29))
    print_line()
    print(Fore.CYAN + "Users:")
    for i in user_lst:
        print(Fore.YELLOW + "cookies: {0}".format(i.cookie_dict))
    print_line()
# 图片的左上角坐标
base_x = 407
base_y = 49

with open("base32.txt", "r") as pic:#ppm转'LGPB'友好文件
    s = pic.readline()# 只读取第一行
    l = int(str(s).split(' ')[0])# 第一行两个数：行和列
    h = int(str(s).split(' ')[1])
    task_num = l * h #总任务数量
    lst = pic.readlines()#读取所有行，每一行作为一个元素存在列表中
    for i in range(0, len(lst)):#这里要求文件的行数和列数与l,h对应
        lst[i] = lst[i].replace('\n', '')
        for j in range(0, len(lst[i])):
            task_que.append(task(j + base_x, i + base_y, lst[i][j]))#添加任务到队列
    print(Fore.GREEN + "length: {0} height: {1}".format(l, h))
    print(Fore.GREEN + "{0} tasks added".format(l * h))
    for i in lst:
        print(i)
    print_line()

log_timer = time.time()

print(Fore.GREEN+"QUEUE START")
while len(task_que) > 0:
    now_task = task_que[0]#赋值队首
    task_que.pop(0)#弹出
    stat = check_task(now_task)
    if stat == False:#如果需要画
        #data['x'] = now_task.x
        #data['y'] = now_task.y
        #data['color'] = int(str(now_task.col), base=32)
        data = { 'x' : now_task.x , 'y' : now_task.y , 'color' : int(str(now_task.col),base=32) }
        user = user_lst[0]#用户队列中的第一个
        user_lst.pop(0)
        if 30 + user.last_time > time.time():#如果时间没有冷却完就冷却
            slp_time=math.ceil(30+user.last_time-time.time())
            for i in range(slp_time,0,-1):
                print(Fore.RED+"\r"+"waiting:{0}s".format(i),end='')
                time.sleep(1)
                print("\r"+" "*30,end='')
            #time.sleep(30 + user.last_time - time.time())
        try:
            r = requests.post("https://www.luogu.org/paintBoard/paint",
                              data=data, cookies=user.cookie_dict, headers=headers,timeout=20)
        except:
            time.sleep(0.01)
            r = requests.post("https://www.luogu.org/paintBoard/paint",
                              data=data, cookies=user.cookie_dict, headers=headers,timeout=20)
        if str(r.text).find("500") != -1:
            out = Fore.RED
            print(out + "Paint failed")
        else:
            out = Fore.GREEN
            print(out + "Paint succeed")
            task_success += 1
            task_success_que.append(time.time())
            if len(task_success_que) != 0:
                if time.time() - task_success_que[0] > 30:
                    task_success_que.pop(0)
        print(out + "ret_code: {0} text: {1}".format(r.status_code, r.text))
        print(out + "user: {0}".format(user.cookie_dict))
        print(Fore.CYAN + "pos&color: {0}".format(data))
        print_line()
        user.last_time = time.time() + 1
        user_lst.append(user)
    task_que.append(now_task)
    if time.time() - log_timer > 5:
        with open("stat.log", "w") as logger:
            logger.write("30s {0}\n".format(len(task_success_que)))
            logger.write("all {0}\n".format(task_success))
            logger.write("{0}%\n".format(task_success*100/task_num))
        log_timer = time.time()
print("==============FINISHED=================")
print_line()
