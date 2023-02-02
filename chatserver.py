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
                conn = p.connect(host='localhost', user='root', password='chlwlgur', db='population', charset='utf8')
                c = conn.cursor()
                c.execute('SELECT *FROM new_table')
                find_log=c.fetchall()
                print(find_log)
                if find_log == ():
                    if '@@' not in self.final_received_message:
                        # c.execute(f'UPDATE new_table SET aa = "{self.final_received_message}"');
                        c.execute(f'INSERT INTO new_table (aa) VALUES ("{self.final_received_message}")');
                        print('메시지 저장 1')
                    else:
                        print('메시지 확인 1')
                        pass
                else:
                    if '@@' not in self.final_received_message:
                              # c.execute(f'UPDATE POPULATION.NEW_TABLE SET aa = concat(aa, ",{self.final_received_message}"');
                        c.execute(f'INSERT INTO new_table (aa) VALUES ("{self.final_received_message}")');
                        print('message confirm')
                    else:
                        pass
                        print('message 12')
                conn.commit()
                conn.close()

        c_socket.close()

    # def receive_signal(self, c_socket):
    #     while True:
    #         try:
    #             incoming_signal=c_socket.recv(256)
    #             if not incoming_signal:
    #                 break
    #         except:
    #             continue
    #         else:
    #             self.final_received_signal=incoming_signal.decode('utf-8')
    #             print(self.final_received_signal)
    #             self.send_all_clients(c_socket)

    # def received_userlist(self, c_socket):
    #     while True:
    #         try:
    #             incoming_userlist=c_socket.recv(256)
    #             if not incoming_userlist:
    #                 break
    #         except:
    #             continue
    #         else:
    #             self.final_received_userlist=incoming_userlist.decode('utf-8')
    #             print(self.final_received_userlist)
    #             self.send_all_clients(c_socket)

    def send_all_clients(self, senders_socket):
        for client in self.clients:
            socket, (ip, port) = client
            if socket is not senders_socket: # 송신자 제외한 클라이언트에게 보냄
                try:
                    socket.sendall(self.final_received_message.encode())
                    # socket.sendall(self.final_received_signal.encode())
                    # socket.sendall(f'{self.final_received_userlist}'.encode())
                except:
                    self.clients.remove(client)
                    print('{},{} 연결이 종료되었습니다.'.format(ip,port))

if __name__=="__main__":
    MultiChatServer()