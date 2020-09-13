from tkinter import *

class basedesk():
    def __init__(self,master):
        self.root=master
        self.root.config()
        self.root.title("林猫猫的小世界")
        self.root.geometry("400x350")
        initface(self.root)

class initface():
    def __init__(self,master):
        self.master=master
        self.master.config()
        self.initface=Frame(self.master)
        self.initface.pack()
        
        self.photo=PhotoImage(file='20200620000837_haYTW.gif')
        logo=Button(self.initface,image=self.photo,
                    cursor='heart',command=self.change)

        label0=Label(self.initface,text='欢迎来到林猫猫的小世界',
                     bg='#fae3d9',fg='#1e2022',
                     font='TIMES 15 bold',
                     cursor='star')

        label1=Label(self.initface,text='账号',
                     bg='#fae3d9',fg='#1e2022',
                     width=4,
                     font='宋体 13 bold',
                     cursor='star')

        label2=Label(self.initface,text='密码',
                     bg='#fae3d9',fg='#1e2022',
                     width=4,
                     font='宋体 13 bold',
                     cursor='star')

        self.x=StringVar()
        message1=Entry(self.initface,textvariable=self.x,width=31)
        self.y=StringVar()
        message2=Entry(self.initface,textvariable=self.y,width=31,show='*')

        label0.grid(row=0,column=0,columnspan=2,padx=5,pady=10)
        logo.grid(row=1,column=0,columnspan=2,padx=10,pady=10)
        label1.grid(row=2,column=0,pady=10)
        message1.grid(row=2,column=1,pady=10)
        label2.grid(row=3,column=0,pady=0)
        message2.grid(row=3,column=1,pady=0)


    def change(self):
        if self.x.get()=='张骞昊是一只有用的猪猪' and self.y.get()=='XLZXHZQH':
            self.initface.destroy()
            face0(self.master)

class face0():
    def __init__(self,master):
        self.master=master
        self.master.config(bg='#f0f0f0')
        self.face0=Frame(self.master)
        self.face0.pack()

        label=Label(self.face0,text='\n\n张猪猪你好呀~这里是林猫猫的小世界\n\n如果你想探索这个小世界\n\n就要开动你的小脑筋\n\n答题答题再答题\n\n看完了吗，看完了就赶紧开始吧！',
                     bg='#bbded6',fg='#f8f3d4',
                     font='宋体 13 bold',cursor='star',
                     wraplength=300,justify='left',
                     padx=20,pady=20)
        btn=Button(self.face0,text='我超喜欢猫猫！肯定难不倒我！开始吧！',command=self.back,
                   bg="#ffb6b9",cursor='heart',
                   font='宋体 13 bold',
                   padx=3,pady=3)
        label.grid(row=0,column=0,padx=20,pady=20)
        btn.grid(row=1,column=0,pady=10)
    def back(self):
        self.face0.destroy()
        face1(self.master)
    

class face1():
    def __init__(self,master):
        self.master=master
        self.master.config(bg='#f0f0f0')
        self.face1=Frame(self.master)
        self.face1.pack()

        label3=Label(self.face1,text='\n\n听说你是个超级好看的帅哥\n\n天天被夸真好看\n\n你知不知道我是听谁说的呀？',
                     bg='#bbded6',fg='#f8f3d4',
                     font='宋体 13 bold',cursor='star',
                     wraplength=300,justify='left',
                     padx=20,pady=20)
        btn=Button(self.face1,text='哼，我当然知道',command=self.back,
                   bg="#ffb6b9",cursor='heart',
                   font='宋体 13 bold',
                   padx=3,pady=3)
        self.z=StringVar()
        message3=Entry(self.face1,textvariable=self.z,width=20)
        
        label3.grid(row=0,column=0,columnspan=2,padx=10,pady=30)
        message3.grid(row=1,column=0,padx=10,pady=10)
        btn.grid(row=1,column=1,padx=10,pady=10)
    def back(self):
        if self.z.get()=='我的猫猫':
            self.face1.destroy()
            face2(self.master)

