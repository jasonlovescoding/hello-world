import urllib.request,json,re,time #urllib用于抓包 json用于解析 re用于匹配车站名称 time用于获取本地时间  
import tkinter as tk        #用于基本的gui窗口  
import tkinter.ttk as ttk   #用于需求美观的gui widgets  
#使用本程序前请先将系统环境设置为信任12306的根证书，以保证12306返回的json不会被系统拦截  
def getStationNames(from_station,to_station):           #获取车站名称信息，输入为汉字，输出为12306可读的标识符  
    url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js' #需要抓取的包来自这个URL  
    req=urllib.request.Request(url)                     #建立请求对象  
    response=urllib.request.urlopen(req)                #发送请求并获取服务器的反馈  
    data=response.read()                                #读取反馈信息，其中记录了汉字与车站标识符的对应关系  
    try:  
        data=data.decode('utf-8')                       #尝试解码 首先使用utf-8格式  
    except:  
        data=data.decode('gbk','ignore')                #失败则强制使用汉字编码模式  
    from_station=re.findall('%s\|([^|]+)' % from_station,data)[0]   #正则匹配发站标识符  
    to_station=re.findall('%s\|([^|]+)' % to_station,data)[0]       #正则匹配到站标识符  
    return from_station,to_station                      #返回匹配结果  
  
class TicketPool:                       #这个类记录了“某一日某车次从某地到某地”的票池  
    def __init__(self):  
        self.station_train_code=''      #列车号  
        self.start_train_date=''        #发车日期  
        self.from_station_name=''       #出发站  
        self.to_station_name=''         #目的站  
        self.lishi=''                   #历时  
        self.start_time=''              #开始时间  
        self.arrive_time=''             #到达时间  
        self.swz_num=''                 #商务座数  
        self.tz_num=''                  #特等座数  
        self.zy_num=''                  #一等座数  
        self.ze_num=''                  #二等座数  
        self.gr_num=''                  #高级软卧数  
        self.rw_num=''                  #软卧数  
        self.yw_num=''                  #硬卧数  
        self.rz_num=''                  #软座数  
        self.yz_num=''                  #硬座数  
        self.wz_num=''                  #无座数  
        self.qt_num=''                  #其他座数  
          
def getTicketPools(queryDate,from_station,to_station): #本函数接收“发车日”“起始地”“目的地”，返回“那一天” 所有 从“起始地”到“目的地”的票池集合  
    #根据“发车日”“起始地”“目的地”生成12306可识别的查票URL，发送至服务器端并接收反馈，将反馈解析成票池的集合  
    url='https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=0X00&queryDate=%s&from_station=%s&to_station=%s'%(queryDate,from_station,to_station)   
    req=urllib.request.Request(url)      #ditto  
    response=urllib.request.urlopen(req) #ditto  
    data=response.read()                 #ditto  
    try:                                 #ditto  
        data=data.decode('utf-8')        #ditto  
    except:                              #ditto  
        data=data.decode('gbk','ignore') #ditto  
      
    try:  
        trains=json.loads(data)["data"]["datas"] #服务器端返回一个json包，首先需要尝试将其解包  
    except:                                      #由于直接解包后获得的是一个字典，其中包含多个列表，列表的中元素是包含车票信息的字典，  
        trains=[]                                #经过分析我们不需要解包所有值，只需要其中["data"]["datas"]部分  
    TicketPools=[]                               #如果解包失败说明包空无票，将trains作一个空表，也就使得TicketPools最终为空  
      
    for train in trains:                        #将要存储到TicketPools中的内容是  
        tmp=TicketPool()                        #每一个字典生成的TicketPool，它来自于解包得到的列表中的每个字典包含的车票信息  
        tmp.station_train_code=train["station_train_code"]      #列车号  
        tmp.start_train_date=train["start_train_date"]        #发车日期  
        tmp.from_station_name=train["from_station_name"]       #出发站  
        tmp.to_station_name=train["to_station_name"]         #目的站  
        tmp.lishi=train["lishi"]                   #历时  
        tmp.start_time=train["start_time"]              #开始时间  
        tmp.arrive_time=train["arrive_time"]             #到达时间  
        tmp.swz_num=train["swz_num"]                 #商务座数  
        tmp.tz_num=train["tz_num"]                  #特等座数  
        tmp.zy_num=train["zy_num"]                  #一等座数  
        tmp.ze_num=train["ze_num"]                  #二等座数  
        tmp.gr_num=train["gr_num"]                  #高级软卧数  
        tmp.rw_num=train["rw_num"]                  #软卧数  
        tmp.yw_num=train["yw_num"]                  #硬卧数  
        tmp.rz_num=train["rz_num"]                  #软座数  
        tmp.yz_num=train["yz_num"]                  #硬座数  
        tmp.wz_num=train["wz_num"]                  #无座数  
        tmp.qt_num=train["qt_num"]                  #其他座数  
        TicketPools.append(tmp)                     #存入TicketPools   
    return TicketPools                              #返回TicketPools  
  
