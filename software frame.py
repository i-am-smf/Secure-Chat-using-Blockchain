from tkinter import *
import mysql.connector
import datetime
import json
from tkinter import messagebox
import socket


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

class ZchatDB:
    def __init__(self) -> None:

        self.connect = mysql.connector.connect(host='maple.db.ashhost.in', user='u946_VhqYu6cZi0', passwd='d=a^xJuOm4jORFz^Odi!1tm7',database="s946_zchat")
        self.cur = self.connect.cursor()
    
    def check_user(self,mobile_number,active_id):
        try:
            self.cur.execute(f"SELECT * FROM users where mobile_number = {mobile_number}")
            result=self.cur.fetchall()
        except:
            return False
        
        if len(result)>0:
            self.cur.execute(f"UPDATE users SET active_ip = '{active_id}' where mobile_number = '{mobile_number}'")
            self.connect.commit()
            return True
        else:
            return False
        
    def new_user(self,username,mobile_number,active_id):


        insert_query = '''
            INSERT INTO users(mobile_number,username,active_ip) 
            VALUES (%s, %s, %s)
        '''

        data = (username,mobile_number,active_id)

        try:
            self.cur.execute(insert_query, data)
        
        except:
            self.__init__()
            self.new_user()

        self.connect.commit()  
        return True
    
db=ZchatDB()

class Main(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Z Chat")
        self.geometry("1200x700")
        self.iconbitmap("icon.ico")
        self.resizable(False,False)
        self.withdraw()

        self.bind("<Key>",self.clicker)

        self.textbox = Text(self,height=4,width=80,font=("Arial",15))
        self.textbox.place(x=200,y=610)

        self.textbox.bind("<Return>",self.send_message)
                
        info_frame = Frame(self,background="#AFEEEE",width=200,height=700)
        info_frame.place(x=1,y=1)

        self.usernamelabel=Label(info_frame,text="Username",font=(("Arial",18)),background="#AFEEEE",foreground="#000080")
        self.usernamelabel.place(x=10,y=40)

        self.mobilelabel=Label(info_frame,text="Mobile",font=(("Arial",18)),background="#AFEEEE",foreground="#000080")
        self.mobilelabel.place(x=10,y=100)

        load_history_button=Button(info_frame,text="Load History",font=("Arial",20),foreground="#000080",background="#87CEFA",command=self.fake_history)
        load_history_button.place(x=10,y=620)

        self.chatframe = VerticalScrolledFrame(self,background="#87CEFA",width=980,height=610)
        self.chatframe.place(x=200,y=1)

        send_button=Button(self,text="Send",font=("Arial",20),foreground="#000080",background="#AFEEEE",command=self.send_message)
        send_button.place(x=1090,y=625)
        self.login()

        self.mainloop()
        
    def showmainpage(self):
        self.deiconify()

    def login(self):
        self.loginpage=Toplevel(self,background="azure3")
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
        
        self.loginpage.protocol("WM_DELETE_WINDOW", self.destroy)
        
    def on_closing(self):
        self.destroy()

    def check_user(self,event=None):
        if self.usernameentry.get()=="" or self.number_entry.get() == "" or self.usernameentry.get().startswith(" ") or self.number_entry.get().startswith(" "):
            messagebox.showwarning(title="Invalid Entry",message="Please correct the given Data")
            self.loginpage_reload()
            return
        
        mobile_number=self.number_entry.get()
        active_id=socket.gethostbyname(socket.gethostname())
        username=self.usernameentry.get()

        try:
            int(mobile_number)
        except:
            messagebox.showerror(title="Invalid Mobile Number",message="Please Enter a valid Mobile Number")
            return

            
        if db.check_user(mobile_number=mobile_number,active_id=active_id):
            self.loginpage.destroy()
            self.deiconify()
            self.usernamelabel.configure(text=f"{username}")
            self.mobilelabel.configure(text=f"{mobile_number}")

        else:
            if messagebox.askokcancel(title="Register New User",message="Are you want to register as new user ?"):
                if db.new_user(mobile_number,username,active_id):
                    messagebox.showinfo(title="New Login Registered",message=f"Username: {username}\nMobile Number: {mobile_number}\nActive ID: {active_id}")
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
        message=self.textbox.get("1.0",END)
        message_data={
            "username":f"{self.usernamelabel.cget('text')}",
            "mobile_number":f"{self.mobilelabel.cget('text')}",
            "message":message
        }

        if message.startswith("\n"):
            messagebox.showwarning(title="Empty Message",message="The first Line is Empty")
            self.textbox.after(10,self.clear_text)
            return

        try:            
            if ord(message)==10:
                messagebox.showwarning(title="Empty Message",message="Cannot send empty message in the feed")
                self.textbox.after(10,self.clear_text)
                return

        except:
            if message.endswith("\n"):
                message=message[:-1]
                message_data["message"]=message

            if message.startswith("1"):
                labelframe=LabelFrame(self.chatframe,text=datetime.datetime.now().__format__("%d-%m-%Y %H:%M:%S"))
                labelframe.pack(padx=10,pady=10,anchor=W)
        
            else:
                labelframe=LabelFrame(self.chatframe,text=datetime.datetime.now().__format__("%d-%m-%Y %H:%M:%S"))
                labelframe.pack(padx=10,pady=10,anchor=E)
        
            Label(labelframe,text=message,font=("Arial",12)).pack()

            self.chatframe.outer.after(10,self.update_scrollbar)
            self.textbox.after(10,self.clear_text)
    
    def clear_text(self):
        self.textbox.delete("1.0",END)
    
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
            self.textbox.focus()

Main()