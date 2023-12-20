from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from cryptography.fernet import Fernet as fernet
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QScrollArea, QScrollBar, QLineEdit
from PyQt5.QtGui import QFont
import sys  
import subprocess
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import filedialog as fd 
import pyperclip
import datetime
import resources
import os
import random

def _file_size(path):
    file_size = os.path.getsize(path)
    total_size = file_size//1024
    if total_size > 1024:
        total_size=total_size//1024
        total_size=str(total_size)+"mb"
    else:
        total_size=str(total_size)+"kb"
    return total_size

curtime = 0

hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip().replace("-","")[::2][:16]

w_ = 480
h_ = 533
HOST = "localhost"
PORT = 1
client_socket = None
text1 = None
text2 = None
Text = None
btn = None
btn2 = None
btn4 = None
btn5 = None
btn6 = None
btn7 = None
text5 = None
text6 = None
text7 = None
CentralWidget = None
msg_from = None
prinat = None
frnt2 = None
otkaz = None
blacklist = ""
chosen_file_path = ""
chosen_file_name = ""
chosen_file_ends = ""
class Ui_MainWindow(object):
    def setupUi(self, seeTable):
        global CentralWidget
        self.setGeometry(0,0,w_,h_)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) 
        CentralWidget = QtWidgets.QWidget(seeTable)
        CentralWidget.setGeometry(0,0,w_,h_)
        CentralWidget.setObjectName("centralwidget")
        font = QFont("Times", 20, QFont.Bold)
        font.setPixelSize(28)
        global text1
        global text2
        global text5
        global text6
        global text7
        global Text
        global btn
        global btn2
        global btn4
        global btn5
        global btn6
        global btn7

        text1 = QLabel(hwid,self)
        text1.setFont(font)
        text1.setStyleSheet("color: rgba(164,42,151,255)")
        text1.setGeometry(173,60,274,23)

        text2 = QLabel("",self)
        text2.setFont(font)
        text2.setStyleSheet("color: rgba(164,42,151,255)")
        text2.setGeometry(39,194,208,33)

        def choose_file():
            global chosen_file_path 
            global chosen_file_name
            global chosen_file_ends
            name= fd.askopenfilename()
            if len(name.split("/")[-1])<11:
                text2.setText(name.split("/")[-1][:11])
            else:
                text2.setText(name.split("/")[-1][:11]+"...")

            chosen_file_path = name
            chosen_file_name = name.split("/")[-1]
            chosen_file_ends = name.split(".")[-1]

        button_style = '''
            #btn{border-radius: 12px;background-color: rgba(255,255,255,0);}
            #btn:Hover{border-radius: 12px;background-color: rgba(41,7,47,55);}
            #btn:Pressed{border-radius: 12px;background-color: rgba(41,7,47,155);}'''
        def send_file():
            global msg_thread
            global curtime
            global client_socket
            global chosen_file_path 
            global chosen_file_name
            global chosen_file_ends
            if Text.text() != hwid and len(Text.text()) > 12 and chosen_file_path != "" and curtime < (datetime.datetime.now() - datetime.datetime(1, 1, 1, 0, 0)).total_seconds()-1.5:
                curtime = (datetime.datetime.now() - datetime.datetime(1, 1, 1, 0, 0)).total_seconds()
                id = Text.text()
                file_size = _file_size(chosen_file_path)
                new_port = str(random.randint(3,65500))
                text_for_server = id+"'__'"+chosen_file_path+"'__'"+file_size+"'__'"+new_port+"'__'"+chosen_file_name+"'__'"+"otpravit"
                client_socket.send(bytes(text_for_server, "utf-8"))
                print(hwid+"i"*(43-len(hwid))+"=")
                key = bytes(hwid+"i"*(43-len(hwid))+"=","utf-8")
                frnt = fernet(key)
                with open(chosen_file_path+".cr","wb") as file1:
                    with open(chosen_file_path, "rb") as file2:
                        file1.write(frnt.encrypt(file2.read()))
                chosen_file_path += ".cr"
                while True:
                    try:
                        s = socket(AF_INET, SOCK_STREAM)
                        s.connect(("127.0.0.1", int(new_port)))
                        print("connected")
                        filename = chosen_file_path 
                        file = open(filename, "rb")
                        while True:
                            file_data = file.read(4096)
                            s.send(file_data)
                            if not file_data:
                                break
                        break
                    except:
                        pass
                file.close()
                os.remove(chosen_file_path)
                chosen_file_path = ""  
                chosen_file_name = ""
                chosen_file_ends = ""
                text2.setText("")

        def prin():
            global msg_from
            global msg_thread
            def send(msg):
                client_socket.send(bytes(msg, "utf-8"))
            new_port = str(random.randint(3,65500))
            send(msg_from[0].split("|")[0]+"'__'"+new_port+"'__'"+msg_from[5]+"'__'prinat")
            key2 = bytes(msg_thread[-1].split("'__'")[0]+"i"*(43-len(msg_thread[-1].split("'__'")[0]))+"=","utf-8")
            print(msg_thread[-1].split("'__'")[0]+"i"*(43-len(msg_thread[-1].split("'__'")[0]))+"=")
            frnt2=fernet(key2)

            while True:
                try:
                    s = socket(AF_INET, SOCK_STREAM)
                    host = "127.0.0.1"
                    port = int(new_port)
                    s.connect((host, port))
                    filename = msg_from[5]
                    file = open(filename+".cr", "wb")
                    while True:
                        file_data = s.recv(4096)
                        file.write(file_data)
                        if not file_data:
                            file.close()
                            break
                    file.close()
                    break
                except:
                    pass

            with open(filename+".cr","rb") as file2:
                with open(filename, "wb") as file1:
                    file1.write(frnt2.decrypt(file2.read()))
            os.remove(filename+".cr")

            text1.move(173,60)
            text2.move(39,194)
            Text.move(268,108)
            btn.move(26,158)
            btn2.move(268,158)
            btn4.move(26,53)
            CentralWidget.setStyleSheet('border-image: url(":/newPrefix/bground.png") 0 0 0 0 stretch stretch;')
            btn5.move(999,999)
            btn6.move(999,999)
            btn7.move(999, 999)
            text5.move(999,999)
            text6.move(999,999)
            text7.move(999,999)
        
        def otkazat():
            text1.move(173,60)
            text2.move(39,194)
            Text.move(268,108)
            btn.move(26,158)
            btn2.move(268,158)
            btn4.move(26,53)
            CentralWidget.setStyleSheet('border-image: url(":/newPrefix/bground.png") 0 0 0 0 stretch stretch;')
            btn5.move(999,999)
            btn6.move(999,999)
            btn7.move(999, 999)
            text5.move(999,999)
            text6.move(999,999)
            text7.move(999,999)

        def kinut_v_chs():
            global blacklist 
            blacklist += msg_thread[-1].split("'__'")[0]
            text1.move(173,60)
            text2.move(39,194)
            Text.move(268,108)
            btn.move(26,158)
            btn2.move(268,158)
            btn4.move(26,53)
            CentralWidget.setStyleSheet('border-image: url(":/newPrefix/bground.png") 0 0 0 0 stretch stretch;')
            btn5.move(999,999)
            btn6.move(999,999)
            btn7.move(999, 999)
            text5.move(999,999)
            text6.move(999,999)
            text7.move(999,999)

        frame = QLabel(self)
        frame.setGeometry(0,0,w_,h_)
        Text = QLineEdit("",self)
        Text.setFont(font)
        Text.setGeometry(268,108,184,33)
        Text.setObjectName("name1")
        Text.setStyleSheet("border-radius: 12px;color: rgba(164,42,151,255); border: 0px solid black; background-color: rgba(41,7,47,0); selection-color: rgba(164,42,151,120); selection-background-color: rgba(60,7,60,0)")
        peremennaya = Text.text()

        btn = QPushButton("",self)  
        btn.setFont(font)
        btn.setObjectName('btn')
        btn.setGeometry(26,158,234,33)
        btn.setStyleSheet(button_style)
        
        btn.clicked.connect(lambda: choose_file())

        btn2 = QPushButton("",self)  
        btn2.setFont(font)
        btn2.setObjectName('btn')
        btn2.setGeometry(268,158,182,33)
        btn2.setStyleSheet(button_style)

        btn2.clicked.connect(lambda: send_file())

        btn4 = QPushButton("",self)  
        btn4.setFont(font)
        btn4.setObjectName('btn')
        btn4.setGeometry(26,53,427,37)
        btn4.setStyleSheet(button_style)
        
        btn4.clicked.connect(lambda: pyperclip.copy(hwid))

        btn3 = QPushButton("",self)  
        btn3.setFont(font)
        btn3.setObjectName('btn')
        btn3.setGeometry(379,1,69,23)
        btn3.setStyleSheet(button_style)
        
        btn3.clicked.connect(lambda: exit())

        btn5 = QPushButton("",self)  
        btn5.setFont(font)
        btn5.setObjectName('btn')
        btn5.setGeometry(999,999,198,33)
        btn5.setStyleSheet(button_style)
        
        btn5.clicked.connect(lambda: prin())

        btn6 = QPushButton("",self)  
        btn6.setFont(font)
        btn6.setObjectName('btn')
        btn6.setGeometry(999,999,224,33)
        btn6.setStyleSheet(button_style)
        
        btn6.clicked.connect(lambda: otkazat())

        btn7 = QPushButton("",self)  
        btn7.setFont(font)
        btn7.setObjectName('btn')
        btn7.setGeometry(999, 999, 162, 37)
        btn7.setStyleSheet(button_style)
        
        btn7.clicked.connect(lambda: kinut_v_chs())

        text5 = QLabel(hwid,self)
        text5.setFont(font)
        text5.setStyleSheet("color: rgba(164,42,151,255)")
        text5.setGeometry(999,999,349,33)

        text6 = QLabel(hwid,self)
        text6.setFont(font)
        text6.setStyleSheet("color: rgba(164,42,151,255)")
        text6.setGeometry(999,999,259,33)

        text7 = QLabel(hwid,self)
        text7.setFont(font)
        text7.setStyleSheet("color: rgba(164,42,151,255)")
        text7.setGeometry(999,999,127,33)



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    global CentralWidget
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        CentralWidget.setStyleSheet("""
            #centralwidget {
                border-radius: 10px;border-image: url(":/newPrefix/bground.png") 0 0 0 0 stretch stretch;
            }
        """)
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass
        
