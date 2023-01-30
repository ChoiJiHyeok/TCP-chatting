# GUI 클라이언트
from socket import *
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

form_class = uic.loadUiType("untitled.ui")[0]

class ChatClient(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(1100, 100)
        self.stackedWidget.setCurrentIndex(0)
        self.le_send.returnPressed.connect(self.go_chat)
        self.btn_send_message.clicked.connect(self.send_chat)
        self.le_message.returnPressed.connect(self.send_chat)
        self.btn_finish.clicked.connect(self.go_chat)
        self.btn_exit.clicked.connect(self.chat_exit)
        self.connect_signal = False

    def chat_exit(self):
        exit_msg = (f"{self.sender_name}/!&%*|EXIT|*%&!").encode('utf-8')
        self.client_socket.send(exit_msg)
        self.stackedWidget.setCurrentIndex(0)
        self.Thread_exit = True

    def go_chat(self):
        self.lw_message.clear()
        self.sender_name = self.le_send.text()
        self.lb_senders_name.setText(self.sender_name)
        if self.sender_name == '':
            QMessageBox.information(self, '사용자', '사용자 정보를 입력해주세요.', QMessageBox.Ok)
            return
        else:
            ip = '10.10.21.104'
            # ip = '192.168.219.109'
            port = 8000
            self.initialize_socket(ip, port)
            self.stackedWidget.setCurrentIndex(1)
            self.Thread_exit = False
            listen_thr = listen_Qthread(self)
            listen_thr.start()
            self.le_send.clear()

    def initialize_socket(self, ip, port):
        '''
        TCP socket을 생성하고 server와 연결
        '''
        pass
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))
        connect_message = (f"{self.sender_name}/{self.sender_name}님이 입장하였습니다.").encode('utf-8')
        self.client_socket.send(connect_message)

    def send_chat(self):
        '''
        message를 전송하는 버튼 콜백 함수
        '''
        message = self.le_message.text()
        if message == "":
            return
        else:
            self.le_message.clear()
            message = (f"{self.sender_name}/{self.sender_name}: {message}").encode('utf-8')
            self.client_socket.send(message)

    def closeEvent(self, QCloseEvent):
        exit_msg = (f"{self.sender_name}/!&%*|EXIT|*%&!").encode('utf-8')
        self.Thread_exit = True
        self.client_socket.send(exit_msg)
        QCloseEvent.accept()

class listen_Qthread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        print('쓰레드 시작')
        while True:
            if self.parent.Thread_exit:
                print('쓰레드 종료')
                break
            else:
                buf = self.parent.client_socket.recv(1024)
                print('쓰레드')
                if not buf:  # 연결이 종료됨
                    break
                self.parent.lw_message.addItem(buf.decode('utf-8'))
                self.parent.lw_message.scrollToBottom()
        self.parent.client_socket.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatclient = ChatClient()
    # 프로그램 화면을 보여주는 코드
    chatclient.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

