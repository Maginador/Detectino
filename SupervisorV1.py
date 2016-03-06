import webbrowser
import sys
from datetime import datetime
#from pymongo import MongoClient
#from pymongo.errors import ConnectionFailure
#from bson.objectid import ObjectId
from tkinter import *
import threading
import time, queue
import socket, select
from msvcrt import getch

class RegisterDataBase (object):

    def __init__(self):
        try:
          #  client = MongoClient(host="localhost",port = 27017)
            print ('Conectado com Sucesso')
        except ConnectionFailure :
            sys.stderr.write("Could not connect to Mongo DB: %s")
            sys.exit(1)
        # Get a Databse Handle to a Database named "Detectinodb"
        global dbh , session_id
        dbh = client['Detectinodb']
        session_id = ObjectId()
        session_doc = {
            "id":session_id,
            "username" : "Maria ",
            "firstname": "Henrique",
            "surname" : "Cesar",
            "datelogin": datetime.today(),
            "email" : "hmaria@hot.com",
        }
        dbh.session.insert(session_doc)
        print ("Successfully inserted document: %s" % session_doc)


class Escreve_Temp_Banco (object):

    def __init__(self,ses_id,temperatura,ip) :

        self.temp = temperatura
        self.ip = ip
        self.ses_id = ses_id
        temp_doc = {
            "session_doc_id": self.ses_id,
            "temp" : self.temp,
            "ip" : self.ip,
            "datetime": datetime.today(),
        }
        dbh.temperatura.insert(temp_doc)
        print ("Successfully inserted Temperatura document: %s" % temp_doc)


