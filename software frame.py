from tkinter import *
import datetime
import json
from tkinter import messagebox
import socket
import threading

    
class VerticalScrolledFrame:
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = Frame(master, **kwargs)

        self.vsb = Scrollbar(self.outer, orient=VERTICAL)
        self.vsb.pack(fill=Y, side=RIGHT)
        self.canvas = Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set

        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = Frame(self.canvas, bg=bg)
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw',width=width)
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            return getattr(self.outer, item)
        else:
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion = (0,0, x2, max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event:Event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units" )

    def __str__(self):
        return str(self.outer)


class Software:
    def __init__(self):
        self.connect()
        threading.Thread(target=self.software).start()

    def software(self):
        self.main=Tk()
        self.main.title("Z Chat")
        self.main.geometry("1200x700")
        self.main.iconbitmap("icon.ico")
        self.main.resizable(False,False)
        self.main.withdraw()

        self.main.bind("<Key>",self.clicker)

        self.message_entry = Text(self.main,height=4,width=80,font=("Arial",15))
        self.message_entry.place(x=200,y=610)

        self.message_entry.bind("<Return>",self.send_message)
        
        info_frame = Frame(self.main,background="#AFEEEE",width=200,height=700)
        info_frame.place(x=1,y=1)

        self.usernamelabel=Label(info_frame,text="Username",font=(("Arial",18)),background="#AFEEEE",foreground="#000080")
        self.usernamelabel.place(x=10,y=40)

        self.mobilelabel=Label(info_frame,text="Mobile",font=(("Arial",18)),background="#AFEEEE",foreground="#000080")
        self.mobilelabel.place(x=10,y=100)

        load_history_button=Button(info_frame,text="Load History",font=("Arial",20),foreground="#000080",background="#87CEFA",command=self.fake_history)
        load_history_button.place(x=10,y=620)

        self.chatframe = VerticalScrolledFrame(self.main,background="#87CEFA",width=980,height=610)
        self.chatframe.place(x=200,y=1)

        send_button=Button(self.main,text="Send",font=("Arial",20),foreground="#000080",background="#AFEEEE",command=lambda:self.send_message_thread)
        send_button.place(x=1090,y=625)
        self.login()

        self.loginpage.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main.mainloop()
    def send_message_thread(self):
        self.message_send_thread=threading.Thread(self.send_message)
        self.message_send_thread.start()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(("192.168.207.35", 5555))
            self.client_connected=True
        
        except Exception as error:
            print(error)
            self.nickname = messagebox.showwarning(title="Connection Error",message="Please check your internet and try again.\nIf your internet isn't problem Please contact admin to resolve this issue")
            self.on_closing()
            return

    def showmainpage(self):
        self.main.deiconify()

    def login(self):
        self.loginpage=Toplevel(self.main,background="azure3")
        self.loginpage.title("Z Chat Login Page")
        self.loginpage.geometry("300x450")
        self.loginpage.iconbitmap("icon.ico")
        self.loginpage.resizable(False,False)

        usernamelabel=Label(self.loginpage,text="Enter User Name",background="azure3")
        usernamelabel.place(relx=0.2, rely=0.3, anchor=W)
        
        self.usernameentry=Entry(self.loginpage,width=30)
        self.usernameentry.place(relx=0.21, rely=0.35, anchor=W)
        
        mobilenumberlabel=Label(self.loginpage,text="Enter Mobile Number",background="azure3")
        mobilenumberlabel.place(relx=0.2, rely=0.4, anchor=W)
        
        self.number_entry=Entry(self.loginpage,width=30)
        self.number_entry.place(relx=0.21, rely=0.45, anchor=W)
        
        self.number_entry.bind("<Return>",self.check_user)
        
        self.loginbutton=Button(self.loginpage,text="Login",background="azure3",width=15,height=2,command=self.check_user,justify="center")
        self.loginbutton.place(x=100, y=300, anchor=W,bordermode="inside")
        self.usernameentry.focus_force()
        
        self.loginpage.protocol("WM_DELETE_WINDOW", self.on_closing)

    def connect_user(self,mobile_number,active_ip):
        dict_data={
            "process":"user_check",
            "mobile_number":mobile_number,
            "active_ip":active_ip
        }
        self.client.send(json.dumps(dict_data).encode('utf-8'))
        server_response = self.client.recv(1024).decode("utf-8")
        server_response=json.loads(server_response)
        if server_response['process']=="found":
            return True
        elif server_response['process']=="notfound":
            return False

    def check_user(self,event=None):
        if self.usernameentry.get()=="" or self.number_entry.get() == "" or self.usernameentry.get().startswith(" ") or self.number_entry.get().startswith(" "):
            messagebox.showwarning(title="Invalid Entry",message="Please correct the given Data")
            self.loginpage_reload()
            return
        
        mobile_number=self.number_entry.get()
        active_ip=socket.gethostbyname(socket.gethostname())
        username=self.usernameentry.get()

        try:
            int(mobile_number)
        except:
            messagebox.showerror(title="Invalid Mobile Number",message="Please Enter a valid Mobile Number")
            return

        if self.connect_user(mobile_number=mobile_number,active_ip=active_ip):
            self.loginpage.destroy()
            self.main.deiconify()
            self.receive_thread=threading.Thread(target=self.receive)
            self.receive_thread.start()

            self.usernamelabel.configure(text=f"{username}")
            self.mobilelabel.configure(text=f"{mobile_number}")

        else:
            if messagebox.askokcancel(title="Register New User",message="Are you want to register as new user ?"):
                dict_data={
                    "process":"new_user",
                    "username":username,
                    "mobile_number":mobile_number
                }
                self.client.send(json.dumps(dict_data).encode("utf-8"))
                server_response = json.loads(self.client.recv(1024).decode("utf-8"))
                print(server_response)
                if server_response["status"]:
                    messagebox.showinfo(title="New Login Registered",message=f"Username: {username}\nMobile Number: {mobile_number}\nActive ID: {active_ip}")
                    self.loginpage_reload()
            else:
                self.loginpage_reload()

    def loginpage_reload(self):
        for i in self.loginpage.winfo_children():
            if isinstance(i,Entry):
                i.delete(0,END)

    def reload(self):
        try:
            self.chatframe.destroy()
        except:
            pass
        self.chatframe = VerticalScrolledFrame(self,background="#87CEFA",width=980,height=610)
        self.chatframe.place(x=200,y=1)

        self.update_scrollbar

    def update_scrollbar(self):
        self.chatframe.canvas.yview_moveto(1)

    def send_message(self,event=None):
        message=self.message_entry.get("1.0",END)


        if message.startswith("\n") and len(message.split("\n"))<1:

            messagebox.showwarning(title="Empty Message",message="The first Line is Empty")
            self.message_entry.after(10,self.clear_text)
            return

        message_json = {
                "process":"message_boardcast",
                "mobile_number":self.mobilelabel.cget("text")
            }
        
        if message.endswith("\n"):
            message=message[:-1]
            message_json["message"]=message

        labelframe=LabelFrame(self.chatframe,text=datetime.datetime.now().__format__("%d-%m-%Y %H:%M:%S"))
        labelframe.pack(padx=10,pady=10,anchor=E)

        Label(labelframe,text=message,font=("Arial",12)).pack()

        self.chatframe.outer.after(10,self.update_scrollbar)
        self.message_entry.after(10,self.clear_text)
        
        self.client.send(json.dumps(message_json).encode("utf-8"))
        self.clear_text

    def receive(self):
        print("Listening Server")
        try:
            dict_data = json.loads(self.client.recv(1024).decode('utf-8'))
            if dict_data['process'] == 'message_boardcast':
                if dict_data['mobile_number']!=self.mobilelabel.cget('text'):
                    labelframe=LabelFrame(self.chatframe,text=f"{dict_data['username']} {datetime.datetime.now().__format__('%d-%m-%Y %H:%M:%S')}")
                    labelframe.pack(padx=10,pady=10,anchor=W)
                    Label(labelframe,text=dict_data['message'],font=("Arial",12)).pack()

                    self.chatframe.outer.after(10,self.update_scrollbar)
            self.receive_thread.join()
            self.main.after(100,self.receive)

        except Exception as e:
            print(f"Error: {e}")


    def on_closing(self):
        self.running = False
        try:
            self.client.close()
        except:
            pass
        try:
            self.main.destroy()
        except:
            pass

    def clear_text(self):
        self.message_entry.delete("1.0",END)
    
    def fake_history(self):
        self.reload()
        for i in range(1,110):
            if i%2==0:
                labelframe=LabelFrame(self.chatframe,text=datetime.datetime.now().__format__("%d-%m-%Y %H:%M:%S"))
                labelframe.pack(padx=10,pady=10,anchor=E)

            else:
                labelframe=LabelFrame(self.chatframe,text=datetime.datetime.now().__format__("%d-%m-%Y %H:%M:%S"))
                labelframe.pack(padx=10,pady=10,anchor=W)

            Label(labelframe,text=i,font=("Arial",12)).pack(anchor=E)

        self.chatframe.outer.after(10,self.update_scrollbar)
    
    def clicker(self,event:Event):
        if event.keysym=="slash":
            self.message_entry.focus()

Software()