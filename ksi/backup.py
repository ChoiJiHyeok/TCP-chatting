from socket import *
from threading import *
import pymysql
import json
import datetime


class MultiChatServer:
    # 소켓을 생성하고 연결되면 accept_client() 호출
    def __init__(self):
        self.clients = []  # 접속된 클라이언트 소켓 목록
        self.clients_name = []  # 접속된 클라이언트 이름
        self.final_received_message = ""  # 최종 수신 메시지
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip = '10.10.21.104'  # 실습실 컴퓨터 IP
        # self.ip = '192.168.219.109' #기숙사 컴퓨터 IP
        self.port = 9050  # 포트번호 9000~9100 중 아무거나 클라이언트랑은 맞춰야됨
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 소켓 옵션제어
        self.s_sock.bind((self.ip, self.port))  # 소켓 결합
        print("클라이언트 대기중...")
        self.s_sock.listen(100)  # 소켓 연결 제한
        self.accept_client()  # accept_client 메서드 실행

    # 연결 클라이언트 소켓을 목록에 추가하고 스레드를 생성하여 데이터를 수신한다
    def accept_client(self):  # 접속소켓을 허용한다는 거임
        while True:
            client = c_socket, (ip, port) = self.s_sock.accept()
            self.clients.append(client)  # 접속된 소켓을 목록에 추가
            print(self.clients)
            print(ip, ':', str(port), '가 연결되었습니다')  # 연결 확인
            cth = Thread(target=self.receive_messages, args=(c_socket, client), daemon=True)  # 수신스레드
            cth.start()  # 스레드 시작

    # 데이터를 수신하여 모든 클라이언트에게 전송한다
    def receive_messages(self, c_socket, client):
        while True:
            try:
                incoming_message = c_socket.recv(256)  # 클라에서 보낸 메시지 받기
                if not incoming_message:  # 연결이 종료됨
                    break
            except:
                continue
            else:
                try:
                    conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='net',
                                           charset='utf8')
                    cursor = conn.cursor()
                    msg = incoming_message.decode()  # 클라에서 보낸 메시지를 decode
                    print(msg)  # 메시지 확인
                    user_name = msg.split('\/')[0]  # 클라에서 보낸 메시지는 \/로 구분하는데 이걸 split함수로 쪼개서 이름에 해당하는 부분을 변수에 넣어줌
                    self.final_received_message = msg.split('\/')[1].encode()
                    now = datetime.datetime.now()  # DB에 넣을 시간 받아주기
                    date = now.strftime('%y-%m-%d')  # datetime 객체를 str로 변환
                    time = now.strftime('%H:%M')
                    if user_name not in self.clients_name or f"!&%*|EXIT|*%&!" in msg or f'!&%*|CLOSE|*%&!' in msg:  # 새로 연결된 소켓이거나 서버에서 보낸 메시지가 exit or close 일 경우
                        if f"!&%*|EXIT|*%&!" in msg or f'!&%*|CLOSE|*%&!' in msg:  # 서버에서 보낸 메시지가 exit or close 일 경우
                            index = self.clients.index(client)  # 해당하는 인덱스값 찾아주기
                            self.clients.remove(self.clients[index])  # 찾은 인덱스값을 연결된 소켓리스트에서 제거하기
                            self.clients_name.remove(user_name)  # 이건 내가 접속한 유저 이름들 확인하려고 만든 리스트에서 마찬가지로 제거하기
                            print(f'온라인 유저', *self.clients_name)  # 접속유저 확인하기 및 잘 제거 됐는지 확인
                            print(f'{user_name} 접속 종료')  # 접속종료한 유저이름 확인하기
                            cursor.execute(
                                f"delete from net.online_user where 이름 = '{user_name}';")  # 온라인 유저 DB에서 해당하는 유저 DB 삭제하기
                            conn.commit()  # 저장하기
                        else:
                            self.clients_name.append(user_name)  # 새로연결된 유저일 경우
                            print('온라인 유저', *self.clients_name)  # 온라인유저 확인용 출력
                            cursor.execute(f"insert into online_user (이름) values ('{user_name}')")  # 온라인 유저DB에 유저 추가해주기
                            conn.commit()  # 저장하기
                        # 유저가 나가거나 들어오면 온라인유저목록, 채팅방 목록 업데이트 해줘야해서 DB에서 가져옴
                        cursor.execute(f"select * from online_user")
                        a = cursor.fetchall()
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list")
                        b = cursor.fetchall()
                        # 클라이언트한테 보낼 때 리스트 형식으로 보내야하는데 그냥 보내면 안보내져서 json 객체로 변환해주기 import json 해야됨
                        user_name_list = json.dumps(a)
                        chat_list = json.dumps(b)
                        # 클라이언트에게 보낼 메시지에 필요한 목록들 인코딩하기
                        self.final_received_message = f'{"@!|USER UPDATE|!@"}\/{user_name_list}\/{chat_list}'.encode()
                    elif f"!&%*|EXIT CHAT|*%&!" in msg:  # 유저가 채팅방을 나갈경우
                        chat_room_name = msg.split('\/')[2]  # 유저가 나간 채팅방 split으로 변수에 담아줌
                        # DB 업데이트 및 해당유저가 채팅방을 나갔다는 내용을 채팅방인원들에게 알려야해서 DB에 저장하기
                        cursor.execute(f"update chat_list set 참여인원 = 참여인원-1 where 채팅방이름='chat_room_{chat_room_name}'")
                        cursor.execute(
                            f"insert into chat_room_{chat_room_name} values('{date}','{time}','{user_name}','님이 채팅방을 나가셨습니다.','{chat_room_name}','퇴장')")
                        conn.commit()  # 수정한 값 저장하기
                        cursor.execute(
                            f"select 채팅방이름,개설자,참여인원 from chat_list")  # 채팅방 업데이트를 하기위해 채팅목록 가져오기 참여인원이 수정되어서 다시 불러와야함
                        a = cursor.fetchall()
                        print(a)  # 확인용 출력
                        chat_list = json.dumps(a)  # 리스트를 클라이언트에게 보내기위해서 json 객체로 변환
                        print(f"{user_name}이 {chat_room_name} 채팅방을 나갔습니다.")  # 서버 콘솔로 확인하기 위한 출력
                        # 클라에게 보낼 메시지 만들어서 인코딩하기
                        self.final_received_message = f"{time}   {user_name}님이 채팅방을 나가셨습니다.\/!&%*|EXIT CHAT|*%&!\/{chat_room_name}\/{chat_list}".encode()
                        # 채팅방 개설
                    elif f"!@|CHATING ROOM OPEN|@!" in msg:  # 유저가 채팅방을 개설 했을 경우
                        chat_name = msg.split('\/')[2]  # 채팅방이름 변수에 담아주기
                        # 채팅방 중복검색
                        cursor.execute(f"select 채팅방이름 from chat_list")
                        a = cursor.fetchall()
                        used_chat_room_signal = False
                        for i in a:

                            if i[0] == chat_name:
                                print('조건문')
                                self.final_received_message = f"{user_name}\/!@|USED CHATING ROOM NAME|@!".encode()
                                self.send_all_clients(self.clients)
                                used_chat_room_signal = True
                                break
                        if used_chat_room_signal:
                            continue
                        # 채팅방 테이블 만들기, 채팅방리스트에 넣기
                        cursor.execute(f"create table {chat_name} ("
                                       f"날짜 VARCHAR(45),"
                                       f"시간 VARCHAR(45),"
                                       f"송신자 VARCHAR(45),"
                                       f"내용 VARCHAR(100),"
                                       f"채팅방 VARCHAR(45),"
                                       f"알림 VARCHAR(45)"
                                       f") ENGINE=InnoDB CHARSET=utf8;")
                        print('테이블생성')
                        # 채팅방 목록에 넣어주기 쿼리문이 많은 건 프로시저나 트리거로 만들어야하는데 지금은 그냥 함
                        cursor.execute(
                            f"insert into chat_list (채팅방이름,개설자,참여인원) values ('{chat_name}','{user_name}','0')")
                        conn.commit()  # 수정내용 저장하기
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list")  # 채팅목록 업데이트 하기 위해 가져오기
                        a = cursor.fetchall()
                        conn.close()
                        chat_list = json.dumps(a)  # 리스트를 클라이언트에게 보내기위해서 json 객체로 변환
                        self.final_received_message = f"!@|CHATING ROOM UPDATE|@!\/{chat_list}".encode()  # 유저들에게 보낼 메시지 만들어서 인코딩
                        print(f"{user_name} 채팅방목록 업데이트")  # 서버 콘솔 확인용 출력
                    elif f"!&%*|ENTER CHAT ROOM|*%&!" in msg:  # 유저가 채팅방에 들어갔을 경우인데 로직 바껴서 수정해야함 일단 둠
                        chat_room_name = msg.split('\/')[2]  # 해당 채팅방이름 담아두기
                        # chat_room_personnel = msg.split('\/')[3]+1 #채팅방 인원 더 해준 값을 변수에 담아줌
                        # print(chat_room_personnel,type(chat_room_personnel)) #확인용 출력
                        # 유저들에게 입장안내 메시지 DB에 넣고 채팅방 참여인원 업데이트
                        cursor.execute(
                            f"insert into chat_room_{chat_room_name} values('{date}','{time}','{user_name}','님이 입장하셨습니다.','{chat_room_name}','입장')")
                        cursor.execute(f"update chat_list set 참여인원= 참여인원+1 where 채팅방이름='chat_room_{chat_room_name}'")
                        conn.commit()  # 수정값 저장
                        # 채팅메시지 DB 가져와서 json으로 변환
                        cursor.execute(f"select 시간,송신자,내용,알림 from chat_room_{chat_room_name}")
                        temp = cursor.fetchall()
                        chat_data = json.dumps(temp)
                        # 업데이트할 채팅방 목록 가져와서 json으로 변환
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list")
                        a = cursor.fetchall()
                        chat_list = json.dumps(a)
                        # 유저에게 전송할 메시지 만들어서 인코딩
                        self.final_received_message = f"!&%*|ENTER CHAT ROOM|*%&!\/{chat_data}\/{chat_room_name}\/{chat_list}".encode()
                        print(f"{user_name}이 {chat_room_name} 채팅방에 들어갔습니다.")  # 확인용 출력
                    elif f"!@#|SEND MESSAGE|#@!" in msg:  # 유저가 메시지를 보낼경우
                        # 필요한 값들 변수에 저장하기
                        message = msg.split('\/')[2]
                        chat_room_name = msg.split('\/')[3]
                        if '/초대' in message:
                            invite_send_index = self.clients_name.index(user_name)  # 초대한 사람 찾기
                            invite_send_sock = self.clients[invite_send_index]  # 초대한 사람 소켓 찾기
                            invite_recv_name = message.split(' ')[1]  # 초대받은 사람 이름
                            invite_recv_index = self.clients_name.index(invite_recv_name)  # 초대 받은 사람 찾기
                            invite_recv_sock = self.clients[invite_recv_index]  # 초대 받은 사람 소켓 찾기
                            self.invite_msg = f'{user_name}/!@#|INVITE SIGNAL|#!@/{invite_recv_name}/{chat_room_name}/{user_name}님이\n{chat_room_name}으로\n{invite_recv_name}님을 초대했습니다.'.encode()
                            self.send_invite_client(invite_recv_sock)
                            continue
                        # 저장된 값으로 메시지DB 추가해주기
                        cursor.execute(
                            f"insert into chat_room_{chat_room_name} (날짜,시간,송신자,내용,채팅방) values ('{date}','{time}','{user_name}','{message}','{chat_room_name}')")
                        conn.commit()  # 수정값 저장
                        # 유저들에게 보낼 메시지 만들어서 인코딩하기
                        self.final_received_message = f"{time}   {user_name}: {message}\/!@#|SEND MESSAGE|#@!\/{chat_room_name}".encode()

                    print(self.final_received_message.decode())
                    self.send_all_clients(self.clients)
                except Exception as er:
                    print(er)  # 오류 출력
        # 소켓 닫기
        c_socket.close()

    def send_all_clients(self, clients):
        for client in clients:  # 목록에 있는 모든 소켓에 대해 위에서 만든 메시지 보내기
            socket, (ip, port) = client
            socket.sendall(self.final_received_message)

    def send_invite_client(self, r_socket):
        socket, (ip, port) = r_socket
        socket.sendall(self.invite_msg)


