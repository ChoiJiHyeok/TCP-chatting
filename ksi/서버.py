from socket import *
from threading import *
import pymysql
import json

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
            # if client not in self.clients:
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
                    msg = incoming_message.decode('utf-8')
                    user_name = msg.split('/')[0]
                    self.final_received_message = msg.split('/')[1].encode()
                    if user_name not in self.clients_name:
                        self.clients_name.append(user_name)
                        print('온라인:', *self.clients_name)
                        cursor.execute(f"select * from online_user")
                        a = cursor.fetchall()
                        cursor.execute(f"select * from chat_list")
                        b = cursor.fetchall()
                        user_name_list = json.dumps(a)
                        chat_list = json.dumps(b)
                        self.connect_user_msg = f'{"@!|USER CONNECT|!@"}/{user_name_list}/{chat_list}'.encode()
                        self.online_user_info(self.clients)
                        continue

                    if f"!&%*|EXIT|*%&!" in msg or f'!&%*|CLOSE|*%&!' in msg:
                        index =self.clients.index(client)
                        self.clients.remove(self.clients[index])
                        self.clients_name.remove(user_name)
                        print(f'클라이언트이름 리스트',*self.clients_name)
                        self.final_received_message = msg
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
                        cursor.execute(f"insert into chat_list (채팅방이름,개설자,참여인원) values ('{chat_name}','{user_name}','{str(1)}')")
                        print('테이블생성')
                        conn.commit()
                        print('커밋')
                        cursor.execute(f"select * from chat_list")
                        print('셀렉트')
                        a = cursor.fetchall()
                        conn.close()
                        chat_list = json.dumps(a)
                        self.final_received_message = f"!@|CHATING ROOM OPEN|@!/{chat_list}".encode()
                    self.send_all_clients(self.clients)
                except ValueError as er: print(er)
        c_socket.close()
    # 송신 클라이언트를 제외한 모든 클라이언트에게 메시지 전송
    def send_all_clients(self,clients):
        for client in clients: # 목록에 있는 모든 소켓에 대해
            socket, (ip,port) = client
            # if f"!&%*|EXIT|*%&!" in self.final_received_message:
            #     self.final_received_message = f"{self.final_received_message.split('/')[0]}님이 채팅방을 나가셨습니다."
            socket.sendall(self.final_received_message)
    def online_user_info(self,clients):
        for client in clients: # 목록에 있는 모든 소켓에 대해
            socket, (ip,port) = client
            socket.sendall(self.connect_user_msg)



if __name__ == '__main__':
    MultiChatServer()