def thread1():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/newPrefix/ico.ico")) 
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    msg_thread = ["",""]
    cache_thread = ""

    def t2():
        global client_socket
        def receive():
            global msg_from
            global msg_thread
            global cache_thread
            global text1
            global text2
            global Text
            global btn
            global btn2
            global btn4
            global CentralWidget
            while True:
                try:
                    msg_thread[-1] = client_socket.recv(BUFSIZ).decode("utf-8")
                    if msg_thread[-1] != cache_thread:
                        cache_thread = msg_thread[-1]                            
                        msg_from = msg_thread[-1].split("'__'")
                        if not (msg_thread[-1].split("'__'")[0] in blacklist) and "otpravit" in msg_from[-1]:
                            text1.move(999,999)
                            text2.move(999,999)
                            Text.move(999,999)
                            btn.move(999,999)
                            btn2.move(999,999)
                            btn4.move(999,999)
                            CentralWidget.setStyleSheet('border-image: url(":/newPrefix/bground2.png") 0 0 0 0 stretch stretch;')
                            btn5.move(26,190)
                            btn6.move(229,190)
                            btn7.move(291, 145)
                            text5.move(123,55)
                            text6.move(185,101)
                            text7.move(150,147)
                            if len(msg_from[-2])<14:
                                text6.setText(msg_from[-2][:15])
                            else:
                                text6.setText(msg_from[-2][:14]+"...")
                            text5.setText(msg_from[0])
                            text7.setText(msg_from[3]) 


                            

                except OSError:
                    pass

        def send(msg):
            client_socket.send(bytes(msg, "utf-8"))


        global HOST
        global PORT

        BUFSIZ = 4096
        ADDR = (HOST, PORT)

        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(ADDR)
        send(hwid)
        receive_thread = Thread(target=receive)
        receive_thread.start()


    def t3():
        thread1()

    # th1 = Thread(target=t1)
    # th1.start()
    th2 = Thread(target=t2)
    th2.start()
    th3 = Thread(target=t3)
    th3.start()