def is_leap_year(year): #判断是否为闰年 为日期调换作准备  
    if (year%4==0 and year%100!=0) or year%400==0:  #是4且不是100的整倍数 或者是400的整倍数  
        return True #是闰年  
    else:         #否则  
        return False #不是  
  
def next_day(today):  #输入一个12306可识别的日期标识符，输出下一天的日期标志符  
    [yr,mon,day]=today.split('-')  #利用标识符的-号将其分为年月日三部分  
    months=[31,28,31,30,31,30,31,31,30,31,30,31] #存储每个月天数  
    if(is_leap_year(int(yr))): #闰年  
        months[1]=29            #2月有29天  
    if(int(day)+1>months[int(mon)-1]):          #跨月  
        if(int(mon)==12):                        #跨年  
            mon='01'              #变为01月  
            day='01'              #变为01日  
            yr=str(int(yr)+1)     #年数加一  
        else:                                   #不跨年  
            mon=str(int(mon)+1).zfill(2)       #月数加一并补零填充为2位  
            day='01'                          #日期为01号  
    else:                                       #不跨月  
        day=str(int(day)+1).zfill(2)          #不跨月只需将日期加一并补零为2位  
    tomorrow="%s-%s-%s"%(yr,mon,day)          #将年月日重新粘合为标识符  
    return tomorrow                         #返回下一天的标识符  
  
def getTicketStack(from_station,to_station,start_date,end_date): #本函数通过接受起站、止站、起日和止日获取这一时期内每一天票池集合的集合  
    from_station,to_station=getStationNames(from_station,to_station)    #得到正确的起站、止站标识符  
    TicketStack=[]  #建立集合  
    while True:       
        if start_date==end_date: #从起日开始 判断是否到达止日  
            TicketStack.append(getTicketPools(start_date,from_station,to_station)) #如果到达止日 将这一天的票池存储  
            break #而后退出  
        TicketStack.append(getTicketPools(start_date,from_station,to_station)) #如果没到达止日 将这一天的票池存储  
        start_date=next_day(start_date)  #而后取下一日  
    return TicketStack #返回票池集合的集合  
  
