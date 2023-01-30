# GUI 클라이언트
from socket import *
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pymysql

form_class = uic.loadUiType("untitled.ui")[0]

class ChatClient(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(600,100)
        self.stackedWidget.setCurrentIndex(0)
        self.sw_open_chat.setCurrentIndex(0)
        # self.btn_send_message.clicked.connect(self.send_chat)
        # self.le_message.returnPressed.connect(self.send_chat)
        self.le_name.returnPressed.connect(self.go_main)
        self.btn_finish.clicked.connect(self.go_main)
        self.btn_exit.clicked.connect(self.chat_exit)
        self.btn_chat_open.clicked.connect(self.chat_room_stack)
        self.btn_room_fns.clicked.connect(self.add_chat_room)
        self.connect_signal = False
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='net',
                                    charset='utf8')


    def go_main(self):
        self.sender_name = self.le_name.text()
        self.lb_senders_name.setText(self.sender_name)
        if self.sender_name =='':
            QMessageBox.information(self, '사용자', '사용자 정보를 입력해주세요.', QMessageBox.Ok)
            return
        else:
            # ip = '192.168.219.109'
            ip = '10.10.21.104'
            port = 9050
            self.initialize_socket(ip, port)
            self.stackedWidget.setCurrentIndex(1)
            self.chat_room_update()
            self.Thread_exit = False
            listen_thr = listen_Qthread(self)
            listen_thr.start()
            self.le_name.clear()

    def chat_room_stack(self):
        self.sw_open_chat.setCurrentIndex(1)
    def add_chat_room(self):
        chat_name = self.le_chat_room.text()
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"create table `chat_room_{chat_name}` ("
                            f"날짜 VARCHAR(45),"
                            f"시간 VARCHAR(45),"
                            f"송신자 VARCHAR(45),"
                            f"수신자 VARCHAR(45),"
                            f"내용 VARCHAR(100)"
                            f") ENGINE=InnoDB CHARSET=utf8;")
        self.cursor.execute(f"insert into chat_list (채팅방이름,개설자,참여인원) values ('{chat_name}','{self.sender_name}','{str(1)}')")
        self.conn.commit()
        open_chat_message = (f"{self.sender_name}/!@|CHATING ROOM OPEN|@!").encode('utf-8')
        self.client_socket.send(open_chat_message)

    def chat_room_update(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"select * from chat_list")
        a_chat_list = self.cursor.fetchall()
        self.tw_chat_list.setRowCount(len(a_chat_list))
        for i in range(len(a_chat_list)):
            for j in range(len(a_chat_list[i])):
                self.tw_chat_list.setItem(i,j, QTableWidgetItem(str(a_chat_list[i][j])))
    def chat_exit(self):
        exit_msg = (f"{self.sender_name}/!&%*|EXIT|*%&!").encode('utf-8')
        self.client_socket.send(exit_msg)
        self.stackedWidget.setCurrentIndex(0)
        self.Thread_exit = True

    def initialize_socket(self, ip, port):
        '''
        TCP socket을 생성하고 server와 연결
        '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))
        connect_message= (f"{self.sender_name}/{self.sender_name}님이 접속했습니다.").encode('utf-8')
        self.client_socket.send(connect_message)

    # def send_chat(self):
    #     '''
    #     message를 전송하는 버튼 콜백 함수
    #     '''
    #     message = self.le_message.text()
    #     if message == "":
    #         return
    #     else:
    #         self.le_message.clear()
    #         message = (f"{self.sender_name}/{self.sender_name}: {message}").encode('utf-8')
    #         self.client_socket.send(message)

    # def go_chat(self):
    #     self.lw_message.clear()
    #     self.lb_senders_name.setText(self.sender_name)
    #     if self.sender_name =='':
    #         QMessageBox.information(self, '사용자', '사용자 정보를 입력해주세요.', QMessageBox.Ok)
    #         return
    #     else:
    #         ip = '10.10.21.104'
    #         # ip = '192.168.219.109'
    #         port = 9050
    #         self.initialize_socket(ip, port)
    #         self.stackedWidget.setCurrentIndex(2)
    #         self.Thread_exit = False
    #         listen_thr = listen_Qthread(self)
    #         listen_thr.start()
    #         self.le_name.clear()
    def closeEvent(self, QCloseEvent):
        exit_msg = (f"{self.sender_name}/!&%*|EXIT|*%&!").encode('utf-8')
        self.Thread_exit = True
        self.client_socket.send(exit_msg)
        QCloseEvent.accept()
        self.client_socket.close()

class listen_Qthread(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
    def run(self):
        print('쓰레드 시작')
        while True:
            if self.parent.Thread_exit:
                print('쓰레드 종료')
                break
            buf = self.parent.client_socket.recv(1024)
            print('쓰레드')
            if not buf: # 연결이 종료됨
                break
            buf = buf.decode('utf-8')
            print(buf)
            if '@!|USER CONNECT|!@' in buf:
                name= buf.split('/')[1]
                print(name)
                self.parent.lw_online_user.addItem(name)
                self.pa
                continue
            elif '!@|CHATING ROOM OPEN|@!' in buf:
                print(buf)
                self.parent.chat_room_update()
                continue
            self.parent.lw_message.addItem(buf.decode('utf-8'))
            self.parent.lw_message.scrollToBottom()
        self.parent.client_socket.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatclient = ChatClient()
    #프로그램 화면을 보여주는 코드
    chatclient.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
