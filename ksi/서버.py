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
        # self.ip = '10.10.21.104' #실습실 컴퓨터 IP
        self.ip = '192.168.219.109' #기숙사 컴퓨터 IP
        self.port = 9050 # 포트번호 9000~9100 중 아무거나 클라이언트랑은 맞춰야됨
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #소켓 옵션제어
        self.s_sock.bind((self.ip, self.port)) #소켓 결합
        print("클라이언트 대기중...")
        self.s_sock.listen(100) #소켓 연결 제한
        self.accept_client() #accept_client 메서드 실행

    # 연결 클라이언트 소켓을 목록에 추가하고 스레드를 생성하여 데이터를 수신한다
    def accept_client(self): #접속소켓을 허용한다는 거임
        while True:
            client = c_socket, (ip,port) = self.s_sock.accept()
            self.clients.append(client) # 접속된 소켓을 목록에 추가
            print(self.clients)
            print(ip,':', str(port),'가 연결되었습니다') #연결 확인
            cth = Thread(target=self.receive_messages, args=(c_socket,client)) # 수신스레드
            cth.start() # 스레드 시작
    # 데이터를 수신하여 모든 클라이언트에게 전송한다
    def receive_messages(self, c_socket,client):
        while True:
            try:
                incoming_message = c_socket.recv(256) #클라에서 보낸 메시지 받기
                if not incoming_message: # 연결이 종료됨
                    break
            except:
                continue
            else:
                try:
                    conn = pymysql.connect(host='localhost', port=3306, user='root', password='00000000', db='net',
                                           charset='utf8')
                    cursor = conn.cursor()
                    msg = incoming_message.decode() #클라에서 보낸 메시지를 decode
                    print(msg) #메시지 확인
                    user_name = msg.split('/')[0] #클라에서 보낸 메시지는 /로 구분하는데 이걸 split함수로 쪼개서 이름에 해당하는 부분을 변수에 넣어줌
                    self.final_received_message = msg.split('/')[1].encode()
                    now = datetime.datetime.now() #DB에 넣을 시간 받아주기
                    date = now.strftime('%y-%m-%d') #datetime 객체를 str로 변환
                    time = now.strftime('%H:%M')
                    if user_name not in self.clients_name or f"!&%*|EXIT|*%&!" in msg or f'!&%*|CLOSE|*%&!' in msg: #새로 연결된 소켓이거나 서버에서 보낸 메시지가 exit or close 일 경우
                        if f"!&%*|EXIT|*%&!" in msg or f'!&%*|CLOSE|*%&!' in msg: #서버에서 보낸 메시지가 exit or close 일 경우
                            index = self.clients.index(client) #해당하는 인덱스값 찾아주기
                            self.clients.remove(self.clients[index]) #찾은 인덱스값을 연결된 소켓리스트에서 제거하기
                            self.clients_name.remove(user_name) #이건 내가 접속한 유저 이름들 확인하려고 만든 리스트에서 마찬가지로 제거하기
                            print(f'온라인 유저', *self.clients_name) #접속유저 확인하기 및 잘 제거 됐는지 확인
                            print(f'{user_name} 접속 종료') #접속종료한 유저이름 확인하기
                            cursor.execute(f"delete from net.online_user where 이름 = '{user_name}';") #온라인 유저 DB에서 해당하는 유저 DB 삭제하기
                            conn.commit() #저장하기
                        else:
                            self.clients_name.append(user_name) #새로연결된 유저일 경우
                            print('온라인 유저', *self.clients_name) #온라인유저 확인용 출력
                            cursor.execute(f"insert into online_user (이름) values ('{user_name}')") #온라인 유저DB에 유저 추가해주기
                            conn.commit() #저장하기
                        #유저가 나가거나 들어오면 온라인유저목록, 채팅방 목록 업데이트 해줘야해서 DB에서 가져옴
                        cursor.execute(f"select * from online_user")
                        a = cursor.fetchall()
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list")
                        b = cursor.fetchall()
                        #클라이언트한테 보낼 때 리스트 형식으로 보내야하는데 그냥 보내면 안보내져서 json 객체로 변환해주기 import json 해야됨
                        user_name_list = json.dumps(a)
                        chat_list = json.dumps(b)
                        #클라이언트에게 보낼 메시지에 필요한 목록들 인코딩하기
                        self.final_received_message = f'{"@!|USER UPDATE|!@"}/{user_name_list}/{chat_list}'.encode()
                    elif f"!&%*|EXIT CHAT|*%&!" in msg: #유저가 채팅방을 나갈경우
                        chat_room_name = msg.split('/')[2] #유저가 나간 채팅방 split으로 변수에 담아줌
                        chat_serial_number = int(msg.split('/')[3]) #이것도 마찬가지 채팅방의 연번 담아줌 채팅방 이름이 혹시 겹칠까바 연번도 같이 넣어준거임
                        # 유저가 나갔으니 채팅방의 참여인원을 업데이트하기 위해 현재 채팅방 참여인원을 가져옴
                        cursor.execute(f"select 참여인원 from chat_list where 채팅방이름='chat_room_{chat_room_name}' and 연번={chat_serial_number}")
                        personnel = cursor.fetchone()
                        temp= str(int(personnel[0])-1) #현재 참여인원에서 -1 한 값을 변수에 담아줌
                        print(temp) #확인
                        #DB 업데이트 및 해당유저가 채팅방을 나갔다는 내용을 채팅방인원들에게 알려야해서 DB에 저장하기
                        cursor.execute(f"update chat_list set 참여인원='{temp}' where 연번={chat_serial_number} and 채팅방이름='{chat_room_name}'")
                        cursor.execute(f"insert into net_chat values('{date}','{time}','{user_name}','님이 채팅방을 나가셨습니다.','{chat_room_name}','{chat_serial_number}','퇴장')")
                        conn.commit() #수정한 값 저장하기
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list") #채팅방 업데이트를 하기위해 채팅목록 가져오기 참여인원이 수정되어서 다시 불러와야함
                        a = cursor.fetchall()
                        print(a)# 확인용 출력
                        chat_list = json.dumps(a) #리스트를 클라이언트에게 보내기위해서 json 객체로 변환
                        print(f"{user_name}이 {chat_room_name} 채팅방을 나갔습니다.") #서버 콘솔로 확인하기 위한 출력
                        #클라에게 보낼 메시지 만들어서 인코딩하기
                        self.final_received_message = f"{time}   {user_name}님이 채팅방을 나가셨습니다./!&%*|EXIT CHAT|*%&!/{chat_room_name}/{chat_serial_number}/{chat_list}".encode()
                        #채팅방 개설
                    elif f"!@|CHATING ROOM OPEN|@!" in msg: #유저가 채팅방을 개설 했을 경우
                        chat_name = msg.split('/')[2] #채팅방이름 변수에 담아주기
                        #채팅방 테이블 만들기, 채팅방리스트에 넣기
                        cursor.execute(f"create table {chat_name} ("
                                            f"날짜 VARCHAR(45),"
                                            f"시간 VARCHAR(45),"
                                            f"송신자 VARCHAR(45),"
                                            f"수신자 VARCHAR(45),"
                                            f"내용 VARCHAR(100)"
                                            f") ENGINE=InnoDB CHARSET=utf8;")
                        print('테이블생성')
                        #채팅방 목록에 넣어주기 쿼리문이 많은 건 프로시저나 트리거로 만들어야하는데 지금은 그냥 함
                        cursor.execute(f"insert into chat_list (채팅방이름,개설자,참여인원) values ('{chat_name}','{user_name}','0')")
                        conn.commit() #수정내용 저장하기
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list") #채팅목록 업데이트 하기 위해 가져오기
                        a = cursor.fetchall()
                        conn.close()
                        chat_list = json.dumps(a) #리스트를 클라이언트에게 보내기위해서 json 객체로 변환
                        self.final_received_message = f"!@|CHATING ROOM UPDATE|@!/{chat_list}".encode() #유저들에게 보낼 메시지 만들어서 인코딩
                        print(f"{user_name} 채팅방목록 업데이트")#서버 콘솔 확인용 출력
                    elif f"!&%*|ENTER CHAT ROOM|*%&!" in msg: #유저가 채팅방에 들어갔을 경우인데 로직 바껴서 수정해야함 일단 둠
                        chat_room_name = msg.split('/')[2] #해당 채팅방이름 담아두기
                        chat_room_personnel = int(msg.split('/')[3])+1 #채팅방 인원 더 해준 값을 변수에 담아줌
                        print(chat_room_personnel,type(chat_room_personnel)) #확인용 출력
                        chat_serial_number = int(msg.split('/')[4]) #해당 채팅방 연번 담기
                        #유저들에게 입장안내 메시지 DB에 넣고 채팅방 참여인원 업데이트
                        cursor.execute(f"insert into net_chat values('{date}','{time}','{user_name}','님이 입장하셨습니다.','{chat_room_name}',{chat_serial_number},'입장')")
                        cursor.execute(f"update chat_list set 참여인원='{str(chat_room_personnel)}' where 채팅방이름='chat_room_{chat_room_name}' and 연번={chat_serial_number}")
                        conn.commit() #수정값 저장
                        #채팅메시지 DB 가져와서 json으로 변환
                        cursor.execute(f"select 시간,송신자,내용,알림 from net_chat where 채팅방='{chat_room_name}' and 채팅방연번={chat_serial_number}")
                        temp = cursor.fetchall()
                        chat_data = json.dumps(temp)
                        #업데이트할 채팅방 목록 가져와서 json으로 변환
                        cursor.execute(f"select 채팅방이름,개설자,참여인원 from chat_list")
                        a = cursor.fetchall()
                        chat_list = json.dumps(a)
                        #유저에게 전송할 메시지 만들어서 인코딩
                        self.final_received_message = f"!&%*|ENTER CHAT ROOM|*%&!/!/!/!{chat_data}/!/!/!{chat_room_name}/!/!/!{chat_list}".encode()
                        print(f"{user_name}이 {chat_room_name} 채팅방에 들어갔습니다.") #확인용 출력
                    elif f"!@#|SEND MESSAGE|#@!" in msg: #유저가 메시지를 보낼경우
                        #필요한 값들 변수에 저장하기
                        message = msg.split('/')[2]
                        chat_room_name = msg.split('/')[3]
                        chat_serial_number = str(msg.split('/')[4])
                        #저장된 값으로 메시지DB 추가해주기
                        cursor.execute(f"insert into net_chat (날짜,시간,송신자,내용,채팅방,채팅방연번) values ('{date}','{time}','{user_name}','{message}','{chat_room_name}','{chat_serial_number}')")
                        conn.commit() #수정값 저장
                        #유저들에게 보낼 메시지 만들어서 인코딩하기
                        self.final_received_message = f"{time}   {user_name}: {message}/!@#|SEND MESSAGE|#@!/{chat_room_name}/{chat_serial_number}".encode()
                        print(self.final_received_message.decode())
                    self.send_all_clients(self.clients)
                except ValueError as er: print(er) #오류 출력
        #소켓 닫기
        c_socket.close()
    def send_all_clients(self,clients):
        for client in clients: # 목록에 있는 모든 소켓에 대해 위에서 만든 메시지 보내기
            socket, (ip,port) = client
            socket.sendall(self.final_received_message)



if __name__ == '__main__':
    MultiChatServer()