class face2():
    def __init__(self,master):
        self.master=master
        self.master.config(bg='#f0f0f0')
        self.face2=Frame(self.master)
        self.face2.pack()

        label=Label(self.face2,text='\n\n第一题很简单的！\n\n林猫猫送了一只自己喜欢的大象给张骞昊\n\n它叫什么呀？',
                    bg='#bbded6',fg='#f8f3d4',
                    font='宋体 13 bold',cursor='star',
                    wraplength=300,justify='left',
                    padx=20,pady=20)
        btn=Button(self.face2,text='哼哼还是我想的！',command=self.back,
                   bg="#ffb6b9",cursor='heart',
                   font='宋体 13 bold',
                   padx=3,pady=3)
        self.a=StringVar()
        message3=Entry(self.face2,textvariable=self.a,width=20)
        
        label.grid(row=0,column=0,columnspan=2,padx=10,pady=30)
        message3.grid(row=1,column=0,padx=10,pady=10)
        btn.grid(row=1,column=1,padx=10,pady=10)
    def back(self):
        if self.a.get()=='巴豆':
            self.face2.destroy()
            face3(self.master)

class face3():
    def __init__(self,master):
        self.master=master
        self.master.config(bg='#f0f0f0')
        self.face3=Frame(self.master)
        self.face3.pack()

        label=Label(self.face3,text='\n\n前面两个问题都是热身的！\n\n张骞昊叫起床困难户林猫猫起床的时候\n\n林猫猫都会说什么呀？',
                    bg='#bbded6',fg='#f8f3d4',
                    font='宋体 13 bold',cursor='star',
                    wraplength=300,justify='left',
                    padx=20,pady=20)
        btn=Button(self.face3,text='每天叫猫猫起床的我太清楚啦',command=self.back,
                   bg="#ffb6b9",cursor='heart',
                   font='宋体 13 bold',
                   padx=3,pady=3)
        self.a=StringVar()
        message3=Entry(self.face3,textvariable=self.a,width=20)
        
        label.grid(row=0,column=0,columnspan=2,padx=10,pady=30)
        message3.grid(row=1,column=0,padx=10,pady=10)
        btn.grid(row=1,column=1,padx=10,pady=10)
    def back(self):
        if self.a.get()=='我不想起床':
            self.face3.destroy()
            face4(self.master)

class face4():
    def __init__(self,master):
        self.master=master
        self.master.config(bg='#f0f0f0')
        self.face4=Frame(self.master)
        self.face4.pack()

        label=Label(self.face4,text=
                    '\n\n嘻嘻嘻，恭喜来到第四关n\n林猫猫最喜欢的可乐是什么牌子的呀？',
                    bg='#bbded6',fg='#f8f3d4',
                    font='宋体 13 bold',cursor='star',
                    wraplength=300,justify='left',
                    padx=20,pady=20)
        btn=Button(self.face4,text='嗯，我承认它是最棒的',command=self.back,
                   bg="#ffb6b9",cursor='heart',
                   font='宋体 13 bold',
                   padx=3,pady=3)
        self.a=StringVar()
        message3=Entry(self.face4,textvariable=self.a,width=20)
        
        label.grid(row=0,column=0,columnspan=2,padx=10,pady=30)
        message3.grid(row=1,column=0,padx=10,pady=10)
        btn.grid(row=1,column=1,padx=10,pady=10)
    def back(self):
        if self.a.get()=='可口可乐':
            self.face4.destroy()
            face5(self.master)

