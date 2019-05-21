import sys
import  requests
import PyQt5.QtGui
from PyQt5.QtCore import Qt
import json
from PyQt5.QtWidgets import *

newsNum=3
textLineStyle='QLineEdit{border:1px solid gray;width:300px;border-radius:10px;padding:2px 4px;}'
titleStyle='width:80px;height:45px;border-width: 1px;border-style: plain;border-color: rgb(255 ,100  ,0 );background-color:rgb(53,123,221);color:white;'
class mainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setFixedWidth(300)
        self.setFixedHeight(140)
        self.setWindowTitle("登录")
        self.setWindowIcon(PyQt5.QtGui.QIcon("./Icon.jpg"))
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        loginlayout=QVBoxLayout()
        self.name=QLineEdit()
        self.name.setPlaceholderText("用户名")
        self.name.setEnabled(False)
        loginlayout.addWidget(self.name)
        self.password=QLineEdit()
        self.password.setPlaceholderText("密码")
        self.password.setEchoMode(QLineEdit.Password)
        loginlayout.addWidget(self.password)
        loginButtonLayout=QHBoxLayout()
        loginButtonLayout.setAlignment(Qt.AlignHCenter)
        loginButton = QPushButton("Login")
        loginButton.setFixedWidth(120)
        loginButtonLayout.addWidget(loginButton)
        loginButton.clicked.connect(self.login)
        loginlayout.addLayout(loginButtonLayout)
        self.setLayout(loginlayout)
    def login(self):
        password=self.password.text()
        secret=requests.get("https://myncutdev.ncut.edu.cn/getauth").text
        if password!=secret:
            QMessageBox.warning(self,"密码错误","    密码错误   ")
        else:
            self.close()
            self.window=clientWindow()
            self.window.show()

class clientWindow(QWidget):
    newsButtonList=[]
    functionList=[]
    newsList=[]
    informButtonList=[]
    infromList=[]
    def __init__(self):
        QWidget.__init__(self)
        self.setFixedWidth(900)
        self.setFixedHeight(300)
        self.setWindowTitle("我的北方新闻管理")
        self.setWindowIcon(PyQt5.QtGui.QIcon("./Icon.jpg"))
        frame=self.frameGeometry()
        center=QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        wholeLayout=QVBoxLayout()
        title1=QLabel("新闻")
        title1.setFrameShape(QFrame.Box)
        title1.setStyleSheet(titleStyle)

        wholeLayout.addWidget(title1)

        for i in range(newsNum):
            newsLayout=QHBoxLayout()
            newsTip=QLabel("新闻"+str(i+1)+"：")
            newsLayout.addWidget(newsTip)
            newsLink=QLineEdit()

            self.newsList.append(newsLink)
            newsLink.setFixedHeight(30)
            newsLink.setStyleSheet(textLineStyle)
            newsLink.setPlaceholderText("文章链接")

            newsLayout.addWidget(newsLink)
            newsImg=QLineEdit()
            self.newsList.append(newsImg)
            newsImg.setFixedHeight(30)
            newsImg.setStyleSheet(textLineStyle)
            newsImg.setPlaceholderText("图片链接")
            newsLayout.addWidget(newsImg)
            newsButton=QPushButton("更新")

            newsButton.clicked.connect(self.makefun(i))

            self.newsButtonList.append(newsButton)
            newsLayout.addWidget(newsButton)
            wholeLayout.addLayout(newsLayout)

        title2 = QLabel("公告")
        title2.setStyleSheet(titleStyle)
        wholeLayout.addWidget(title2)
        for i in range(newsNum):
            newsLayout=QHBoxLayout()
            newsTip=QLabel("公告"+str(i+1)+"：")
            newsLayout.addWidget(newsTip)
            newsLink=QLineEdit()
            self.infromList.append(newsLink)
            newsLink.setFixedHeight(30)
            newsLink.setStyleSheet(textLineStyle)
            newsLink.setPlaceholderText("公告内容")
            newsLayout.addWidget(newsLink)
            newsButton=QPushButton("更新")
            newsButton.clicked.connect(self.makefun_indorm(i))
            self.informButtonList.append(newsButton)

            # newsButton.setStyleSheet(titleStyle)
            # newsButton.setStyleSheet(textLineStyle)
            newsLayout.addWidget(newsButton)
            wholeLayout.addLayout(newsLayout)
        self.setLayout(wholeLayout)
    def makefun(self,index):
        def newsUpdate():
            newsLink=self.newsList[index].text()
            imgLink=self.newsList[index*2+1].text()
            print(index)
            requests.post("https://myncutdev.ncut.edu.cn/storedata",{"msgUrl":newsLink,"imgUrl":imgLink,"type":"banner","index":str(index)})
        return newsUpdate

    def makefun_indorm(self,index):
        def informUpate():
            inform=self.infromList[index].text()
            requests.post("https://myncutdev.ncut.edu.cn/storedata",data=({"text":inform,"type":"notice","index":str(index)}))

        return informUpate
if __name__=="__main__":
    app=QApplication(sys.argv)
    window=mainWindow()
    window.show()
    sys.exit(app.exec_())