from tkinter import Tk,PhotoImage,Label,Button,Canvas,Frame,messagebox,Entry,W,E,S,N,NE,NSEW,NW,SE,SW
from PIL import Image,ImageTk
from winotify import Notification, audio
from playsound import playsound
from scripts.config import Config
from scripts.pixela import Pixela 
from datetime import datetime as dt
import webbrowser
# ------------- Constants ------------- #

RED_COLOR = "#F38181"
YELLOW_COLOR = "#FCE38A"
GREEN_COLOR = "#95E1D3"
BG_COLOR = "#EAFFD0"
PURPLE_COLOR = "#6B72C4"
FONT = ("Calibri",40,"bold")
BREAK_TOAST = Notification(
    app_id="E Clock",
    title="Break!",
    msg="Time for a break. But no KitKats.",
    duration="short",
    icon=r"D:\E-Clock-Timer\assets\icon.ico"
)
BREAK_TOAST.set_audio(audio.LoopingAlarm10,loop=False)
WORK_TOAST = Notification(
    app_id="E Clock",
    title="Work!!",
    msg="Time to get back to work.",
    duration="short",
    icon=r"D:\E-Clock-Timer\assets\icon.ico"
)
WORK_TOAST.set_audio(audio.LoopingAlarm10,loop=False)
COMPLETE_TOAST = Notification(
    app_id="E Clock",
    title="Complete!!!",
    msg="Hooray! Your hard work will payoff soon.",
    duration="short",
    icon=r"D:\Timer\EPomo-Timer\Assets\icon.png"
)
COMPLETE_TOAST.set_audio(audio.LoopingAlarm10,loop=False)
# ------------- Toast ------------- #
## change name to notification create a notification class
def break_toast()->None:
    BREAK_TOAST.show()

    playsound('assets/sounds/break.mp3')
    return
def work_toast()->None:
    WORK_TOAST.show()
    playsound("assets/sounds/work.mp3")
    return
def complete_toast()->None:
    COMPLETE_TOAST.show()
    playsound('assets/sounds/complete.mp3')
    return
TOAST = {
    "B" : break_toast,
    "W" : work_toast,
    "C" : complete_toast
}
config = Config()

# ------------- UI ------------- #
class UI():
    def __init__(self) -> None:
        
        self.work_session_count = 0
        self.mode = "idle" # work, idle, break
        self.status = "stop" # running
        self.session_time = {"W":30, #mins
                             "B":5} #mins
        self.session = ["W","B","W","B","W","B","W","B","W","B"]
        self.session_index = 0
        self.current_time = 0
        self.speed = 1000 # in ms
        self.work_done_sec = 0

        self.btn_cursor = "hand2"

        pass
    def create_window(self):
        self.window = Tk()
        self.window.title("Home | EClock")
        self.window.config(bg=BG_COLOR)
        self.window.minsize(1280,720)
        self.window.iconbitmap("assets\image\icon.ico")
        return self.create_window
    def clear(self):
        for child in self.window.winfo_children():
            child.destroy()
        return