class face5():
    def __init__(self,master):
        self.master=master
        self.master.config(bg='#f0f0f0')
        self.face5=Frame(self.master)
        self.face5.pack()

        label=Label(self.face5,text=
                    '\n\n在林猫猫飞奔上班的时候\n\n张骞昊喊的台词出自哪部电影呀？',
                    bg='#bbded6',fg='#f8f3d4',
                    font='宋体 13 bold',cursor='star',
                    wraplength=300,justify='left',
                    padx=20,pady=20)
        btn=Button(self.face5,text='当时垃圾男孩很开心',command=self.back,
                   bg="#ffb6b9",cursor='heart',
                   font='宋体 13 bold',
                   padx=3,pady=3)
        self.a=StringVar()
        message3=Entry(self.face5,textvariable=self.a,width=20)
        
        label.grid(row=0,column=0,columnspan=2,padx=10,pady=30)
        message3.grid(row=1,column=0,padx=10,pady=10)
        btn.grid(row=1,column=1,padx=10,pady=10)
    def back(self):
        if self.a.get()=='阿甘正传':
            self.face5.destroy()
            face6(self.master)

class face6():
    def __init__(self,master):
        self.master=master
        self.master.config(bg='#f0f0f0')
        self.face6=Frame(self.master)
        self.face6.pack()

        label=Label(self.face6,text=
                    '\n\n林猫猫学不会数学\n\n张骞昊看了一下课件就学会了\n\n并且教会了林猫猫的科目是什么？',
                    bg='#bbded6',fg='#f8f3d4',
                    font='宋体 13 bold',cursor='star',
                    wraplength=300,justify='left',
                    padx=20,pady=20)
        btn=Button(self.face6,text='林猫猫是可爱的傻瓜蛋',command=self.back,
                   bg="#ffb6b9",cursor='heart',
                   font='宋体 13 bold',
                   padx=3,pady=3)
        self.a=StringVar()
        message3=Entry(self.face6,textvariable=self.a,width=20)
        
        label.grid(row=0,column=0,columnspan=2,padx=10,pady=30)
        message3.grid(row=1,column=0,padx=10,pady=10)
        btn.grid(row=1,column=1,padx=10,pady=10)
    def back(self):
        if self.a.get()=='STAT6038':
            self.face6.destroy()
            face7(self.master)

class face7():
    def __init__(self,master):
        self.master=master
        self.master.config(bg='#f0f0f0')
        self.face7=Frame(self.master)
        self.face7.pack()

        label=Label(self.face7,text=
                    '\n\n林猫猫说喵！喵喵！喵喵喵！是什么意思呢？\n\n',
                    bg='#bbded6',fg='#f8f3d4',
                    font='宋体 13 bold',cursor='star',
                    wraplength=300,justify='left',
                    padx=20,pady=20)
        btn=Button(self.face7,text='小猫咪肯定不会说脏话的',command=self.back,
                   bg="#ffb6b9",cursor='heart',
                   font='宋体 13 bold',
                   padx=3,pady=3)
        self.a=StringVar()
        message3=Entry(self.face7,textvariable=self.a,width=20)
        
        label.grid(row=0,column=0,columnspan=2,padx=10,pady=30)
        message3.grid(row=1,column=0,padx=10,pady=10)
        btn.grid(row=1,column=1,padx=10,pady=10)
    def back(self):
        if self.a.get()=='我喜欢你':
            self.face7.destroy()
            face8(self.master)

class face8():
    def __init__(self,master):
        self.master=master
        self.master.config(bg='#f0f0f0')
        self.face8=Frame(self.master)
        self.face8.pack()

        label=Label(self.face8,text='啊恭喜你成功通关！果然张骞昊超级棒的！张骞昊发现了吗，林猫猫的小世界里全部都是你~小林真的真的超级喜欢你！希望以后的日子里都有你！希望能一直是张骞昊喜欢的乖乖小猫咪~',
                     bg='#bbded6',fg='#f8f3d4',
                     font='宋体 13 bold',cursor='star',
                     wraplength=350,justify='left',
                     padx=20,pady=20)
        btn=Button(self.face8,text='返回，我要再来亿遍',command=self.back,
                   bg="#ffb6b9",cursor='heart',
                   font='宋体 13 bold',
                   padx=3,pady=3)
        label.grid(row=0,column=0,padx=10,pady=20)
        btn.grid(row=1,column=0,pady=10)

    def back(self):
        self.face8.destroy()
        initface(self.master)

if __name__=='__main__':
    root=Tk()
    basedesk(root)
    root.mainloop()
