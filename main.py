import os
#from twilio.rest import Client
import threading
from distutils.command.check import check
from threading import Thread
import psutil
from docutils.nodes import target
from pydub import AudioSegment
from pydub.playback import play
import pywhatkit as kit
import pywhatkit
import pyttsx3
import time as time_lib
from tkinter import messagebox
import datetime
import gtts
import os
import time
import speech_recognition as sr
import requests as req
from bs4 import BeautifulSoup as BeautifulSoup
from tkinter import *
import tkinter as tk
import schedule
import customtkinter as ctk
from PIL import Image, ImageTk
from customtkinter import CTkImage
from PIL import Image
import customtkinter as ctk
import threading
from tkinter import messagebox
import sys
import webbrowser
import pyautogui as pg
phone_number = '+201287231873'
def sayer_en(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    speed = engine.getProperty('rate')
    engine.setProperty('rate', 100)
    engine.say(text)
    engine.runAndWait()
def sayer_ar(text):
    say = gtts.gTTS(text, lang="ar")
    say.save('sound.mp3')
    sound = AudioSegment.from_mp3('sound.mp3')
    play(sound)
    try:
        os.remove('sound.mp3')
    except:
        pass  
def take_command(arg=''):
    command = sr.Recognizer()
    with sr.Microphone() as mic:
        print('listening...')
        if arg != "listen":
            sayer_ar("فَلِتَبْدََاءِ بِالتَّحَدُّثِ")
        command.phrase_threshold = 0.3
        audio = command.listen(mic)
        time.sleep(2)
        try:
            print('Recognizing...')
            quary = command.recognize_google(audio, language='ar')
            print(f'User said: {quary}')
        except Exception as e:
            print(e)
            return None
    return quary.lower()
def table_time():
    with open('time_sheets2.txt','a') as f:
        pass
    with open('time_sheets2.txt', 'r') as f:
        text = f.read()
        print(type(text))
        if text == '':
            sayer_ar('لا يوجد لديك دواء')
        text = text.split('*')
        medics = [x for x in text if x]
        for text in medics:
            date, name = text.split(',')
            sayer_ar(f'في الم'
                     f'وعد{date}لديك{name}')
            time.sleep(3)
def return_list():
    with open("phones.txt",'a') as f:
        pass 
    with open("phones.txt",'r') as f:
        phones = f.read()
        f_num = phones.split("*")
        print(phones)
        #f_num = [x for x in number if x]
        return f_num
def get_num_from_window():
    phone_num= inte.get()
    sayer_ar(phone_num)
    sayer_ar('هل صحيح ام لا ')
    command = take_command()
    if command == "صحيح" :
        with open("phones.txt",'a') as f:
            f.write(f'{phone_num}*')
        sayer_ar(' هل تريد رقم اخر اجل ام لا ')
        command = take_command()
        if command == 'اجل' :
            win.destroy()
            phone_window()
        else:
            win.destroy()
            print('okkkk')
        print(phone_num)
    else:
        sayer_ar("سوف يتم فتح نافذه جديده لكتابه الرقم")
        phone_window()
def phone_window():
    global inte,win
    add_admin_win= Tk()
    add_admin_win.geometry('330x80')
    add_admin_win.title('ادخل رقم للمشرف')
    add_admin_win.config(bg='#e0e9f7')
    win = add_admin_win
    inte= Entry(win,background='#c2d4f0',width=20,font=(12))
    inte.pack(pady=10)
    inte.focus()
    inte.bind("<Return>", lambda event: get_num_from_window())
    add_admin_win.mainloop()
def close_program_by_name(program_name):
    for proc in psutil.process_iter(attrs=['name']):
        if program_name.lower() in proc.info['name'].lower():  # تحقق من اسم البرنامج
            try:
                proc.kill()  # قتل العملية
                print(f"تم إغلاق البرنامج {program_name}")
            except psutil.NoSuchProcess:
                print(f"لم يتم العثور على العملية: {program_name}")
            except psutil.AccessDenied:
                print(f"لا يوجد إذن لإغلاق العملية: {program_name}")
            except psutil.ZombieProcess:
                print(f"العملية {program_name} هي عملية ميتة ولا يمكن قتلها")
def close_program():
    close_program_by_name('EL.NOUR.exe')
def send_msg(message):
    print('sending msg')
    while True:
        try:
            phone_lists = return_list()
            if len(phone_lists) != 0:
                for number in phone_lists:
                    if number != '':
                        print(f'this the number : {number}')
                        time_ = datetime.datetime.now()
                        print(time_)
                        now = time_.strftime('%H %M')
                        print(now)
                        hour, mine = now.split(' ')
                        mine = int(mine) 
                        print(f"hour:{hour}, min:{mine}")
                        kit.sendwhatmsg(f"{number}", message, int(hour),mine+1)
                        pg.press('Enter')
                        time.sleep(10)
                        pg.press('Enter')
                        time.sleep(3)
                        pg.hotkey("alt", "space")
                        time.sleep(0.5)
                        pg.press("n")
                        #close_program_by_name('chrome.exe')
                    else:
                        break
                break
        except Exception as e:
             print(f'{e}')
             time.sleep(15)
             continue
def every_day_msg():
    def get_medic():
        with open('time_sheets2.txt','a') as f:
            pass
        with open('time_sheets2.txt', 'r') as f2:
            text = f2.read()
            text = text.split('*')
            medics = [x for x in text if x]
            print(f"this the medic will send it :{medics}")
            for text in medics:
                date, name = text.split(',')
                send_msg(f'وقت الدواء هو {date}واسمه هو {name} ')
    schedule.every().day.at('00:01').do(get_medic)
    while True:
        schedule.run_pending()
        time.sleep(1)
print('waiting to send msg')
msg_thread = threading.Thread(target=every_day_msg , daemon=True)
def start_timer():
    while True:
        my_time = datetime.datetime.now()
        now = my_time.strftime("%Y-%m-%d %H:%M:%S")
        with open('time_sheets2.txt', 'r') as f:
            text = f.read()
            text = text.split('*')
            medics = [x for x in text if x]
            for text in medics:
                date, name = text.split(',')
                if date == now:
                    print(f"take your medicine : {name}")
                    alarm=AudioSegment.from_mp3('alarm.mp3')
                    play(alarm)
                    sayer_ar(f'حان الان موعد دواء {name}')
                    send_msg(f' حان الان موعد دواء : {name} ')
def timer():
    my_time = datetime.datetime.now()
    now = my_time.strftime("%Y-%m-%d %H:%M:%S")
    with open ('time_sheets.txt','a') as f :
            pass
    def check(medic_time):
        medic_times = []
        while True:
            my_time = datetime.datetime.now()
            now = my_time.strftime("%Y-%m-%d %H:%M:%S")
            if medic_time == now:
                with open('time_sheets2.txt', 'r') as f:
                    text = f.read()
                    text = text.split('*')
                    medics = [x for x in text if x]
                    for text in medics:
                        date, name = text.split(',')
                        print(f'date : {date} name : {name}')
                        if date == now:
                            print(f"take your medicine : {name}")
                            print(len(medic_time))
                            alarm=AudioSegment.from_mp3('alarm.mp3')
                            play(alarm)
                            sayer_ar(f'حان الان موعد دواء {name}')
                            send_msg(f' حان الان موعد دواء : {name}')
                    break
            else:
                continue
    def main(medic_time):
        print(f'main:{medic_time}')
        sort_time = []
        my_time = datetime.datetime.now()
        now = my_time.strftime("%Y-%m-%d %H:%M:%S")
        with open ('time_sheets.txt','a') as f :
            pass
        with open('time_sheets.txt', 'r') as f:
            all_times = f.read()
            times = all_times.split('*')
            for medic_time in times:
                sort_time.append(medic_time)
            sort_time = [x for x in sort_time if x]
            sort_time.sort(key=lambda a: time_lib.strptime(a, '%Y-%m-%d %H:%M:%S')[0:6])
            # sort_time=sort_(sort_time)
            print(sort_time)
            for time_ in sort_time:
                if time_ < now:
                    print(f'{time_} is finished already')
                    continue
                else:
                    print(f'{time_} wait....')
                    check(time_)
    def start():
        list_time = []
        def enter_window():
            def save_data():
                global year, month, day, hour, minute, second, medicine_name, another_time
                try:
                    year = year_entry.get()
                    month = month_entry.get()
                    day = day_entry.get()
                    hour = hour_entry.get()
                    minute = minute_entry.get()
                    second = second_entry.get()
                    medicine_name = medicine_name_entry
                    another_time = anothor_time_entry.get()
                    medic_time = f'{year}-{month}-{day} {hour}:{minute}:{second}'
                    sayer_ar(f'لقد أضفتَ ميعادَ الدواء كالتالي: اجَلْ أم لا؟ {medic_time} واسمُ الدواءِ: {medicine_name}.')
                    sayer_ar('اخْتَرْ اجَلْ امْ لَا')
                    ch = take_command()
                    if ch == "اجل":
                        list_time.append(medic_time)
                        sayer_ar(f'لقد تم اضافه {medicine_name} في الوقت التالي {medic_time}')
                        send_msg(f"لقد تم اضافه {medicine_name} في الوقت التالي {medic_time}")
                    else:
                        enter_window()
                    with open('time_sheets.txt', 'a') as f:
                        f.write(f"{medic_time}*")
                    with open('time_sheets2.txt', 'a') as f:
                        f.write(f"{medic_time},{medicine_name}*")
                    if another_time == '1':
                        enter_window()
                    if another_time == '0':
                        print(list_time)
                        for time_ in list_time:
                            main(time_)
                except Exception as e:
                    messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
                # إعداد واجهة الإدخال باستخدام Tkinter
            root = tk.Tk()
            root.geometry("500x720")
            root.title('اضافه دواء جديد')
            canvas = tk.Canvas(root, width=500, height=720)
            canvas.pack(fill="both", expand=True)
            label_style = {'bg': '#E6F0F5', 'font': ('Arial', 8), 'padx': 1, 'pady': 1, 'fg': '#2e3b4e'}
            entry_style = {'font': ('Arial', 14), 'width': 20, 'fg': '#2e3b4e', 'bd': 2, 'relief': 'solid', 'bg': '#e3fafa', 'highlightthickness': 1, 'highlightcolor': '#2980b9', 'highlightbackground': '#2980b9'}
            # الحقول
            year_entry = tk.Entry(root, **entry_style)
            month_entry = tk.Entry(root, **entry_style)
            day_entry = tk.Entry(root, **entry_style)
            hour_entry = tk.Entry(root, **entry_style)
            minute_entry = tk.Entry(root, **entry_style)
            second_entry = tk.Entry(root, **entry_style)
            anothor_time_entry = tk.Entry(root, **entry_style)
            canvas.create_window(250, 50, window=tk.Label(root, text="السنة:"))
            canvas.create_window(250, 80, window=year_entry)
            canvas.create_window(250, 130, window=tk.Label(root, text="الشهر:"))
            canvas.create_window(250, 160, window=month_entry)
            canvas.create_window(250, 210, window=tk.Label(root, text="اليوم:"))
            canvas.create_window(250, 240, window=day_entry)
            canvas.create_window(250, 290, window=tk.Label(root, text="الساعة:"))
            canvas.create_window(250, 320, window=hour_entry)
            canvas.create_window(250, 370, window=tk.Label(root, text="الدقيقة:"))
            canvas.create_window(250, 400, window=minute_entry)
            canvas.create_window(250, 450, window=tk.Label(root, text="الثانية:"))
            canvas.create_window(250, 480, window=second_entry)
            canvas.create_window(250, 530, window=tk.Label(root, text="منبه اخر (1و0):"))
            canvas.create_window(250, 560, window=anothor_time_entry)
            sayer_ar('اِدْخُلْ اسْمَ الدَّوَاءِ')
            medicine_name_entry = take_command()
            button_color = "#16a085"
            button_hover_color = "#1abc9c"
            def on_enter(e):
                e.widget.config(bg=button_hover_color)
            def on_leave(e):
                e.widget.config(bg=button_color)
            save_button = tk.Button(root, text="إضافة الميعاد", command=lambda: save_data(), bg=button_color, fg="white", font=("Arial", 11, 'bold'), height=1, width=24)
            canvas.create_window(250, 690, window=save_button)
            save_button.bind("<Enter>", on_enter)
            save_button.bind("<Leave>", on_leave)
            def on_enter_pressed(event, next_widget):
                next_widget.focus()
            year_entry.focus()
            year_entry.bind("<Return>", lambda event: on_enter_pressed(event, month_entry))
            month_entry.bind("<Return>", lambda event: on_enter_pressed(event, day_entry))
            day_entry.bind("<Return>", lambda event: on_enter_pressed(event, hour_entry))
            hour_entry.bind("<Return>", lambda event: on_enter_pressed(event, minute_entry))
            minute_entry.bind("<Return>", lambda event: on_enter_pressed(event, second_entry))
            second_entry.bind("<Return>", lambda event: on_enter_pressed(event, anothor_time_entry))
            anothor_time_entry.bind("<Return>", lambda event: save_data())
            root.mainloop()
        enter_window()
    start()
#timer()
def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
    }
    while True:
        sayer_ar('اهْلًا كَيْفَ حَالُكَ؟ اختر ما تريد. الأول: المساعد الذكي، الثاني: إضافة دواء جديد، الثالث: معرفة مواعيد الدواء الرابع: إضافه رقم مشرف خامسا: خروج من البرنامج.')
        command = take_command()
        if command == 'المساعد الذكي':
            print('voice assistant')
            sayer_ar("اهْلًا بِكَ فِي الْمُسَاعِدِ الشَّخْصِيِّ الذَّكِيِّ فِي مَاذَا اِسَاعِدُكَ")
            sayer_ar('اختر ماذا تريد البحث في يوتيوب أو البحث في جوجل أو خروج للعودة إلى الصفحة السابقة')
            command = take_command()
            while True:
                command = take_command('listen')
                if command == 'البحث في يوتيوب':
                    sayer_ar("عَنْ مَاذَا تُرِيدُ انْ تَبْحَثَ فِي ا"
                             "لْيُوتْيُوبْ")
                    search = take_command()
                    sayer_ar(f'هل تريد البحث عن {search} أجل أم لا')
                    command = take_command()
                    if command == 'اجل':
                        pywhatkit.playonyt(search)
                        time.sleep(2)
                    else :
                       sayer_ar('سوف تعود الان الي الصفحه الرئيسيه للمساعد الذكي')
                       continue
                if command == 'البحث في جوجل':
                    sayer_ar('عَنْ مَاذَا تُرِيدُ انْ تَبْحَثَ فِي جُوجَلْ')
                    question = take_command()
                    url = 'https://www.google.com/search?h1+ar+&q={}'.format(question)
                    page = req.get(url, headers=headers)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    try:
                        result = soup.find(class_='wDYxhc').get_text()
                        sayer_ar(result)
                        sayer_ar('سوف تعود الان الي الصفحه الرئيسيه للمساعد الذكي')
                    except Exception as e:
                        sayer_ar('عُذْرًا لَمْ اسْتَطِعْ ايجَادَ نَتِيجِهِ')
                if command == "خروج":
                    break
            main()    
        if command == 'اضافه دواء جديد':
            print('new alarm')
            sayer_ar("اِدْخُلِ السَّنَةَ ثُمَّ اِدْخُلِ الشَّهْرَ ثُمَّ اِدْخُلِ الْيَوْمَ ثُمَّ اِدْخُلِ السَّاعَةَ ثُمَّ اِدْخُلِ الدَّقِيقَةَ ثُمَّ اِدْخُلِ الثَّانِيَةَ ثُمَّ اِدْخُلْ إِن كُنتَ تُرِيدُ مِنَبَّهًا آخَرَ. مُلَاحَظَةٌ: إِن كُنتَ تُرِيدُ مِنَبَّهًا آخَرَ اَكْتُبْ وَاحِدًا، وَإِن كُنتَ لَا تُرِيدُ فَاكْتُبْ صِفْرًا.")
            timer()
        if command == 'مواعيد الدواء التي لدي':
            print('list of alarms')
            table_time()
        if command == 'اضافه مشرف' :
            sayer_ar('ادْخُلْ رَقْمَ الْمُشْرِفِ الَّذِي تُرِيدُهُ')
            phone_window()
        if command == 'خروج':
            close_program()
        else:
            sayer_ar('أرْجُوا الاِعَادَهُ لَمِ أفَْهَََمْ')