class User_Interface:   #用户界面  
    def __init__(self): #初始化  
        self.root=tk.Tk() #tk窗口  
        self.root.geometry("650x400") #默认大小  
        self.root.title("查票器V1.0") #注明功能和版本  
  
        menubar = tk.Menu(self.root)  
        self.root["menu"]=menubar  
        helpmenu = tk.Menu(menubar, tearoff=0)  
        helpmenu.add_command(label="帮助",command=self.morehelp)  
        helpmenu.add_command(label="关于",command=self.moreabout)  
        helpmenu.add_separator()  
        helpmenu.add_command(label="退出", command=self.root.destroy)  
        menubar.add_cascade(label="更多", menu=helpmenu)  
          
        inputframe=tk.Frame(self.root) #输入部分放入一个Frame  
        inputframe.pack()               #显示Frame  
        tk.Label(inputframe,text="查票器V1.0").grid(row=0,column=2) #注释  
  
        tk.Label(inputframe,text="出发站:").grid(row=1,column=0,pady=1) #出发站输入界面注释  
        self.from_station_entry=ttk.Entry(inputframe) #出发站采用entry接收  
        self.from_station_entry.grid(row = 1, column = 1,pady=1) #显示这个entry  
  
        self.startdays=[]  #可选出发时间列表   
        today=time.strftime("%Y-%m-%d", time.localtime()) #获取系统的今日日期并转化为12306可识别模式  
        for i in range(60): #12306的预售期为60天  
            self.startdays.append(today) #加入这天的日期  
            today=next_day(today) #变为下一天  
          
        self.start_date=tk.StringVar() #建立监控起日的变量  
        self.start_date_box=ttk.Combobox(inputframe,textvariable=self.start_date,values=self.startdays,  
                                         height=6,width=14) #起日采用combobox接收  
        tk.Label(inputframe,text="起始日期:").grid(row=1,column=2,pady=2) #显示label  
        self.start_date_box.set(self.startdays[0]) #初始为今天的日期  
        self.start_date_box.grid(row = 1, column=3,pady=1) #显示combobox  
              
        tk.Label(inputframe,text="目的站:").grid(row=2,column=0,pady=1) #注释  
        self.to_station_entry=ttk.Entry(inputframe) #目的站用entry接收  
        self.to_station_entry.grid(row = 2, column = 1,pady=3) #显示这个entry  
          
        self.end_date=tk.StringVar() #建立监控止日的变量  
        self.end_date_box=ttk.Combobox(inputframe,textvariable=self.end_date,values="输入起日",  
                                       height=6,width=14, postcommand =lambda:self.setenddays())#止日列表的初始日期取决于起日  
        tk.Label(inputframe,text="结束日期:").grid(row=2,column=2,pady=2) #显示label  
        self.end_date_box.set(self.start_date.get()) #初始为起日日期  
        self.end_date_box.grid(row = 2, column = 3,pady=3) #显示combobox   
  
        runbutton=ttk.Button(inputframe,text='查询',command=lambda: self.submit()) #设置完成输入后的查询按钮  
        runbutton.grid(row=1,column=4,padx=8,rowspan=2) #显示按钮  
  
        outputframe=tk.Frame(self.root) #输出部分装入一个Frame  
        outputframe.pack(padx=10) #显示这个Frame  
          
        titles=("列车号","发车日期","出发站","目的站","历时","发车时间","到达时间","商务座","特等座",     
            "一等座","二等座","高级软卧","软卧","硬卧","软座","硬座","无座","其他")  #需要显示的车票信息  
          
        self.ticketstack_tree= ttk.Treeview(outputframe,columns=titles) #建立表格的根节点（实质上表格是一个树）  
        self.ticketstack_tree.pack() #显示表格  
        self.ticketstack_tree['show'] = 'headings' #只显示根节点的子节点，以隐藏空的第一列  
        for each in titles:  #每个车票信息  
            self.ticketstack_tree.column(each,width=80,anchor='center') #有专门的一列  
            self.ticketstack_tree.heading(each,text=each) #显示文本为本身  
        vsb=ttk.Scrollbar(outputframe) #左右拖动滑块  
        vsb["orient"]='horizon' #设置为水平  
        vsb.pack(fill = 'x') #x方向补满  
        self.ticketstack_tree["xscrollcommand"]=vsb.set #将表格的水平控制交由vsb滑块  
        vsb['command']=self.ticketstack_tree.xview #将vsb滑块的控制对象设置为表格的水平视角  
          
        self.root.mainloop() #进入事件循环  
  
    def submit(self): #查询按钮的控制函数  
        from_station=self.from_station_entry.get() #获取起站  
        to_station=self.to_station_entry.get() #获取止站  
        start_date=self.start_date.get() #获取起日  
        end_date=self.end_date.get() #获取止日  
          
        self.trains=0 #查到的列车总数  
        for each in self.ticketstack_tree.get_children(): #先清空原先的表格  
            self.ticketstack_tree.delete(each) #即把表格根节点的每一个子节点删除  
              
        ticketstack=getTicketStack(from_station,to_station,start_date,end_date) #获取票池集合的集合  
          
        for eachpools in ticketstack: #对每一个票池集合  
            for eachpool in eachpools: #当中的每一个票池  
                tabulater=(eachpool.station_train_code, eachpool.start_train_date, eachpool.from_station_name, eachpool.to_station_name, eachpool.lishi,  
                        eachpool.start_time, eachpool.arrive_time, eachpool.swz_num, eachpool.tz_num, eachpool.zy_num, eachpool.ze_num,  
                        eachpool.gr_num, eachpool.rw_num, eachpool.yw_num, eachpool.rz_num, eachpool.yz_num, eachpool.wz_num, eachpool.qt_num) #读出其全部信息  
                self.ticketstack_tree.insert('',self.trains,values=tabulater) #并将这些信息显示出来  
                self.trains+=1 #查到的车数+1 用于记录下一次插到第几行  
        self.ticketstack_tree.pack() #显示表格  
  
    def setenddays(self): #用于止日可选列表的设定  
        try:  
            startday=self.start_date.get() #尝试能否直接获取起日  
            enddays=[] #能则设定止日列表  
            for i in range(7): #7天内  
                enddays.append(startday) #将起日开始的所有日期装入  
                if startday==self.startdays[59]: #如果碰到了从系统今日开始的第60天，说明已经达到预售期  
                    break #退出循环 不再增加  
                startday=next_day(startday) #如果没碰到 就将其变为下一天  
            self.end_date_box["values"]=enddays #将止日的combobox显示列表更新  
            self.end_date_box.set(enddays[0]) #将止日的combobox显示更新  
        except:   
            pass #不能则跳过  
          
    def morehelp(self):  
        text1="1.输入你出发所在城市和目的地城市的汉语名称，通过“起始时间”和“结束时间”栏确定你需要查票的时间区间,点击“查询”即可\n"           
        text2="2.推荐首先设置系统使之信任12306根证书，否则本程序将不能完成功能，且您可能会无法访问12306购票网站"  
        tk.messagebox.showinfo("帮助",text1+text2)  #帮助栏  
  
    def moreabout(self):  
        text1="☺2015-12-10 Programmed by Jason ZHANG\n"  
        text2="   School of Computer Science and Engineering, Beihang Univ."  
        tk.messagebox.showinfo("关于",text1+text2)  #作者栏  
  
      
if __name__=='__main__':  
    User_Interface() #显示查票器
