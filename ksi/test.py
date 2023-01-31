# GUI 클라이언트
import json
from socket import *
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

form_class = uic.loadUiType("untitled.ui")[0]

class ChatClient(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.move(100,100)
        self.move(600, 100)
        self.stackedWidget.setCurrentIndex(0)
        self.sw_open_chat.setCurrentIndex(0)
        self.btn_send_message.clicked.connect(self.send_chat)
        self.le_message.returnPressed.connect(self.send_chat)
        self.le_name.returnPressed.connect(self.go_main)
        self.btn_finish.clicked.connect(self.go_main)
        self.btn_exit.clicked.connect(self.chat_exit)
        self.btn_chat_open.clicked.connect(self.chat_room_stack)
        self.btn_room_fns.clicked.connect(self.add_chat_room)
        self.btn_back_input.clicked.connect(self.go_input_name_page)
        self.tw_chat_list.setColumnWidth(0, 141)
        self.tw_chat_list.setColumnWidth(1, 141)
        self.tw_chat_list.setColumnWidth(2, 141)
        self.tw_chat_list.cellDoubleClicked.connect(self.go_chat)

    def send_chat(self):
        message = self.le_message.text()
        self.le_message.clear()
        send_message_signal= f"{self.login_user_id}/!@#|SEND MESSAGE|#@!/{message}/{self.chat_room_name}/{self.chat_serial_number}".encode()
        self.client_socket.send(send_message_signal)

    def chat_data_update(self,chat_data):
        for i in chat_data:
            if i[3]!= None:
                self.lw_message.addItem(f"{i[0]}  {i[1]}{i[2]}")
                continue
            self.lw_message.addItem(f"{i[0]}  {i[1]}: {i[2]}")
        self.lw_message.scrollToBottom()
    def go_chat(self):
        self.lw_message.clear()
        chat_room_info = self.tw_chat_list.selectedItems()
        self.chat_serial_number = self.tw_chat_list.currentRow() + 1
        print(type(self.chat_serial_number))
        self.chat_room_name = chat_room_info[0].text()
        print(self.chat_room_name)
        self.lb_chat_name.setText(str(self.chat_room_name))
        chat_room_personnel = chat_room_info[2].text()
        enter_chat_room_msg = (f"{self.login_user_id}/!&%*|ENTER CHAT ROOM|*%&!/{self.chat_room_name}/{chat_room_personnel}/{self.chat_serial_number}").encode()
        self.client_socket.send(enter_chat_room_msg)
        self.stackedWidget.setCurrentIndex(2)
        self.lw_message.scrollToBottom()

    def go_input_name_page(self):
        self.Thread_exit = True
        exit_msg = (f"{self.login_user_id}/!&%*|EXIT|*%&!").encode()
        self.client_socket.send(exit_msg)
        self.stackedWidget.setCurrentIndex(0)

    def go_main(self):
        self.login_user_id = self.le_name.text()
        self.lb_senders_name.setText(self.login_user_id)
        if self.login_user_id =='':
            QMessageBox.information(self, '사용자', '사용자 정보를 입력해주세요.', QMessageBox.Ok)
            return
        else:
            # ip = '192.168.219.109'
            ip = '10.10.21.104'
            port = 9050
            self.initialize_socket(ip, port)
            self.stackedWidget.setCurrentIndex(1)
            # self.chat_room_update()
            self.Thread_exit = False
            listen_thr = listen_Qthread(self)
            listen_thr.start()
            self.le_name.clear()
    def online_user_update(self,online_user_list):
        self.lw_online_user.clear()
        for i in online_user_list:
            self.lw_online_user.addItem(i[0])
            self.lw_online_user.scrollToBottom()
    def chat_room_stack(self):
        self.sw_open_chat.setCurrentIndex(1)
    def add_chat_room(self):
        chat_name = self.le_chat_room.text()
        self.le_chat_room.clear()
        QMessageBox.information(self,'채팅방', '생성완료',QMessageBox.Ok)
        open_chat_message = (f"{self.login_user_id}/!@|CHATING ROOM OPEN|@!/chat_room_{chat_name}").encode()
        self.client_socket.send(open_chat_message)
    def chat_room_update(self,chat_list):
        self.tw_chat_list.setRowCount(len(chat_list))
        for i in range(len(chat_list)):
            for j in range(0,len(chat_list[i])):
                if j==0:
                    self.tw_chat_list.setItem(i, j, QTableWidgetItem(str(chat_list[i][j]).replace('chat_room_','')))
                    continue
                self.tw_chat_list.setItem(i,j, QTableWidgetItem(str(chat_list[i][j])))
    def chat_exit(self):
        self.lw_message.clear()
        exit_msg = (f"{self.login_user_id}/!&%*|EXIT CHAT|*%&!/{self.chat_room_name}/{self.chat_serial_number}").encode()
        self.client_socket.send(exit_msg)
        self.stackedWidget.setCurrentIndex(1)

    def initialize_socket(self, ip, port):
        '''
        TCP socket을 생성하고 server와 연결
        '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))
        connect_message= (f"{self.login_user_id}/{self.login_user_id}님이 접속했습니다.").encode()
        self.client_socket.send(connect_message)

    def closeEvent(self, QCloseEvent):
        if self.stackedWidget.currentIndex() == 2:
            QCloseEvent.ignore()
            return
        self.Thread_exit = True
        close_msg = (f"{self.login_user_id}/!&%*|CLOSE|*%&!").encode()
        print('exit')
        self.client_socket.send(close_msg)
        print(close_msg)
        self.client_socket.close()
        QCloseEvent.accept()

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
            buf = self.parent.client_socket.recv(8192)
            print('buf')
            if not buf: # 연결이 종료됨
                print('시발')
                break
            buf = buf.decode('utf-8')
            if '@!|USER UPDATE|!@' in buf:
                print('asdkasdjklasdjklasjdklsjalkdjsakldjsakljdklsajkdljsalkdjskladjklsakjd')
                temp = buf.split('/')[1]
                temp2= buf.split('/')[2]
                online_user_list= json.loads(temp)
                chat_list = json.loads(temp2)
                self.parent.online_user_update(online_user_list)
                self.parent.chat_room_update(chat_list)
                continue
            elif '!&%*|ENTER CHAT ROOM|*%&!' in buf:
                temp = buf.split('/!/!/!')[1]
                temp2 = buf.split('/!/!/!')[3]
                chat_data = json.loads(temp)
                chat_list = json.loads(temp2)
                self.parent.chat_room_update(chat_list)
                self.parent.chat_data_update(chat_data)
                continue
            elif '!@|CHATING ROOM UPDATE|@!' in buf:
                a = buf.split('/')[1]
                chat_list= json.loads(a)
                self.parent.chat_room_update(chat_list)
                continue
            elif '!@#|SEND MESSAGE|#@!' in buf:
                message = buf.split('/')[0]
                chat_room = buf.split('/')[2]
                chat_serial_num = buf.split('/')[3]
                print(f"{chat_room} == {self.parent.chat_room_name}      {chat_serial_num}  == {self.parent.chat_serial_number}")
                print(str(chat_room) == str(self.parent.chat_room_name))
                print(str(self.parent.chat_serial_number) == str(chat_serial_num))
                if str(chat_room) == str(self.parent.chat_room_name) and str(self.parent.chat_serial_number) == str(chat_serial_num):
                    self.parent.lw_message.addItem(message)
                self.parent.lw_message.scrollToBottom()
                continue
            elif '!&%*|EXIT CHAT|*%&!' in buf:
                print('!&%*|EXIT CHAT|*%&!')
                message = buf.split('/')[0]
                buf_serial_num = buf.split('/')[2]
                buf_room_name = buf.split('/')[3]
                temp = buf.split('/')[4]
                chat_list = json.loads(temp)
                chat_room = self.parent.lb_chat_name.text()
                if str(chat_room) == str(buf_room_name) and str(self.parent.chat_serial_number) == str(buf_serial_num):
                    self.parent.lw_message.addItem(message)
                self.parent.lw_message.scrollToBottom()
                self.parent.chat_room_update(chat_list)
                continue
        print('소켓해제')
        self.parent.client_socket.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatclient = ChatClient()
    #프로그램 화면을 보여주는 코드
    chatclient.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
