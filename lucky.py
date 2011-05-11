#-*- coding: utf-8 -*-
import sys
import os
import random
import time
import threading

try:
    import pygtk
    pygtk.require('2.0')
except:
    pass

try:
    import gtk
except:
    print "GTK Not avaliable!"
    sys.exit(1)

class update(threading.Thread):
    def __init__(self):
        """初始化线程"""
        threading.Thread.__init__(self,name="update")
        self.label=None
        self.num=0
        self.over=False

    def setNum(self,widget,data):
        """设置label的text值"""
        widget.set_text(str(data))
        return True

    def kill(self):
        """设置标志位,来杀死线程"""
        self.over=True

    def run(self):
        while not self.over :
            self.num=random.randint(1,200)
            self.setNum(self.label,self.num)
            time.sleep(0.1000)


class lucky():
    """抽奖的一个小程序"""
    def on_window_destroy(self,widget,data=None):
        gtk.main_quit()

    def __init__(self):
        """读取glade文件,并自动链接信号"""

        #从xml文件中读取数据,并链接必要的信号
        self.builder=gtk.Builder()
        self.file=sys.path[0]+"/lucky.glade"
        self.builder.add_from_file(self.file)
        self.builder.connect_signals(self)
        for widget in  self.builder.get_objects():
            if issubclass(type(widget),gtk.Buildable):
                name=gtk.Buildable.get_name(widget)
                setattr(self,name,widget)
        #显示所有窗体
        self.window.set_size_request(800,500)
        self.window.show()

    def on_startbutton_clicked(self,widget,data=None):
        """开始抽奖"""
        self.u=update()
        self.u.label=self.luckylabel
        self.u.setDaemon(True)
        self.u.start()

    def on_stopbutton_clicked(self,widget,data=None):
        """停止,显示当前号码"""
        self.u.kill()

    #主循环
    def main(self):
            gtk.main()

if __name__=="__main__":
    gtk.gdk.threads_init()
    lc=lucky()
    lc.main()
