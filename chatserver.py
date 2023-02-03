from socket import *
from threading import *
import json
import pymysql as p

class MultiChatServer:

    #소켓을 생성하고 연결되면 accept_client() 호출
    def __init__(self):
        self.clients=[] # 접속된 클라이언트 소켓 목록
        self.final_received_message="" #최종수신 메시지
        self.final_received_signal=""#최종수신 로그인 신호

        # self.final_received_userlist=[]#최종수신 userlist
        self.s_sock=socket(AF_INET, SOCK_STREAM)
        self.ip='10.10.21.105'
        self.port=9001
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        self.s_sock.bind((self.ip, self.port))
        print("클라이언트 대기 중...")
        self.s_sock.listen(100)
        self.accept_client()

    def accept_client(self):
        while True:
            client = c_socket, (ip, port)= self.s_sock.accept()
            if client not in self.clients:
                self.clients.append(client)
            print(ip,':',str(port),'가 연결되었습니다')
            cth=Thread(target=self.receive_messages, args=(c_socket,))
            cth.start()

    # def send_chatroom(self, info_chatroom2,alert):
    #     if info_chatroom2:
    #         trans_room=json.dumps(info_chatroom2)+'ch##'
    #         return trans_room
    #     elif alert:
    #         return alert


    #데이터를 수신하여 모든 클라이언트에게 전송한다
    def receive_messages(self, c_socket):
        while True:
            try:
                incoming_message = c_socket.recv(256)
                if not incoming_message:
                    break
            except:
                continue
            else:
                self.final_received_message=incoming_message.decode('utf-8')
                print(self.final_received_message)
                self.send_all_clients(c_socket)
                conn = p.connect(host='localhost', user='root', password='chlwlgur', db='chatting', charset='utf8')
                # conn = p.connect(host='localhost', user='root', password='chlwlgur', db='population', charset='utf8')
                c = conn.cursor()

                # c.execute('SELECT *FROM new_table')
                # find_log=c.fetchall()
                # print(find_log)
                c.execute('SELECT *FROM chatroom');
                info_chatroom1=c.fetchall()
                if '!!' in self.final_received_message :
                    try :  #  db에 roooname(primary key) 값이 중복 되면 발생하는 에러 예외처리
                        print(f'{self.final_received_message[2:]}')
                        c.callproc('MAKE_ROOM',[f'{self.final_received_message[2:]}'])
                        print('채팅방 추가')
                    except:
                        pass
                else:
                    pass
                c.execute('SELECT *FROM chatroom');
                # string='ch##'
                # tuple=(string,)
                info_chatroom2=str(c.fetchall())
                send_chat_info=json.dumps('ch##'+info_chatroom2)

                print(info_chatroom2,'gg')
                print(self.final_received_message,'gigi')
                c_socket.sendall(send_chat_info)
                # if find_log == ():
                #     if '@@' not in self.final_received_message: # 접속 명단 추가
                #         # c.execute(f'UPDATE new_table SET aa = "{self.final_received_message}"');
                #         c.execute(f'INSERT INTO new_table (aa) VALUES ("{self.final_received_message}")');
                #         print('메시지 저장 1')
                #     else:
                #         print('메시지 확인 1')
                #         pass
                # else:
                #     if '@@' not in self.final_received_message:
                #               # c.execute(f'UPDATE POPULATION.NEW_TABLE SET aa = concat(aa, ",{self.final_received_message}"');
                #         c.execute(f'INSERT INTO new_table (aa) VALUES ("{self.final_received_message}")');
                #         print('message confirm')
                #     else:
                #         pass
                #         print('message 12')
                conn.commit()
                conn.close()
                # return info_chatroom2

        c_socket.close()

    # def send_chatroom(self, info_chatroom2): #채팅방 db 모든 클라이언트에게
    #     for client in self.clients:
    #         socket, (ip, port) = client
    #         try:
    #             socket.sendall(info_chatroom2)
    #         except:
    #             self.clients.remove(client)
    #             print('{},{} 연결이 종료되었습니다.'.format(ip, port))

    def send_all_clients(self, senders_socket):
        for client in self.clients:
            socket, (ip, port) = client
            if socket is not senders_socket: # 송신자 제외한 클라이언트에게 보냄
                try:
                    socket.sendall(self.final_received_message.encode())
                except:
                    self.clients.remove(client)
                    print('{},{} 연결이 종료되었습니다.'.format(ip,port))

if __name__=="__main__":
    MultiChatServer()











