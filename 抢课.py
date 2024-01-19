import requests
from future.backports.test.ssl_servers import threading
 
 # 获取cookie 和 课程id就可以抢课
 
 
def qian1():
    data = 202120221008221
    # data 是找到的课程ID，因为python没学好，代码写的有点乱
    # 下面是地址 就是我们抓到的那个数据包的URL
    url = 'http://jw.sdufe.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?kcid=1C76076A00FC4DE8A42FC631D22DFB9B&cfbs=null&xyjc=undefined&jx0404id='+str(data)+"&xkzy=&trjf="
    cookie = ' __guid=87634819.4086716089534391000.1626660395862.9094; Hm_lvt_9129285f5377948859f2bbac3ff5b223=1626579514,1626587491,1626750064,1626862685; JSESSIONID=7A511CBBE4EFE9EC836483446284DA66; monitor_count=9'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Referer': 'http://172.30.1.70/srun_portal_pc.php?ac_id=1',
        'cookie':cookie
    }
 
    # 一直抢！
    while True:
        # 设定5s服务器未应答就放弃这次，鬼知道是服务器炸了还是。。。。
        mes = requests.get(url, headers=header, timeout=5) 
        # 打印返回的结果，就是弹出来的那个小窗口的内容
        print(str(1)+str(mes.status_code)+':'+str(mes.text))
 
 
'''# 后面是不同的课，因为不能吊在一课树上！
def qian():
    data = 201820192001302
    url = 'http://*****/jsxsd/xsxkkc/bxxkOper?jx0404id='+str(data)
    cookie = '*****cookie'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Referer': 'http://172.30.1.70/srun_portal_pc.php?ac_id=1',
        'cookie':cookie
    }
    while True:
        mes = requests.get(url, headers=header, timeout=5)
        print(str(0)+str(mes.status_code)+':'+str(mes.text))
 
 
 
def qian2():
    data = 201820192001155
    url = 'http://****n/jsxsd/xsxkkc/bxxkOper?jx0404id=' + str(data)
    cookie = 'cookie'
 
 
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Referer': 'http://172.30.1.70/srun_portal_pc.php?ac_id=1',
        'cookie': cookie
    }
    while True:
        mes = requests.get(url, headers=header, timeout=5)
        print(str(2)+str(mes.status_code) + ':' + str(mes.text))
 
 '''
 
def main():
    # 开多线程分开抢课
    # 接下来就会一直抢课！
    thread2 = threading.Thread(target=qian1)
    thread5 = threading.Thread(target=qian1)

 
    thread2.start()
    thread5.start()
 
 
 
main()