if __name__ == '__main__':
    MultiChatServer()
















#클라이언트


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
        self.btn_room_fns.clicked.connect(self.add_chat_room)
        self.btn_back_input.clicked.connect(self.go_input_name_page)
        self.tw_chat_list.setColumnWidth(0, 141)
        self.tw_chat_list.setColumnWidth(1, 141)
        self.tw_chat_list.setColumnWidth(2, 141)
        self.listen_thr = listen_Qthread(self)
        self.listen_thr.chat_roomname=None
        self.listen_thr.invite_sigal=False
        self.tw_chat_list.cellDoubleClicked.connect(lambda:self.go_chat(invite_signal=False, chat_roomname=None))
        self.btn_invite_O.clicked.connect(lambda:self.go_chat(self.listen_thr.invite_sigal, self.listen_thr.chat_roomname))
        self.btn_invite_X.clicked.connect(self.invite_msg_hide)
        self.gb_invite_msg.hide()

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
        print('초대 받음')
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

    def go_input_name_page(self):#제일 처음 화면으로
        #쓰레드 멈추는 시그널
        self.Thread_exit = True
        #서버에 보낼 메시지 해당유저의 온라인상태를 오프라인으로 바꾸기 위해 만듬
        exit_msg = (f"{self.login_user_id}\/!&%*|EXIT|*%&!").encode()
        self.client_socket.send(exit_msg)
        self.stackedWidget.setCurrentIndex(0)

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
    def online_user_update(self,online_user_list): #유저가 온라인 했을 경우
        #온라인 유저목록 클리어
        self.lw_online_user.clear()
        #받아온 온라인된 유저 리스트 위젯에 넣기
        for i in online_user_list:
            self.lw_online_user.addItem(i[0])
            self.lw_online_user.scrollToBottom()
    def chat_room_stack(self): #채팅방으로 이동하기
        self.sw_open_chat.setCurrentIndex(1)
    def add_chat_room(self): #채팅방 개설
        chat_name = self.le_chat_room.text()
        self.le_chat_room.clear()
        chat_num = '{:04d}'.format(random.randint(0, 9999))
        #채팅방 개설 메시지 만들어서 인코딩하기
        open_chat_message = (f"{self.login_user_id}\/!@|CHATING ROOM OPEN|@!\/chat_room_{chat_name}\/{chat_num}").encode()
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
                temp = buf.split('\/')[1]
                temp2= buf.split('\/')[2]
                online_user_list= json.loads(temp)
                chat_list = json.loads(temp2)
                self.parent.online_user_update(online_user_list)
                self.parent.chat_room_update(chat_list)
                continue
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
            elif '!@|CHATING ROOM UPDATE|@!' in buf: #유저가 채팅방을 만들었을경우
                a = buf.split('\/')[1]
                chat_list= json.loads(a)
                self.parent.chat_room_update(chat_list)
                self.parent.lb_open_room.setText('')
                continue
            elif f"!@|USED CHATING ROOM NAME|@!" in buf:
                buf_name= buf.split('\/')[0]
                print("self.parent.login_user_id",self.parent.login_user_id)
                print("buf_name:",buf_name)
                if self.parent.login_user_id == buf_name:
                    self.parent.lb_open_room.setText('사용중인 채팅방이름입니다.')
            elif '!@#|SEND MESSAGE|#@!' in buf: #유저가 메시지를 보냈을 경우
                message = buf.split('\/')[0]
                chat_room = buf.split('\/')[2]
                #유저가 메시지를 보낸 채팅방과 들어가있는 채팅방이 같을 경우만 리스트위젯에 넣어주는건데 채팅방별로 테이블을 만들어서 나중에 이거없애야함
                if str(chat_room) == str(self.parent.chat_room_name):
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
            elif '!@#|INVITE SIGNAL|#!@' in buf:
                self.parent.gb_invite_msg.show()
                self.invite_sigal= True
                self.chat_roomname = buf.split('/')[3]
                invite_msg = buf.split('/')[4]
                self.parent.lb_invite_msg.setText(invite_msg)


            #f'{user_name}/!@#|INVITE SIGNAL|#!@/{invite_recv_name}/{chat_room_name}/{user_name}님이 {chat_room_name}으로 {invite_recv_name}님을 초대했습니다.'.encode()
            # go_chat(self, invite_signal, chat_roomname):  # 채팅방 들어갔을 때

        print('소켓해제')
        self.parent.client_socket.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatclient = ChatClient()
    #프로그램 화면을 보여주는 코드
    chatclient.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