class GuiPart(object):
    def __init__(self, master, queue, startCommand, endCommand, statusRobo):
        self.queue = queue
        self.statusRobo = statusRobo
        # Inicia Interface Grafica, onde inicia

        master.title('Detectino- Tela de Monitoramento : Curso de Mestrado Eng. Eletrica/2016 - Eng. de Software Prof. Vicente Lucena')

        master.option_add('*Font', 'Verdana 10 bold')
        master.option_add('*EntryField.Entry.Font', 'Courier 10')
        master.option_add('*Listbox*Font', 'Courier 10')
        # Defino o tipo de Letra do Menu
        # Desenho o Menu
        self.menubar = Menu(master)
        master.geometry("800x600+300+50")
        self.cmdmenu = Menu(self.menubar)
        self.cmdmenu.add_command(label='Open...', underline=0)
        self.cmdmenu.add('separator')
        self.cmdmenu.add_command(label='Quit', underline=0,
                                 background='white', activebackground='green',
                                 command=endCommand)
        self.menubar.add_cascade(label="File", menu=self.cmdmenu)
        master.config(menu=self.menubar)

        Frame1 = Frame(master,borderwidth=2,relief=GROOVE, highlightthickness=2, highlightbackground="#111")

        Label(Frame1, text = "IP Server :").grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.HOST = StringVar()
        self.HOST.set(IP_Server)
        Entry(Frame1, textvariable= self.HOST).grid(row=0,column=1,padx=5,pady=5)

        Label(Frame1, text = "PORT :").grid(row=1,column=0,padx=5,pady=5,sticky=W)
        self.PORT = IntVar()
        self.PORT.set(21000)
        Entry(Frame1, textvariable= self.PORT).grid(row=1,column=1,padx=5,pady=5)

        Frame1.grid(row=0,column=0,padx=5,pady=5,sticky=W+E)

        Frame2 = Frame(master,borderwidth=2,relief=GROOVE, highlightthickness=2, highlightbackground="#111")

        self.lbl_Alfa= Label(Frame2,relief=RAISED, borderwidth=2, text = "SETOR ALFA : Galileo 1           ")
        self.lbl_Alfa.grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.lbl_Temp1= Label(Frame2,relief=GROOVE, borderwidth=2, text = "Temp (°C)")
        self.lbl_Temp1.grid(row=1,column=0,padx=5,pady=5,sticky=W)

        self.lbl_galileo1 = Label(Frame2,width =10, height =1,state=DISABLED)
        self.lbl_galileo1.grid(row=1,column=0,padx=5,pady=5,sticky=E)

        self.lbl_Beta= Label(Frame2,relief=RAISED, borderwidth=2, text = "SETOR BETA : Galileo 2           ")
        self.lbl_Beta.grid(row=0,column=1,padx=5,pady=5,sticky=W)
        self.lbl_Temp2= Label(Frame2,relief=GROOVE, borderwidth=2, text = "Temp (°C)")
        self.lbl_Temp2.grid(row=1,column=1,padx=5,pady=5,sticky=W)

        self.lbl_galileo2 = Label(Frame2,width =10, height =1,state=DISABLED)
        self.lbl_galileo2.grid(row=1,column=1,padx=5,pady=5,sticky=E)

        Frame2.grid(row=1,column=0,padx=5,pady=5)

        Frame3 = Frame(master,borderwidth=2,relief='sunken', highlightthickness=2, highlightbackground="#111")
        self.lbl_Robotino = Label(Frame3,relief=RAISED, borderwidth=2, text = "STATUS ROBOTINO")
        self.lbl_Robotino.grid(row=0,column=0,padx=5,pady=5,sticky=W+E)
        self.Text_Robotino = Text(Frame3,width =45, height =20,state=DISABLED)

        self.Text_Robotino.config(state=NORMAL)
        self.Text_Robotino.insert(END,self.statusRobo + '\n')
        self.Text_Robotino.yview_scroll(1,"pages")
        self.Text_Robotino.config(state=DISABLED)

        self.Text_Robotino.grid(row=1,column=0,padx=5,pady=5,sticky=W)
        scroll_r1 = Scrollbar(Frame3, command = self.Text_Robotino.yview)
        self.Text_Robotino.configure(yscrollcommand = scroll_r1.set)
        scroll_r1.grid(row=1,column=2,padx=5,pady=5,sticky=E+S+N)

        Frame3.grid(row=2,column=0,padx=5,pady=5)

        self.circleCanvas = Canvas(Frame1,width=50, height=50)
        self.circleCanvas.grid(row=0, column=3,rowspan=2, padx=5, pady=10)
        self.redCircle()

        self.bt_start = Button(Frame1, text=' START ',bg="#ECE82E",command = startCommand)
        self.bt_start.grid(row=0,column=2,rowspan=2,padx=5,pady=5)


    def redCircle(self):
        self.circleCanvas.create_oval(10, 10, 40, 40, width=0, fill='red')

    def greenCircle(self):
        self.circleCanvas.create_oval(10, 10, 40, 40, width=3, fill='green')
        self.bt_start.config(state = DISABLED,relief=SUNKEN)

    def processIncoming(self):
        """ Verifica se tem ha algum dado na Queue a cada 200ms e faz a tratativa -  . """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed.

                print (msg)
                s0 = msg.split(",")[0]
                s1 = msg.split(",")[1]
                #if s1 == IP_GalileoALfa or s1 == IP_GalileoBeta:
                #tempint = int(s0)
                #Escreve_Temp_Banco(session_id,tempint,s1)  # Passo a temperatura como Inteiro para gravar no Banco
                if s1 == IP_GalileoALfa :
                    self.lbl_Alfa.config(bg='#6EEC78')
                    self.lbl_galileo1.config(state=NORMAL)
                    self.lbl_galileo1.config(text= '    ')
                    self.lbl_galileo1.config(relief=GROOVE, borderwidth=2, text= s0,fg="blue",font = "Helvetica 11 bold italic")
                    self.lbl_galileo1.config(state=DISABLED)

                if s1 == IP_GalileoBeta:
                    self.lbl_Beta.config(bg='#6EEC78')
                    self.lbl_galileo2.config(state=NORMAL)
                    self.lbl_galileo2.config(text= '    ')
                    self.lbl_galileo2.config(relief=GROOVE, borderwidth=2, text= s0,fg="blue",font = "Helvetica 11 bold italic")
                    self.lbl_galileo2.config(state=DISABLED)

                if s1 == IP_Robotino:
                    self.lbl_Robotino.config(bg='#ECE82E')
                    self.Text_Robotino.config(state=NORMAL)
                    self.Text_Robotino.insert(END,s0 + '\n')
                    self.Text_Robotino.yview_scroll(1,"pages")
                    self.Text_Robotino.config(state=DISABLED)

            except queue.Empty:
                # just on general principles, although we don't expect this
                # branch to be taken in this case, ignore this exception!
                pass