def program_info():
    sayer_ar("يوجد اربعة اختيارات: أولًلا المساعد الذكي، الأوامر الخاصة به كالتالي: أولًا: البحث في يوتيوب، ثانيًا: البحث في جوجل، ثالثًا: خروج للخروج من خيار المساعد الذكي. ثاني خاصية وهي إضافة دواء جديد، سوف تقوم بإدخال تاريخ واسم الدواء. ملاحظة: يجب إدخال بيانات الدواء كالتالي: السَنة، الشهر، اليوم، الساعة، الدقيقة، الثانية، وأسم الدواء، وليس غير ذلك. ثالث خاصية وهي معرفة مواعيد الدواء التي لديك بالفعل رابعا رَابِعًا : يُمْكِنُكَ أنْ تَقُومَ بِاضَافِهِ رَقْمٍ لِلْمُشْرِفِ.")
def aboutme():
     sayer_ar("هذا البرنامجُ تمَّ برمجتُهُ وتصميمُهُ بواسطةِ المبرمجِ محمدٍ مصطفى شعبان، تبعًا لمسابقَةٍ في مدرسةِ بورسعيدَ الثانويةِ العسكريةِ.")
def listening():
    while True:
        command = take_command('listen')
        if command == "ابدا":
            main()
        if command == 'الاوامر الخاصه بالبرنامج' :
            program_info()
        if command == 'معلومات عن المطور' :
           aboutme()
        if command == 'خروج':
            close_program()

