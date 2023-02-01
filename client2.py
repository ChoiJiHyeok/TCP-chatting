import sys
import json
from socket import *
import pymysql as p
from threading import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic


form_class=uic.loadUiType('jichat.ui')[0]

class MultiChating(QWidget,form_class):
    client_socket=None
    def __init__(self,ip, port):
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        self.initialize_socket(ip,port)
        self.listen_thread()
        self.chatroom_btn.clicked.connect(self.page2)
        self.enter_btn.clicked.connect(self.send_chat)
        self.chat_lineEdit.returnPressed.connect(self.send_chat)
        self.outroom_btn.clicked.connect(self.out_room)
        self.login_signal='' ## 로그인 안함
    def out_room(self):
        self.stackedWidget.setCurrentIndex(0)
        self.id_lineEdit.clear()
        self.login_signal=""# 로그아웃 했을때 시그널

    def page2(self):
        if self.id_lineEdit.text() == '':
            QMessageBox.about(self, '알림','이름을 입력하세요')
        else:
            #채팅창에 ~ 입장하셨습니다.
            self.login_signal='@@'+self.id_lineEdit.text()
            self.stackedWidget.setCurrentIndex(1)
            self.listWidget.addItem(self.id_lineEdit.text()+'님 입장하셨습니다.')
            self.user_listWidget.addItem(self.id_lineEdit.text())
            send_signal=self.login_signal
            login_msg=(send_signal).encode('utf-8')
            self.client_socket.send(login_msg)



    def initialize_socket(self,ip, port):
        self.client_socket=socket(AF_INET, SOCK_STREAM)
        chat_ip=ip
        chat_port=port
        self.client_socket.connect((chat_ip,chat_port))

    def send_chat(self):
        """
        message를 전송하는 버튼 콜백 함수

        """
        senders_name=self.id_lineEdit.text()
        data=self.chat_lineEdit.text()
        message=(senders_name+':'+ data).encode('utf-8')
        self.listWidget.addItem(message.decode('utf-8'))
        self.client_socket.send(message)
        print(self.listWidget.count())
        text_list=[]
        for i in range(self.listWidget.count()):
            self.listWidget.item(i).text()
            print(self.listWidget.item(i).text())
            text_list.append(self.listWidget.item(i).text())
        print(text_list)
        self.chat_lineEdit.clear()
        return 'break'

    def listen_thread(self):
        """
        데이터를 수신 Thread를 생성하고 시작한다.
        """
        t=Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()

    def receive_message(self, so):
        while True:
            buf=so.recv(256)
            if not buf:
                break
            print(buf.decode('utf-8'))
            if '@@' in buf.decode('utf-8'):
                self.user_listWidget.addItem(buf.decode('utf-8')[2:])
                self.listWidget.addItem(buf.decode('utf-8')[2:]+'님 입장하셨습니다.')
            else:
                self.listWidget.addItem(buf.decode('utf-8'))
        so.close()



if __name__=='__main__':
    ip='10.10.21.105'
    port=9001
    app=QApplication(sys.argv)
    popup=MultiChating(ip,port)
    popup.show()
    app.exec_()