class ThreadedClient(object):
    """
      Lanço o main e a worker thread. peridicCall e endApp residem na GUI
    """
    def __init__(self, master,statusrobo):
        """
        inicio o GUI e as Threadas assincronas . aqui é o main() que sera usada pelo GUI
        Daqui em diante outras threads serão abertas.
        .
        """

        self.master = master
        self.statusrobo = statusrobo
        # Create the queue
        self.queue = queue.Queue()
        # Set up the GUI part
        self.gui = GuiPart(self.master, self.queue, self.startApplication, self.endApplication,self.statusrobo)
        self.robo = Conecta_robotino(self.gui.Text_Robotino,self.gui.statusRobo) #  Thread de conexao  com Robotino
        self.robo.start()
        """
            # Set up  thread para fazer  I/O assincrono
            # Outras threads podem tambem ser criadas se for o caso de expandir o projeto --> Previsão futura
            # Inicio a chamada peridica dentro da GUI  p/ checar a fila
            # self.periodicCall()
        """
    def periodicCall(self):
        """ Check a cada 200 ms  se ha algo novo na fila. """
        self.master.after(200, self.periodicCall)
        self.gui.processIncoming()

        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            print ("passou aqui .... FIM" )
            import sys
            self.master.destroy()
            sys.exit(0)

    def workerThread1(self):
        """
        Aqui é onde manuseio o I/O Assincrono. faço uso da SELECT . Importante lembrar que
        a Thread ganha o controle regularmente.

        """

        print ("Aguardando uma conexao Galileo...")

        while self.running:
            print ("passou aqui ........ Worker Thread .........................." )
            input = [self.tcpsock_g]
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:
                if s == self.tcpsock_g :
                    (conn, (ip, port)) = self.tcpsock_g.accept()
                    if ip == IP_GalileoALfa :
                        self.gui.lbl_Alfa.config(bg='#6EEC78') # Tratativa do Status de conexao galileo
                        c = recebe_msg_galileo(conn,ip,port,self.queue)
                    else:
                        #ip == IP_GalileoBeta
                        self.gui.lbl_Beta.config(bg='#6EEC78')
                        c = recebe_msg_galileo(conn,ip,port,self.queue)
                    #else:
                        #self.gui.lbl_Beta.config(bg='#6EEC78') # Mudar para janela do Android
                        #c = recebe_msg_android(conn,ip,port,self.queue)
                    c.start()
                    self.threads.append(c)
        self.tcpsock_g.close()

        for c in self.threads:
            c.join()
        """
                    Codigo anterior
                    (conn, (ip, port)) = self.tcpsock_g.accept()
                    if ip == IP_GalileoALfa : self.gui.lbl_Alfa.config(bg='#6EEC78') # Tratativa do Status de conexao galileo
                    else : self.gui.lbl_Beta.config(bg='#6EEC78')
                    c = recebe_msg_galileo(conn,ip,port,self.queue)
                    c.start()
                    self.threads.append(c)
        """


    def startApplication(self):

        self.running = True
        self.tcpsock_g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpsock_g.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpsock_g.bind((str(self.gui.HOST.get()),int(self.gui.PORT.get())))
        self.tcpsock_g.listen(5)
        self.threads = []

        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()
        self.gui.greenCircle()

        self.periodicCall()
        pega_msgrobotino("B") # Por Default considera-se que o Robotino esta Parado e Stand by

    def endApplication(self):
        self.running = False

