# GUI 클라이언트
import json
from socket import *
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import random
form_class = uic.loadUiType("untitled.ui")[0]

class ChatClient(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(100,100)
        # self.move(600, 100)
        # self.move(1100, 100)
        self.stackedWidget.setCurrentIndex(0)
        self.sw_open_chat.setCurrentIndex(0)
        self.btn_send_message.clicked.connect(self.send_chat)
        self.le_message.returnPressed.connect(self.send_chat)
        self.le_name.returnPressed.connect(self.go_main)
        self.btn_finish.clicked.connect(self.go_main)
        self.btn_exit.clicked.connect(self.chat_exit)
        self.btn_chat_open.clicked.connect(self.chat_room_stack)
        self.btn_room_finish.clicked.connect(self.add_chat_room)
        self.btn_back_input.clicked.connect(self.go_input_name_page)
        self.tw_chat_list.setColumnWidth(0, 141)
        self.tw_chat_list.setColumnWidth(1, 141)
        self.tw_chat_list.setColumnWidth(2, 141)
        self.listen_thr = listen_Qthread(self)
        self.listen_thr.chat_roomname = None
        self.listen_thr.invite_sigal = False
        self.tw_chat_list.cellDoubleClicked.connect(lambda:self.go_chat(invite_signal=False, chat_roomname=None))
        self.btn_invite_O.clicked.connect(lambda:self.go_chat(self.listen_thr.invite_sigal, self.listen_thr.chat_roomname))
        self.btn_invite_X.clicked.connect(self.invite_msg_hide)
        self.btn_chat_delete.clicked.connect(self.chat_delete)
        self.gb_invite_msg.hide()
    def chat_delete(self):
        try:
            chat_room_info = self.tw_chat_list.selectedItems()
            chat_room_name = chat_room_info[0].text()
            chat_room_Founder = chat_room_info[1].text()
            chat_perssonal = chat_room_info[2].text()
            if chat_room_Founder == self.login_user_id and int(chat_perssonal) == 0:
                delete_chat_room = f"{self.login_user_id}\/!@#|DELETE CHAT ROOM|#@!\/{chat_room_name}".encode()
                self.client_socket.send(delete_chat_room)
            elif chat_room_Founder != self.login_user_id:
                QMessageBox.information(self, '개설자','개설자가 아닙니다.', QMessageBox.Ok)
                return
            elif int(chat_perssonal) !='0':
                QMessageBox.information(self, '참여인원', '참여인원이 없는 채팅방만 삭제가능합니다.', QMessageBox.Ok)
        except Exception as a : print(a)


    def send_chat(self): #메시지를 보냈을 때
        message = self.le_message.text() #메시지값 받기
        self.le_message.clear() #메시지 라인에디터 클리어
        #서버에 전송할 메시지 만들어서 인코딩
        send_message_signal= f"{self.login_user_id}\/!@#|SEND MESSAGE|#@!\/{message}\/{self.chat_room_name}".encode()
        #메시지 보내기
        self.client_socket.send(send_message_signal)

    def chat_data_update(self,chat_data): #메시지 업데이트 유저가 메시지를 보냈을 경우
        self.lw_message.clear()
        for i in chat_data:
            if i[3]!= None:
                self.lw_message.addItem(f"{i[0]}  {i[1]}{i[2]}")
                continue
            self.lw_message.addItem(f"{i[0]}  {i[1]}: {i[2]}")
        #리스트 스크롤 아래로
        self.lw_message.scrollToBottom()
    def go_chat(self, invite_signal,chat_roomname): #채팅방 들어갔을 때
        print('초대 bool ',invite_signal,' 채팅방이름=', chat_roomname)
        #메시지 리스트위젯 클리어
        self.lw_message.clear()
        #들어간 채팅방의 정보가져오기
        chat_room_info = self.tw_chat_list.selectedItems()
        #채팅방 이름 담기
        if invite_signal:
            self.chat_room_name = chat_roomname
        else: self.chat_room_name = chat_room_info[0].text()
        print(self.chat_room_name) #확인용 출력
        #들어간 채팅방의 이름으로 라벨 바꿔주기
        self.lb_chat_name.setText(str(self.chat_room_name))
        #서버에 보낼 메시지 만들어서 인코딩
        enter_chat_room_msg = (f"{self.login_user_id}\/!&%*|ENTER CHAT ROOM|*%&!\/{self.chat_room_name}").encode()
        #서버에 메시지 보내기
        self.client_socket.send(enter_chat_room_msg)
        self.stackedWidget.setCurrentIndex(2)
        self.lw_message.scrollToBottom()
        self.invite_msg_hide()

    def go_main(self): #이름 입력 후 메인화면
        #유저 이름 받기
        self.login_user_id = self.le_name.text()
        #라벨 텍스트 유저의 이름으로 바꾸기 채팅방 들어가면 뜸
        self.lb_senders_name.setText(self.login_user_id)
        #이름을 안치고 그냥 엔터쳤을 때 다시 치게 하기
        if self.login_user_id =='':
            QMessageBox.information(self, '사용자', '사용자 정보를 입력해주세요.', QMessageBox.Ok)
            return
        else:
            #ip,port 설정
            # ip = '192.168.219.109'
            ip = '10.10.21.104'
            port = 9050
            #소켓 결합
            self.initialize_socket(ip, port)
            self.stackedWidget.setCurrentIndex(1)
            #쓰레드 실행하기
            self.Thread_exit = False
            # self.listen_thr = listen_Qthread(self)
            self.listen_thr.start()
            self.le_name.clear()

    def go_input_name_page(self):#제일 처음 화면으로
        #쓰레드 멈추는 시그널
        self.Thread_exit = True
        #서버에 보낼 메시지 해당유저의 온라인상태를 오프라인으로 바꾸기 위해 만듬
        exit_msg = (f"{self.login_user_id}\/!&%*|EXIT|*%&!").encode()
        self.client_socket.send(exit_msg)
        self.stackedWidget.setCurrentIndex(0)
    def online_user_update(self,online_user_list): #유저가 온라인 했을 경우
        #온라인 유저목록 클리어
        self.lw_online_user.clear()
        #받아온 온라인된 유저 리스트 위젯에 넣기
        for i in online_user_list:
            self.lw_online_user.addItem(i)
            self.lw_online_user.scrollToBottom()
    def chat_room_stack(self): #채팅방으로 이동하기
        self.sw_open_chat.setCurrentIndex(1)
    def add_chat_room(self): #채팅방 개설
        chat_name = self.le_chat_room_.text()
        self.le_chat_room_.clear()
        #채팅방 개설 메시지 만들어서 인코딩하기
        open_chat_message = (f"{self.login_user_id}\/!@|CHATING ROOM OPEN|@!\/chat_room_{chat_name}").encode()
        self.client_socket.send(open_chat_message)

    def chat_room_update(self,chat_list): #채팅방 업데이트
        #서버에서 받아온 채팅방 테이블위젯에 넣어주기
        self.tw_chat_list.setRowCount(len(chat_list))
        for i in range(len(chat_list)):
            for j in range(len(chat_list[i])):
                if j==0:
                    self.tw_chat_list.setItem(i, j, QTableWidgetItem(str(chat_list[i][j]).replace('chat_room_','')))
                    continue
                else: self.tw_chat_list.setItem(i,j, QTableWidgetItem(str(chat_list[i][j])))
    def chat_exit(self): #유저가 채팅방을 나갔을 경우
        self.lw_message.clear()
        #서버에 보낼 메시지 만들어서 인코딩
        exit_msg = (f"{self.login_user_id}\/!&%*|EXIT CHAT|*%&!\/{self.chat_room_name}").encode()
        self.client_socket.send(exit_msg)
        self.stackedWidget.setCurrentIndex(1)

    def initialize_socket(self, ip, port):
        '''
        TCP socket을 생성하고 server와 연결
        '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip, port))
        connect_message= (f"{self.login_user_id}\/{self.login_user_id}님이 접속했습니다.").encode()
        self.client_socket.send(connect_message)
    def invite_msg_hide(self):
        self.gb_invite_msg.hide()

    def closeEvent(self, QCloseEvent): #유저가 강제종료했을 경우
        #채팅방에서는 종료를 못시키게함
        if self.stackedWidget.currentIndex() == 2:
            QCloseEvent.ignore() #이건 종료하지마라임
            self.chat_exit()
            return
        #채팅방이 아닌 경우에서는 종료시켜야함
        self.Thread_exit = True
        close_msg = (f"{self.login_user_id}\/!&%*|CLOSE|*%&!").encode()
        print(close_msg)
        self.client_socket.send(close_msg)
        self.client_socket.close()
        QCloseEvent.accept() #이건 종료시켜라

class listen_Qthread(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
    def run(self):
        print('쓰레드 시작')
        while True:
            #쓰레드 종료시그널이 True인경우
            if self.parent.Thread_exit:
                print('쓰레드 종료')
                break
            buf = self.parent.client_socket.recv(8192)
            print('buf')
            if not buf: # 연결이 종료됨
                break
            buf = buf.decode('utf-8')
            print(buf)
            if '@!|USER UPDATE|!@' in buf: #유저목록 업데이트
                self.parent.lw_online_user.clear()
                temp = buf.split('\/')[1]
                print('템프:',temp)
                temp2= buf.split('\/')[2]
                print('템프2:',temp2)
                chat_list = json.loads(temp2)
                if temp == '온라인 유저 없음':
                    print(temp)
                    self.parent.lw_online_user.clear()
                    self.parent.chat_room_update(chat_list)
                else:
                    print('템프: ',temp)
                    online_user_list = json.loads(temp)
                    print('템프: ',temp)
                    self.parent.online_user_update(online_user_list)
                    self.parent.chat_room_update(chat_list)
                continue
            elif '!&%*|UPDATE CHAT ROOM|*%&!' in buf:
                buf_name = buf.split('\/')[0]
                temp = buf.split('\/')[2]
                del_chat_room_name = buf.split('\/')[3]
                update_chat_list = json.loads(temp)
                self.parent.chat_room_update(update_chat_list)
                if self.parent.login_user_id == buf_name:
                    self.parent.lb_open_room.setText(f'채팅방 {del_chat_room_name}을 삭제했습니다.')
            elif '!&%*|ENTER CHAT ROOM|*%&!' in buf: #유저가 채팅방을 들어갔을 경우
                temp = buf.split('\/')[1]
                temp2 = buf.split('\/')[3]
                #유저목록과 채팅방목록 json객체를 변환해서 변수에 담기 !리스트로 들어감!
                chat_data = json.loads(temp)
                chat_list = json.loads(temp2)
                self.parent.chat_data_update(chat_data)
                self.parent.chat_room_update(chat_list)
                self.parent.lb_open_room.setText('')
                continue
            elif '!@|CHATING ROOM UPDATE|@!' in buf: #유저가 채팅방을 만들었을 경우
                a = buf.split('\/')[1]
                chat_list= json.loads(a)
                self.parent.chat_room_update(chat_list)
                self.parent.lb_open_room.setText('')
                continue
            elif f"!@|USED CHATING ROOM NAME|@!" in buf: #채팅방이름 중복됐을 경우
                buf_name= buf.split('\/')[0]
                print("self.parent.login_user_id",self.parent.login_user_id)
                print("buf_name:",buf_name)
                if self.parent.login_user_id == buf_name:
                    self.parent.lb_open_room.setText('사용중인 채팅방이름입니다.')
            elif '!@#|SEND MESSAGE|#@!' in buf: #유저가 메시지를 보냈을 경우
                message = buf.split('\/')[0]
                chat_room = buf.split('\/')[2]
                #유저가 메시지를 보낸 채팅방과 들어가있는 채팅방이 같을 경우만 리스트위젯에 넣어주는건데 채팅방별로 테이블을 만들어서 나중에 이거없애야함
                if chat_room == self.parent.chat_room_name:
                    self.parent.lw_message.addItem(message)
                #업데이트 됐을 때 스크롤 내려주는거
                self.parent.lw_message.scrollToBottom()
                continue
            elif '!&%*|EXIT CHAT|*%&!' in buf: #유저가 채팅방을 나갔을 때 참여인원이 줄어들었으니 채팅목록 업데이트하기
                print('!&%*|EXIT CHAT|*%&!')
                message = buf.split('\/')[0]
                buf_room_name = buf.split('\/')[2]
                temp = buf.split('\/')[3]
                chat_list = json.loads(temp)
                chat_room = self.parent.lb_chat_name.text()
                print("chat_room:", chat_room, type(chat_room))
                print('buf:',buf_room_name, type(buf_room_name))
                # 채팅방을 나갔습니다. 메시지 넣어주기
                if chat_room == buf_room_name.replace("chat_room_",""):
                    self.parent.lw_message.addItem(message)
                self.parent.lw_message.scrollToBottom()
                #업데이트된 채팅방 목록 테이블 위젯에 넣어주기
                self.parent.chat_room_update(chat_list)
                continue
            elif '!@#|INVITE SIGNAL|#!@' in buf: #초대를 받았을 경우
                self.parent.gb_invite_msg.show()
                self.invite_sigal= True
                self.chat_roomname = buf.split('/')[3]
                invite_msg = buf.split('/')[4]
                self.parent.lb_invite_msg.setText(invite_msg)
        print('소켓해제')
        self.parent.client_socket.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatclient = ChatClient()
    #프로그램 화면을 보여주는 코드
    chatclient.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