def main_window():
    listen_thread = threading.Thread(target=listening, daemon=True)
    listen_thread.start()
    timer_thread = threading.Thread(target=start_timer,daemon=True)
    timer_thread.start()
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title('EL.NOUR')
    root.geometry("400x600")
    bg = "#E6F0F5"  
    button_color = "#78C2C4"  
    hover_color = "#5FA9AC" 
    text_color = "#003333"

    img_path = "robot_no_bg.png"  # مسار الصورة
    img = Image.open(img_path)
    robot_img = ctk.CTkImage(img, size=(270, 150))
    label = ctk.CTkLabel(root, text='', image=robot_img)
    label.pack()
    wel = ctk.CTkLabel(
        root,
        text="welcome",
        font=('Arial Rounded MT Bold', 36),
        text_color=text_color,
        bg_color=bg
        )
    wel.pack(pady=10)
    def create_button(parent, text, command):
        btn = ctk.CTkButton(
            parent,
            text=text,
            font=("Arial Rounded MT Bold", 26),
            fg_color=button_color,
            hover_color=hover_color,
            border_width=2,
            text_color=text_color,
            corner_radius=20,
            command=command,
            height=60,
            width=280
        )
        btn.pack(pady=17)
        return btn
    buttons = [
        ("ابدأ", main),
        ("بالبرنامج الخاصة الاوامر", program_info),
        ("المطور عن خاصة معلومات", aboutme),
        ("الخروج", close_program),
    ]
    for text, command in buttons:
        create_button(root, text, command)
    root.mainloop()
main_window()