'''
    -------------------------- Tratativa do Galileo ------------------
'''

class recebe_msg_galileo(threading.Thread):     # Thread de comunicacao com Galileo recebe as Temperaturas e poe na fila

    def __init__(self,conn,ip,port,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.ip = ip
        self.port = port
        self.conn = conn
        self.size = 64

        print("[+] Nova Thread Iniciada para Galileo:  "+ip+":"+str(port))

    def run(self):
        while True:
            data = self.conn.recv(self.size)
            if not data: break
            msg = str(int(data)) + "," + self.ip
            self.queue.put(msg)         # Poe na Fila o valor lido de galileo
            dataint = int(data)
            print("  Leitura de Temperatura  ", dataint)
            print(" VALOR  STATUS DO ROBO =", ROBOTINO_STOP)
            if dataint >= 32 and ROBOTINO_STOP == True:
                print("Temperatura elevada ..................", dataint)
                print("Processo de ativação do Robotino iniciado .......")
                if self.ip == IP_GalileoALfa:
                    envia_msg_robotino('1')
                    msg2 = 'COMANDO: MOVIMENTAR-SE PARA ALFA' + ',' + IP_Robotino
                else:
                    envia_msg_robotino('0')
                    msg2 = 'COMANDO: MOVIMENTAR-SE PARA BETA' + ',' + IP_Robotino
                self.queue.put(msg2)

'''
    ----------------------- Tratativa do Robotino ------------------
'''

class ThreadReception_robotino(threading.Thread):
    """ Thread Objeto que garante a recepçao das Msg oriundas do Robotino"""
    def __init__(self, conn,text,statRobo):
        threading.Thread.__init__(self)
        self.connexion = conn  # Socket Robotino
        self.text = text


    def run(self):
        # global ROBOTINO_STOP
        # ROBOTINO_STOP = True
        while True:
            try:
                # en attente de rÃ©ception
                message_rec = self.connexion.recv(1024)
                message_rec = message_rec.decode(encoding='UTF-8')
                pega_msgrobotino(message_rec)
                self.text.config(state=NORMAL)
                self.text.insert(END,'CMD RECEBIDO : ' + message_rec + '\n')
                # dÃ©filement vers le bas
                self.text.yview_scroll(1,"pages")
                # lecture seule
                self.text.config(state=DISABLED)

                if "A" in message_rec:
                    # A = Robotino saiu da Base
                    print ("Robotino saiu da Base")
                    # ROBOTINO_STOP = False
                    self.text.config(state=NORMAL)
                    self.text.insert(END,' ROBOTINO PARTIU DA BASE ' + '\n')
                    self.text.yview_scroll(1,"pages")
                    self.text.config(state=DISABLED)
                    message_rec=''

                if "B" in message_rec:
                    # B = Robotino Chegou no Sensor
                    # ---------> Neste ponto tem que ativar o Android para tirar foto
                    print("Robotino Chegou no Sensor   ativar o Android para tirar foto")
                    self.text.config(state=NORMAL)
                    self.text.insert(END,' ROBOTINO CHEGOU NO SETOR  '+ '\n')
                    self.text.yview_scroll(1,"pages")
                    self.text.config(state=DISABLED)
                    message_rec=''
                    # ROBOTINO_STOP = True
                    # b = webbrowser.get('google-chrome')
                    webbrowser.open_new('http://192.168.1.100:8080')

                if "C" in message_rec:
                    # C = Robotino voltando para Base
                    print("Robotino Chegou Voltando para Base")
                    self.text.config(state=NORMAL)
                    self.text.insert(END,' ROBOTINO VOLTANDO PARA BASE  '+ '\n')
                    self.text.yview_scroll(1,"pages")
                    self.text.config(state=DISABLED)
                    message_rec=''

                if "X" in message_rec:
                    # D = Robotino voltando para Base
                    print("Robotino  Chegou na  Base - Pronto")
                    # ROBOTINO_STOP = True
                    self.text.config(state=NORMAL)
                    self.text.insert(END,' ROBOTINO CHEGOU NA BASE  '+ '\n')
                    self.text.yview_scroll(1,"pages")
                    self.text.config(state=DISABLED)
                    message_rec=''

                if "END" in message_rec:
                    # fin du qcm
                    global CONECTAROBOTINO
                    CONECTAROBOTINO = False

            except socket.error:
                pass


class Conecta_robotino(threading.Thread):
    def __init__(self,text,statrobo):
        threading.Thread.__init__(self)
        self.text = text
        self.statrobo = statrobo

    def run(self):
        global CONECTAROBOTINO
        global SOCKET_ROBO
        while 1:
            if CONECTAROBOTINO == False:
                try:
                    robotino_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    robotino_Socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                    robotino_Socket.connect((IP_Robotino, PORT_Robotino))
                    # Conversa com Robotino (server ): Lança uma thread para pegar as  messages
                    th_R = ThreadReception_robotino(robotino_Socket,self.text,self.statrobo)
                    th_R.start()
                    print("[+] Nova Thread Iniciada para Robotino:  "+IP_Robotino+":"+str(PORT_Robotino))
                    CONECTAROBOTINO = True
                    SOCKET_ROBO = robotino_Socket


                except socket.error:
                    print('Erro','A conexão com Robotino falhou.')
                    print('Nova','Nova Tentativa.....')
                    CONECTAROBOTINO = False


class envia_msg_robotino(object):

    def __init__(self,message):
        self.msg = message
        #self.txt = text
        if CONECTAROBOTINO == True:
            try:
                SOCKET_ROBO.send(bytes(self.msg,"UTF8"))

            except socket.error:
                pass

'''
    --------------- Captura o retorno do Status do Robotino e Altera a Var Global--------------
'''

def pega_msgrobotino(x):
    if "B" in x:
        global ROBOTINO_STOP
        ROBOTINO_STOP = True
    else:
        ROBOTINO_STOP = False

'''
    ------------- Parte de Tratamento do Android (ainda em duvida se vou usar ) ---------------------------
'''
class envia_msg_android(object):

    def __init__(self,message):
        self.msg = message
        #self.txt = text
        print('CONECTA ANDROID -----> ', CONECTA_ANDROID)
        if CONECTA_ANDROID == True:

            try:
                SOCKET_ANDROID.send(bytes(self.msg,"UTF8"))

            except socket.error:
                pass

class recebe_msg_android(threading.Thread):     # Thread de comunicacao com Galileo

    def __init__(self,conn,ip,port,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.ip = ip
        self.port = port
        self.conn = conn
        self.size = 64
        print("[+] Nova Thread Iniciada para Android :  "+ip+":"+str(port))

    def run(self):

        while True:
            data = self.conn.recv(self.size)
            print("--------------> Valor recebido do Android:", data)
            pega_msgandroid(self.conn)
            if not data: break
            data = data.decode(encoding='UTF-8')
            msg = str(data) + "," + self.ip
            self.queue.put(msg)         # Poe na Fila o valor lido de galileo
            # self.conn.send(bytes("BRASIL","UTF8"))

'''
    ------------ Esta Função é utilizada para Mudar as variaveis globais do Status do Android
'''

def pega_msgandroid(conx):

    global CONECTA_ANDROID
    global SOCKET_ANDROID
    CONECTA_ANDROID = True
    SOCKET_ANDROID = conx

root = Tk()
CONECTAROBOTINO = False
IP_GalileoALfa = '192.168.1.105'
IP_GalileoBeta = '192.168.1.106'
IP_Robotino = '192.168.1.103'
IP_Android = '192.168.1.100'
IP_Server = '192.168.1.102'
PORT_Robotino = 9100
ROBOTINO_status = 'X'
# ROBOTINO_STOP = True
#RegisterDataBase()
client = ThreadedClient(root,ROBOTINO_status)
root.mainloop()