class Home_UI(UI):
    def __init__(self,window) -> None:
        super().__init__()
        self.window = window
        self.window.title("Pixela Graph | E Clock")


        self.font = ("Helvetica",30,'bold')
        # remove all and create
        self.clear()    
        self.initialize_img()
        self.create_ui()
    
    def initialize_img(self) -> None:
        self.logo_pattern_img_path = "assets\image\pattern.png"
        self.logo_pattern_img = Image.open(self.logo_pattern_img_path).resize((300,300))
        self.logo_pattern_img = ImageTk.PhotoImage(self.logo_pattern_img)
        
        self.logo_img_path = "assets\image\icon.png"
        self.logo_img = Image.open(self.logo_img_path).resize((194,78))
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        
        self.setting_img_path = "assets\image\setting.png"
        self.setting_img = Image.open(self.setting_img_path).resize((47,47))
        self.setting_img = ImageTk.PhotoImage(self.setting_img)

        self.blue_dial_img_path = r"assets\image\blue-dial.png"
        self.blue_dial_img = Image.open(self.blue_dial_img_path).resize((500,500))
        self.blue_dial_img = ImageTk.PhotoImage(self.blue_dial_img)
        
        self.green_dial_img_path = r"assets\image\green-dial.png"
        self.green_dial_img = Image.open(self.green_dial_img_path).resize((500,500))
        self.green_dial_img = ImageTk.PhotoImage(self.green_dial_img)

        self.red_dial_img_path = r"assets\image\red-dial.png"
        self.red_dial_img = Image.open(self.red_dial_img_path).resize((500,500))
        self.red_dial_img = ImageTk.PhotoImage(self.red_dial_img)
    
        self.second_hand_img_path = "assets\image\second-hand.png"
        self.second_hand_img = Image.open(self.second_hand_img_path).resize((210,210))
        self.second_hand_img = ImageTk.PhotoImage(self.second_hand_img)
        
        self.minute_hand_img_path = "assets\image\minute-hand.png"
        self.minute_hand_img = Image.open(self.minute_hand_img_path).resize((150,150))
        self.minute_hand_img = ImageTk.PhotoImage(self.minute_hand_img)

        self.dot_img_path = "assets\image\dot.png"
        self.dot_img = Image.open(self.dot_img_path).resize((40,40))
        self.dot_img = ImageTk.PhotoImage(self.dot_img)

        self.home_blob_1_img_path = 'assets\image\home-blob1.png'
        self.home_blob_1_img= Image.open(self.home_blob_1_img_path).resize((200,200))
        self.home_blob_1_img = ImageTk.PhotoImage(self.home_blob_1_img)
        
        self.home_blob_2_img_path = 'assets\image\home-blob2.png'
        self.home_blob_2_img= Image.open(self.home_blob_2_img_path).resize((240,240)).rotate(-30)
        self.home_blob_2_img = ImageTk.PhotoImage(self.home_blob_2_img)
        
        self.home_blob_3_img_path = 'assets\image\home-blob3.png'
        self.home_blob_3_img= Image.open(self.home_blob_3_img_path).resize((300,300)).rotate(20)
        self.home_blob_3_img = ImageTk.PhotoImage(self.home_blob_3_img)

        self.play_btn_img_path = 'assets\image\play.png'
        self.play_btn_img = Image.open(self.play_btn_img_path).resize((40,40))
        self.play_btn_img = ImageTk.PhotoImage(self.play_btn_img)
        
        self.pause_btn_img_path = 'assets\image\pause.png'
        self.pause_btn_img = Image.open(self.pause_btn_img_path).resize((40,40))
        self.pause_btn_img = ImageTk.PhotoImage(self.pause_btn_img)
        
        self.reset_btn_img_path = r'assets\image\reset.png'
        self.reset_btn_img = Image.open(self.reset_btn_img_path).resize((40,40))
        self.reset_btn_img = ImageTk.PhotoImage(self.reset_btn_img)
        
        self.complete_btn_img_path = r'assets\image\complete.png'
        self.complete_btn_img = Image.open(self.complete_btn_img_path).resize((40,40))
        self.complete_btn_img = ImageTk.PhotoImage(self.complete_btn_img)
        
        self.circle_blob_img_path = r'assets\image\circle-blob.png'
        self.circle_blob_img = Image.open(self.circle_blob_img_path).resize((580,580))
        self.circle_blob_img = ImageTk.PhotoImage(self.circle_blob_img)

        self.done_img_path = "assets\image\done.png"
        self.done_img = Image.open(self.done_img_path).resize((35,35))
        self.done_img = ImageTk.PhotoImage(self.done_img)
        return

    def create_ui(self) -> None:

        # Nav Part
        canvas = Canvas(bg=BG_COLOR,highlightthickness=0)
        canvas.create_rectangle(0,0,1280,60,fill=GREEN_COLOR,width=0)
        canvas.create_image(1280,0,anchor=NE,image=self.logo_pattern_img)
        canvas.create_image(1275,30,anchor=NE,image=self.logo_img)
        canvas.pack(fill='both',expand=True)
        
        setting_btn = Button(image=self.setting_img,
                             cursor=self.btn_cursor,
                             bg=GREEN_COLOR,
                             borderwidth=0,
                             activebackground=GREEN_COLOR,
                             command=self.setting)
        setting_btn.place(relx=0.01,rely=0.01)
        
        # Clock Part

        self.clock = Canvas(height=660,width=900,
                       bg=BG_COLOR,
                       highlightthickness=0)
        self.clock.create_image(190,120,image=self.home_blob_1_img)
        self.clock.create_image(190,520,image=self.home_blob_2_img)
        self.clock.create_image(770,270,image=self.home_blob_3_img)
        self.clock_face = self.clock.create_image(450,330,image = self.blue_dial_img) 
        self.clock_second_hand = self.clock.create_image(450,330,image = self.second_hand_img) 
        self.clock_minute_hand = self.clock.create_image(450,330,image = self.minute_hand_img) 
        self.clock.create_image(450,330,image = self.dot_img) 
        self.clock.place(relx=0,rely=1,anchor=SW)
        
        self.done_frame = Frame(height=200,width=50,bg=RED_COLOR)
        self.done_frame.place(relx=0.595,rely=.3)
        


        self.title_text = self.clock.create_text(190,525,text="Idle",
                                            fill=BG_COLOR,angle=-10,
                                            font=self.font)
        
        self.play_pause_btn = Button(image=self.play_btn_img,
                            bg=RED_COLOR,
                            activebackground=RED_COLOR,
                            borderwidth=0,
                            command=self.play_pause,
                            cursor=self.btn_cursor)
        self.play_pause_btn.place(relx=0.12,rely=0.21)
        
        complete_btn = Button(image=self.complete_btn_img,
                            bg=RED_COLOR,
                            activebackground=RED_COLOR,
                            borderwidth=0,
                            command=self.complete,
                            cursor=self.btn_cursor)
        complete_btn.place(relx=0.12,rely=0.29)

        reset = Button(image=self.reset_btn_img,
                            bg=RED_COLOR,
                            activebackground=RED_COLOR,
                            borderwidth=0,
                            command=self.call_reset_timer,
                            cursor=self.btn_cursor)
        reset.place(relx=0.16,rely=0.15)
        

        # Data show part
        data = self.get_today_hours()
        
        data_canvas = Canvas(bg=BG_COLOR,highlightthickness=0,height=540,width=320)
        data_canvas.create_image(140,285,image=self.circle_blob_img)
        data_canvas.place(relx=0.689,rely=1,anchor=SW)
        data_canvas.create_text(223,85,text="Today",
                                        fill=YELLOW_COLOR,
                                        font=('Helvetica 30 bold'))
        data_canvas.create_text(230,245,text="Hours",
                                        fill=YELLOW_COLOR,
                                        font=('Helvetica 30 bold'))
        data_canvas.create_text(90,325,text="Mins",
                                        fill=YELLOW_COLOR,
                                        font=('Helvetica 30 bold'))
        self.hour_text = data_canvas.create_text(100,185,text=data['hours'],
                                        fill=YELLOW_COLOR,
                                        font=self.font)
        self.minute_text = data_canvas.create_text(210,375,text=data['minutes'],
                                        fill=YELLOW_COLOR,
                                        font=self.font)
        pixela_btn = Button(text="Details",
                            bg=RED_COLOR,
                            fg=YELLOW_COLOR,
                            activebackground=RED_COLOR,
                            activeforeground=YELLOW_COLOR,
                            cursor=self.btn_cursor,
                            font=('Helvetica 15 underline'),
                            borderwidth=0,
                            command=lambda : Stats_UI(self.window))
        pixela_btn.place(relx=0.743,rely=.825,anchor=NW)
        return

    def update_ui(self) -> None:


        if self.mode == "idle":
            replace_text = "Timer"
            replace_clock_face = self.blue_dial_img
            
        elif self.mode == "work":
            replace_text = config.read_value('pixela_graph')[0]['graph_name']
            replace_clock_face = self.green_dial_img

        elif self.mode == "break":
            replace_text = "Break"
            replace_clock_face = self.red_dial_img

        self.clock.itemconfig(self.title_text,text=replace_text)
        self.clock.itemconfig(self.clock_face,image = replace_clock_face)
       
        # create done images
        for child in  self.done_frame.winfo_children():
            child.destroy()
        for n in range(self.work_session_count):
            lb = Label(self.done_frame,image=self.done_img,bg=RED_COLOR)
            lb.grid(row=n,column=1,pady=(0,5))


        if self.status == "stop" and self.mode == "idle":
            self.play_pause_btn.configure(image=self.play_btn_img)

        elif self.status == "pause" and self.mode != "idle":
            self.clock.itemconfig(self.title_text,text="Paused")
            self.play_pause_btn.configure(image=self.play_btn_img)

        elif self.status == "play" and self.mode != "idle":
            self.clock.itemconfig(self.title_text,text=replace_text)
            self.play_pause_btn.configure(image=self.pause_btn_img)
        
        return

    # ------------- Buttons ------------- #
    def setting(self):
        Setting_UI(self.window)
        return

    def play_pause(self) -> None:
        if self.status == "stop":
            self.status = "play"
            self.mode_change()

            # get min for timer and convert in second
            self.current_time = self.session_time[self.session[self.session_index] ] * 60
            self.start_timer()
        elif self.status == "play":
            # Do pause stuff
            self.status = "pause"
            self.pause_timer()
            print("Paused")
            self.update_ui()
        elif self.status == "pause":
            # Do play stuff
            self.status = "play"
            self.start_timer()
            self.update_ui()
        return

    def complete(self):
        if self.work_done_sec < 60:
            messagebox.showwarning("Warning!","Couldn't post the data.\nDo some work.")
            return
        worked_mins = self.work_done_sec//60
        token = config.read_value('pixela_token')
        user = config.read_value('pixela_user')
        graph_id = config.read_value('pixela_graph')[0]['graph_id']
        date = dt.now()
        date=date.strftime("%Y%m%d")
        Pixela().plot_pixel(token,user,graph_id,date,worked_mins)
        self.call_reset_timer()
        return

    def call_reset_timer(self) -> None:
        self.work_session_count = 0
        self.mode = "idle"
        self.status = "stop"
        self.session_index = 0
        self.current_time = 0
        self.work_session_count = 0
        self.work_done_sec = 0
        self.update_ui()
        self.move_minute_hand(0,0,True)
        self.move_second_hand(0,0,True)
        # create done images
        for child in  self.done_frame.winfo_children():
            child.destroy()
        try:
            self.pause_timer()
        except:
            pass

    # ------------- pixela ------------- #
    def get_today_hours(self) -> dict:
        """
            This method fetches hours and minutes worked today and returns in a dict.
        """
        return_data = {'hours':0,
                       'minutes':0}
        ## get data
        user = config.read_value('pixela_user')
        graph_id = config.read_value('pixela_graph')[0]['graph_id']
        today_data = Pixela().get_graph_stats(user,graph_id)
        today_data = today_data['todaysQuantity']
        if today_data != 0:
            hours = today_data // 60
            minutes = today_data % 60
            return_data["hours"] = hours
            return_data["minutes"] = minutes

        return return_data
    


    # ------------- Move Clock ------------- #

    def move_second_hand(self,degree,time,reset=False) -> None:
        
        
        if reset == True:
            self.second_hand_img = Image.open(self.second_hand_img_path).resize((210,210))
            self.second_hand_img = ImageTk.PhotoImage(self.second_hand_img)
            self.clock.itemconfig(self.clock_second_hand,image = self.second_hand_img)
            return
        
        to_rotate = degree * time
        
        self.second_hand_img = self.second_hand_img = Image.open(self.second_hand_img_path).resize((210,210)).rotate(-to_rotate)
        self.second_hand_img = ImageTk.PhotoImage(self.second_hand_img)

        self.clock.itemconfig(self.clock_second_hand,image = self.second_hand_img)
        return

    def move_minute_hand(self,degree,time,reset=False) -> None:
        
        if reset == True:
            self.minute_hand_img = Image.open(self.minute_hand_img_path).resize((150,150))
            self.minute_hand_img = ImageTk.PhotoImage(self.minute_hand_img)
            self.clock.itemconfig(self.clock_minute_hand,image = self.minute_hand_img)
            
            return
        
        time = time//60 # in mins
        to_rotate = degree * time
        
        self.minute_hand_img = Image.open(self.minute_hand_img_path).resize((150,150)).rotate(-to_rotate)
        self.minute_hand_img = ImageTk.PhotoImage(self.minute_hand_img)

        self.clock.itemconfig(self.clock_minute_hand,image = self.minute_hand_img)
        return

    # ------------- Modes ------------- #
    def mode_change(self) -> None:
        if self.mode == "idle":
            # change to work
            self.mode = "work"

        elif self.mode == "work":
            # change to break
            self.mode = "break"

        elif self.mode == "break":
            # change to work or idle        
            self.mode = "work"
        
        self.update_ui()
        return

    def mode_complete(self) -> None:

        self.session_index += 1
        try:
            if self.session[self.session_index] == "W":
                self.mode = "work"
            elif self.session[self.session_index] == "B":
                self.work_session_count += 1
                self.mode = "break"
            
            self.current_time = self.session_time[self.session[self.session_index]] * 60
        except IndexError:
            TOAST["C"]()
            self.complete()
            self.call_reset_timer()
            return
        else:
            self.update_ui()
            TOAST[self.session[self.session_index]]()

            self.window.after(3000,self.start_timer)
        return

    # ------------- Timer ------------- #
    def start_timer(self) -> None:
        self.timer_id = self.window.after(1,self.countdown,self.current_time)
        return
    def pause_timer(self) -> None:
        self.window.after_cancel(self.timer_id)
        return

    def countdown(self,count) -> None:
        print(count)
        # get mode
        if self.mode == "work":
            self.work_done_sec += 1
        if count < 0:
            self.mode_complete()
            return
        session_type = self.session[self.session_index]
        full_time = self.session_time[session_type] # in mins
        minute_rotation = 360/full_time # degree
        second_rotation =  360/60 # degree
        self.current_time = self.current_time-1
        self.move_second_hand(second_rotation,full_time*60 - count)
        self.move_minute_hand(minute_rotation,full_time*60 - count)
        self.timer_id=self.window.after(self.speed,self.countdown,self.current_time)
        return

