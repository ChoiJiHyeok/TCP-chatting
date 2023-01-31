from socket import *
from threading import *
import pymysql
import json
import datetime

class MultiChatServer:
    # 소켓을 생성하고 연결되면 accept_client() 호출
    def __init__(self):
        self.clients = [] #접속된 클라이언트 소켓 목록
        self.clients_name=[] #접속된 클라이언트 이름
        self.final_received_message = "" # 최종 수신 메시지
        self.s_sock = socket(AF_INET, SOCK_STREAM)
        self.ip = '10.10.21.104'
        # self.ip = '192.168.219.109'
        self.port = 9050
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        print("클라이언트 대기중...")
        self.s_sock.listen(100)
        self.accept_client()

    # 연결 클라이언트 소켓을 목록에 추가하고 스레드를 생성하여 데이터를 수신한다
    def accept_client(self):
        while True:
            client = c_socket, (ip,port) = self.s_sock.accept()
            self.clients.append(client) # 접속된 소켓을 목록에 추가
            print(self.clients)
            print(ip,':', str(port),'가 연결되었습니다')
            cth = Thread(target=self.receive_messages, args=(c_socket,client)) # 수신스레드
            cth.start() # 스레드 시작
    # 데이터를 수신하여 모든 클라이언트에게 전송한다
    def receive_messages(self, c_socket,client):
        while True:
            try:
                incoming_message = c_socket.recv(256)
                if not incoming_message: # 연결이 종료됨
                    break
            except:
                continue
            else:
                try:
                    conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='net',
                                           charset='utf8')
                    cursor = conn.cursor()
                    msg = incoming_message.decode()
                    print(msg)
                    user_name = msg.split('/')[0]
                    self.final_received_message = msg.split('/')[1].encode()
                    now = datetime.datetime.now()
                    date = now.strftime('%y-%m-%d')
                    time = now.strftime('%H:%M')
                    if user_name not in self.clients_name or f"!&%*|EXIT|*%&!" in msg or f'!&%*|CLOSE|*%&!' in msg:
                        if f"!&%*|EXIT|*%&!" in msg or f'!&%*|CLOSE|*%&!' in msg:
                            index = self.clients.index(client)
                            self.clients.remove(self.clients[index])
                            self.clients_name.remove(user_name)
                            print(f'온라인 유저', *self.clients_name)
                            print(f'{user_name} 접속 종료')
                            cursor.execute(f"delete from net.online_user where 이름 = '{user_name}';")
                            conn.commit()
                        else:
                            self.clients_name.append(user_name)
                            print('온라인 유저', *self.clients_name)
                            cursor.execute(f"insert into online_user (이름) values ('{user_name}')")
                            conn.commit()
                        cursor.execute(f"select * from online_user")
                        a = cursor.fetchall()
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list")
                        b = cursor.fetchall()
                        user_name_list = json.dumps(a)
                        chat_list = json.dumps(b)
                        self.final_received_message = f'{"@!|USER UPDATE|!@"}/{user_name_list}/{chat_list}'.encode()
                    elif f"!&%*|EXIT CHAT|*%&!" in msg:
                        chat_room_name = msg.split('/')[2]
                        chat_serial_number = int(msg.split('/')[3])
                        cursor.execute(f"select 참여인원 from chat_list where 채팅방이름='chat_room_{chat_room_name}' and 연번={chat_serial_number}")
                        personnel = cursor.fetchone()
                        temp= str(int(personnel[0])-1)
                        print(temp)
                        cursor.execute(f"update chat_list set 참여인원='{temp}' where 연번={chat_serial_number} and 채팅방이름='{chat_room_name}'")
                        cursor.execute(f"insert into net_chat values('{date}','{time}','{user_name}','님이 채팅방을 나가셨습니다.','{chat_room_name}','{chat_serial_number}','퇴장')")
                        conn.commit()
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list")
                        a = cursor.fetchall()
                        print(a)
                        chat_list = json.dumps(a)
                        print(f"{user_name}이 {chat_room_name} 채팅방을 나갔습니다.")
                        self.final_received_message = f"{time}   {user_name}님이 채팅방을 나가셨습니다./!&%*|EXIT CHAT|*%&!/{chat_room_name}/{chat_serial_number}/{chat_list}".encode()
                        #채팅방 개설
                    elif f"!@|CHATING ROOM OPEN|@!" in msg:
                        chat_name = msg.split('/')[2]
                        #채팅방 테이블 만들기, 채팅방리스트에 넣기
                        cursor.execute(f"create table {chat_name} ("
                                            f"날짜 VARCHAR(45),"
                                            f"시간 VARCHAR(45),"
                                            f"송신자 VARCHAR(45),"
                                            f"수신자 VARCHAR(45),"
                                            f"내용 VARCHAR(100)"
                                            f") ENGINE=InnoDB CHARSET=utf8;")
                        print('테이블생성')
                        cursor.execute(f"insert into chat_list (채팅방이름,개설자,참여인원) values ('{chat_name}','{user_name}','0')")
                        conn.commit()
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list")
                        a = cursor.fetchall()
                        conn.close()
                        chat_list = json.dumps(a)
                        self.final_received_message = f"!@|CHATING ROOM UPDATE|@!/{chat_list}".encode()
                        print(f"{user_name} 채팅방목록 업데이트")
                    elif f"!&%*|ENTER CHAT ROOM|*%&!" in msg:
                        chat_room_name = msg.split('/')[2]
                        chat_room_personnel = int(msg.split('/')[3])+1
                        print(chat_room_personnel,type(chat_room_personnel))
                        chat_serial_number = int(msg.split('/')[4])
                        cursor.execute(f"insert into net_chat values('{date}','{time}','{user_name}','님이 입장하셨습니다.','{chat_room_name}',{chat_serial_number},'입장')")
                        cursor.execute(f"update chat_list set 참여인원='{str(chat_room_personnel)}' where 채팅방이름='chat_room_{chat_room_name}' and 연번={chat_serial_number}")
                        conn.commit()
                        cursor.execute(f"select 시간,송신자,내용,알림 from net_chat where 채팅방='{chat_room_name}' and 채팅방연번={chat_serial_number}")
                        temp = cursor.fetchall()
                        chat_data = json.dumps(temp)
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list")
                        a = cursor.fetchall()
                        chat_list = json.dumps(a)
                        self.final_received_message = f"!&%*|ENTER CHAT ROOM|*%&!/!/!/!{chat_data}/!/!/!{chat_room_name}/!/!/!{chat_list}".encode()
                        print(f"{user_name}이 {chat_room_name} 채팅방에 들어갔습니다.")
                    elif f"!@#|SEND MESSAGE|#@!" in msg:
                        message = msg.split('/')[2]
                        chat_room_name = msg.split('/')[3]
                        chat_serial_number = str(msg.split('/')[4])
                        cursor.execute(f"insert into net_chat (날짜,시간,송신자,내용,채팅방,채팅방연번) values ('{date}','{time}','{user_name}','{message}','{chat_room_name}','{chat_serial_number}')")
                        conn.commit()
                        self.final_received_message = f"{time}   {user_name}: {message}/!@#|SEND MESSAGE|#@!/{chat_room_name}/{chat_serial_number}".encode()
                        print(self.final_received_message.decode())
                    self.send_all_clients(self.clients)
                except ValueError as er: print(er)
        c_socket.close()
    # 송신 클라이언트를 제외한 모든 클라이언트에게 메시지 전송
    def send_all_clients(self,clients):
        for client in clients: # 목록에 있는 모든 소켓에 대해
            socket, (ip,port) = client
            socket.sendall(self.final_received_message)



if __name__ == '__main__':
    MultiChatServer()