class Setting_UI(UI):
    def __init__(self,window) -> None:
        super().__init__()
        self.window = window
        self.window.title("Pixela Graph | E Clock")

        self.title_font = ("Helvetica",30,'bold')
        self.content_font = ("Helvetica",15,'bold')
        # remove all and create
        self.clear()    
        self.initialize_img()
        self.create_ui()

    def initialize_img(self):
        self.logo_pattern_img_path = "assets\image\pattern.png"
        self.logo_pattern_img = Image.open(self.logo_pattern_img_path).resize((300,300))
        self.logo_pattern_img = ImageTk.PhotoImage(self.logo_pattern_img)
        
        self.logo_img_path = "assets\image\icon.png"
        self.logo_img = Image.open(self.logo_img_path).resize((194,78))
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        
        self.back_img_path = r"assets\image\back.png"
        self.back_img = Image.open(self.back_img_path).resize((40,40))
        self.back_img = ImageTk.PhotoImage(self.back_img)
        
        self.create_img_path = r"assets\image\add.png"
        self.create_img = Image.open(self.create_img_path).resize((40,40))
        self.create_img = ImageTk.PhotoImage(self.create_img)

        
        return

    def create_ui(self):
        # Nav Part
        canvas = Canvas(bg=BG_COLOR,highlightthickness=0)
        canvas.create_rectangle(0,0,1280,60,fill=GREEN_COLOR,width=0)
        canvas.create_image(1280,0,anchor=NE,image=self.logo_pattern_img)
        canvas.create_image(1275,30,anchor=NE,image=self.logo_img)
        canvas.pack(fill='both',expand=True)
        
        back_btn = Button(image=self.back_img,
                             cursor=self.btn_cursor,
                             bg=GREEN_COLOR,
                             borderwidth=0,
                             activebackground=GREEN_COLOR,
                             command=self.back)
        back_btn.place(relx=0.01,rely=0.01)

        window = Frame(height=600,bg=BG_COLOR)
        window.place(relwidth=.8,relx=0,rely=0.1)

        top_window = Frame(window,height=300,bg=BG_COLOR)
        top_window.pack(side="top",fill="x",expand=True,padx=(20,0),pady=(20,0))
        
        bottom_window = Frame(window,height=300,bg=BG_COLOR)
        bottom_window.pack(side="top",fill="x",expand=True,padx=(20,0),pady=(20,0))

        if True: # Top window
        
            user_data = config.read_value('pixela_user')
            token_data = config.read_value('pixela_token')
            graph_id_data = config.read_value('pixela_graph')[0]['graph_id']
            graph_name_data = config.read_value('pixela_graph')[0]['graph_name']


            pixela_title = Label(top_window,text="Pixela Info",font=self.title_font,bg=BG_COLOR,fg=RED_COLOR)
            pixela_title.grid(row=1,column=1,columnspan=2,sticky=W,pady=(0,20))

            pixela_user_lb = Label(top_window,text="User",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            pixela_user_ans = Label(top_window,text=user_data,font=self.content_font,bg=BG_COLOR,fg=PURPLE_COLOR)
            pixela_user_lb.grid(row=2,column=1,sticky=W)
            pixela_user_ans.grid(row=2,column=3,sticky=W)
            
            pixela_token_lb = Label(top_window,text="Token",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            pixela_token_ans = Label(top_window,text=token_data,font=self.content_font,bg=BG_COLOR,fg=PURPLE_COLOR)
            pixela_token_lb.grid(row=3,column=1,sticky=W)
            pixela_token_ans.grid(row=3,column=3,sticky=W)
            
            pixela_graph_id_lb = Label(top_window,text="Graph ID",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            pixela_graph_id_ans = Label(top_window,text=graph_id_data,font=self.content_font,bg=BG_COLOR,fg=PURPLE_COLOR)
            pixela_graph_id_lb.grid(row=4,column=1,sticky=W)
            pixela_graph_id_ans.grid(row=4,column=3,sticky=W)
            
            pixela_graph_name_lb = Label(top_window,text="Graph Name",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            pixela_graph_name_ans = Label(top_window,text=graph_name_data,font=self.content_font,bg=BG_COLOR,fg=PURPLE_COLOR)
            pixela_graph_name_lb.grid(row=5,column=1,sticky=W)
            pixela_graph_name_ans.grid(row=5,column=3,sticky=W)

            pixela_divider_placeholder1 = Label(top_window,text=":",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            pixela_divider_placeholder2 = Label(top_window,text=":",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            pixela_divider_placeholder3 = Label(top_window,text=":",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            pixela_divider_placeholder4 = Label(top_window,text=":",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            pixela_divider_placeholder1.grid(row=2,column=2)
            pixela_divider_placeholder2.grid(row=3,column=2)
            pixela_divider_placeholder3.grid(row=4,column=2)
            pixela_divider_placeholder4.grid(row=5,column=2)

            line = Canvas(top_window,height=2,width=1000,bg=GREEN_COLOR,highlightthickness=0)
            line.grid(row=6,column=1,columnspan=3,sticky=W,pady=(30,0))



        if True: # Bottom Window
            ## Left side

            account_title = Label(bottom_window,text="Account",font=self.title_font,bg=BG_COLOR,fg=RED_COLOR)
            account_title.grid(row=1,column=1,sticky=W,pady=(0,20))
            create_lb = Label(bottom_window,text="Create new",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            create_lb.grid(row=2,column=1,sticky=W)
            graph_name_lb = Label(bottom_window,text="Enter graph name",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            divider_placeholder1 = Label(bottom_window,text=":",font=self.content_font,bg=BG_COLOR,fg=RED_COLOR)
            self.graph_name_etr = Entry(bottom_window,width=20,font=self.content_font,fg=RED_COLOR,bg=BG_COLOR,relief="sunken")
            graph_name_lb.grid(row=3,column=1,sticky=W)
            divider_placeholder1.grid(row=3,column=2,sticky=W)
            self.graph_name_etr.grid(row=3,column=3,sticky=W)
            graph_create_btn = Button(bottom_window,image=self.create_img,bg=BG_COLOR,activebackground=BG_COLOR,borderwidth=0,command=self.call_create_pixela,cursor=self.btn_cursor)
            graph_create_btn.grid(row=4,column=1,columnspan=3,pady=(20,0))

            ## Divider 
            line = Canvas(bottom_window,width=2,bg=GREEN_COLOR,highlightthickness=0)
            line.grid(row=1,column=4,rowspan=10,sticky=N,pady=(50,0),padx=(120,20))

            ## Right side

            reset_title = Label(bottom_window,text="Reset",font=self.title_font,bg=BG_COLOR,fg=RED_COLOR)
            reset_title.grid(row=1,column=5,sticky=W,pady=(0,20))
            reset_btn = Button(bottom_window,text="All settings",font=self.content_font,bg=BG_COLOR,activebackground=BG_COLOR,fg=RED_COLOR,activeforeground=RED_COLOR,borderwidth=0,command=self.call_config_reset,cursor=self.btn_cursor)
            reset_btn.grid(row=2,column=5,sticky=W)
            pass    

        return

    def back(self):
        Home_UI(self.window)
        return

    def call_config_reset(self):
        _is_ask = messagebox.askyesno("Confirmation", "You are about to reset the config file. It contains your Pixela Graph Credentials. If you continue you will lose all the Pixela graph data.\nDo you want to continue with the reset?") 
        if _is_ask is True:
            Config().reset()
        return

    def call_create_pixela(self):
        # check if already created
        if Config().read_value('pixela_token') != None:
            messagebox.showwarning("Failed!","User already created.")
            return False
        name = self.graph_name_etr.get()
        if name == " " or name == "":
            messagebox.showerror("Error!","Enter name for the graph.")
            return False
        if (Pixela().create(name)) == True:
            messagebox.showinfo("Success!",f"You've created a graph with the name: {name}.")
            return True
        messagebox.showerror("Error!","Some other error. Line 464")
        return False

class Stats_UI(UI):
    def __init__(self,window) -> None:
        super().__init__()
        if config.read_value("pixela_user") == None:
            messagebox.showwarning("Warning","User not found.\nCreate a new user in settings.")
            return
        self.window = window
        self.window.title("Stats | E Clock")
        self.font_heading = ("Calibri",30,"bold")
        self.font_content = ("Calibri",20,"bold")

        # remove all and create
        self.clear()    


        self.initialize_img()
        self.create_ui2()
        return

    def initialize_img(self):
        self.logo_pattern_img_path = "assets\image\pattern.png"
        self.logo_pattern_img = Image.open(self.logo_pattern_img_path).resize((300,300))
        self.logo_pattern_img = ImageTk.PhotoImage(self.logo_pattern_img)
        
        self.logo_img_path = "assets\image\icon.png"
        self.logo_img = Image.open(self.logo_img_path).resize((194,78))
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        
        self.back_img_path = r"assets\image\back.png"
        self.back_img = Image.open(self.back_img_path).resize((40,40))
        self.back_img = ImageTk.PhotoImage(self.back_img)

        self.card_bg_img_path = r"assets\image\card-bg.png"
        self.card_bg_img = Image.open(self.card_bg_img_path).resize((325,163))
        self.card_bg_img = ImageTk.PhotoImage(self.card_bg_img)


        return

    def get_data(self) -> None:
        user = config.read_value("pixela_user")
        graph_id = config.read_value("pixela_graph")[0]["graph_id"]

        Pixela().save_graph_svg(user,graph_id)

        data = Pixela().get_graph_stats(user,graph_id)
    
        today_hour_data = int(data["todaysQuantity"])
        self.today_hour,self.today_mins = self.get_time(today_hour_data)

        avg_hour_data = int(data["avgQuantity"])
        self.avg_hour,self.avg_mins = self.get_time(avg_hour_data)

        total_hour_data = int(data["totalQuantity"])
        self.total_hour,self.total_mins = self.get_time(total_hour_data)


        most_hour_data = int(data["maxQuantity"])
        self.most_hour,self.most_mins = self.get_time(most_hour_data)


        least_hour_data = int(data["minQuantity"])
        self.least_hour,self.least_mins = self.get_time(least_hour_data)

        return

    def get_time(self,time) -> dict:
        """
            This method converts given time to hours and minutes.
        """
        
        ## get data
        if time != 0:
            hours = time // 60
            minutes = time % 60
            return_data = (hours,minutes)
            return return_data
        return (0,0)
    
    def create_ui2(self) -> None:

        self.get_data()

        # Nav Part
        canvas = Canvas(bg=BG_COLOR,highlightthickness=0)
        canvas.create_rectangle(0,0,1280,60,fill=GREEN_COLOR,width=0)
        canvas.create_image(1280,0,anchor=NE,image=self.logo_pattern_img)
        canvas.create_image(1275,30,anchor=NE,image=self.logo_img)
        canvas.pack(fill='both',expand=True)
        
        back_btn = Button(image=self.back_img,
                             cursor=self.btn_cursor,
                             bg=GREEN_COLOR,
                             borderwidth=0,
                             activebackground=GREEN_COLOR,
                             command=self.back)
        back_btn.place(relx=0.0,rely=0.01)


 
        # Stats Card Part
        card_frame = Frame(height=350,width=1050,bg=BG_COLOR)
        card_frame.place(relx=0.0,rely=.1)

        graph_name = config.read_value('pixela_graph')[0]['graph_name']
        card_title = Label(text=graph_name,font=self.font_heading,fg=RED_COLOR,bg=BG_COLOR)
        card_title.place(relx=.8,rely=.3)

        card1_hours = 0
        card1_mins = 0
        card1 = Canvas(card_frame,height=162,width=325,bg=BG_COLOR,highlightthickness=0)
        card1.create_image(165,82,image=self.card_bg_img)
        card1.create_text(165,35,text="Total Time",font=self.font_heading,fill=YELLOW_COLOR)       
        card1.create_text(165,75,text=f"{self.total_hour} Hours",font=self.font_content,fill=YELLOW_COLOR)       
        card1.create_text(165,100,text="&",font=self.font_content,fill=YELLOW_COLOR)       
        card1.create_text(165,125,text=f"{self.total_mins} Minutes",font=self.font_content,fill=YELLOW_COLOR)       

        card2 = Canvas(card_frame,height=162,width=325,bg=BG_COLOR,highlightthickness=0)
        card2.create_image(165,82,image=self.card_bg_img)
        card2.create_text(165,35,text="Average Time",font=self.font_heading,fill=YELLOW_COLOR)       
        card2.create_text(165,75,text=f"{self.avg_hour} Hours",font=self.font_content,fill=YELLOW_COLOR)       
        card2.create_text(165,100,text="&",font=self.font_content,fill=YELLOW_COLOR)       
        card2.create_text(165,125,text=f"{self.avg_mins} Minutes",font=self.font_content,fill=YELLOW_COLOR)   
        
        card3 = Canvas(card_frame,height=162,width=325,bg=BG_COLOR,highlightthickness=0)
        card3.create_image(165,82,image=self.card_bg_img)
        card3.create_text(165,35,text="Most Hours",font=self.font_heading,fill=YELLOW_COLOR)       
        card3.create_text(165,75,text=f"{self.most_hour} Hours",font=self.font_content,fill=YELLOW_COLOR)       
        card3.create_text(165,100,text="&",font=self.font_content,fill=YELLOW_COLOR)       
        card3.create_text(165,125,text=f"{self.most_mins} Minutes",font=self.font_content,fill=YELLOW_COLOR)   

        card4 = Canvas(card_frame,height=162,width=325,bg=BG_COLOR,highlightthickness=0)
        card4.create_image(165,82,image=self.card_bg_img)
        card4.create_text(165,35,text="Least Hours",font=self.font_heading,fill=YELLOW_COLOR)       
        card4.create_text(165,75,text=f"{self.least_hour} Hours",font=self.font_content,fill=YELLOW_COLOR)       
        card4.create_text(165,100,text="&",font=self.font_content,fill=YELLOW_COLOR)       
        card4.create_text(165,125,text=f"{self.least_mins} Minutes",font=self.font_content,fill=YELLOW_COLOR)   
        
        card5 = Canvas(card_frame,height=162,width=325,bg=BG_COLOR,highlightthickness=0)
        card5.create_image(165,82,image=self.card_bg_img)
        card5.create_text(165,35,text="Today",font=self.font_heading,fill=YELLOW_COLOR)       
        card5.create_text(165,75,text=f"{self.today_hour} Hours",font=self.font_content,fill=YELLOW_COLOR)       
        card5.create_text(165,100,text="&",font=self.font_content,fill=YELLOW_COLOR)       
        card5.create_text(165,125,text=f"{self.today_mins} Minutes",font=self.font_content,fill=YELLOW_COLOR)   
        
        card1.grid(row=1,column=1,padx=(20,0),pady=(10,10))
        card2.grid(row=2,column=1,padx=(20,0))
        card3.grid(row=1,column=2,pady=(10,10))
        card4.grid(row=2,column=2)
        card5.grid(row=1,rowspan=2,column=3)


        # Pixela Chart Part
        global graph_img
        graph_img = Image.open("data\graph.png")
        width,height = graph_img.size
        left = 20
        right = width - 50
        top = 2
        bottom = height
        graph_img = graph_img.crop((left, top, right, bottom))
        graph_img = graph_img.resize((1100,275))
        graph_img = ImageTk.PhotoImage(graph_img)


        pixela_chart_btn = Button(image=graph_img,bg=BG_COLOR,activebackground=BG_COLOR,command=self.open_pixela_chart,borderwidth=0,cursor=self.btn_cursor)
        pixela_chart_btn.place(relx=0.05,rely=.6)
        return

    def back(self):
        Home_UI(self.window)
        return

    def open_pixela_chart(self):
        username = config.read_value('pixela_user')
        graph_id = config.read_value('pixela_graph')[0]['graph_id']
        url = f"https://pixe.la/v1/users/{username}/graphs/{graph_id}.html"

        webbrowser.open(url) 
        return

    pass
