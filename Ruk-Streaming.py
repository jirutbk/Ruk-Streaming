#region import
import os, sys, glob 
from tkinter import Tk, IntVar, StringVar, Menu, messagebox, filedialog, Listbox, Scrollbar, ttk
#endregion import

#region special function
#ตรวจสอบว่าเป็น path ปกติ หรือ resource_path ของ PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#endregion special function

#region FormInit
mainfrm = Tk()
mainfrm.geometry("315x450+50+150")
mainfrm.resizable(width=False, height=False)
mainfrm.title("Ruk-Streaming 1.00")
mainfrm.wm_iconbitmap(resource_path("Ruk_Streaming_icon.ico"))
#endregion FormInit

#region variable
curr_directory = os.getcwd()
RTMPserver = "rtmp://a.rtmp.youtube.com/live2"
streamingKey = "12t7-dyu6-wj2h-8xxy"

videoSource = ""
videoSourceVar = StringVar(mainfrm, "USB Camera")
audioSource = "" 
audioSourceVar = StringVar(mainfrm, "Microphone (USB Microphone)")
video_size = ""   
video_sizeVar = StringVar(mainfrm, "1280x720")  

compressor = "-af acompressor=threshold=0.089:ratio=9:attack=200:release=1000"
mediaFile = "D:\\temp\\bg002.jpg"
#mediaFile = "D:\\temp\\mv.mp4"
outputFile = "D:\\temp\\test01.mp4"

inputVar = IntVar(mainfrm, 1)       # 1 = Desktop, 2 = Media, 3 = Camera
outputVar = IntVar(mainfrm, 1)      # 1 = File, 2 = Streaming

#endregion variable

#region Main function
x = 0
 
def ask():
    fld = "D:\\temp\\"
    new_fld = input("สร้างโฟลเดอร์ใหม่ (enter ถ้าไม่ต้องการสร้าง)?: ")
    
    if new_fld != "":
        fld = fld + new_fld + "\\"        
        if new_fld not in os.listdir("D:\\temp\\"):
            os.mkdir(fld)
    filename = input("ป้อนชื่อไฟล์ : ")
    filename = fld + filename + ".mp4"
    return filename
 
def stream():
    video_size = video_sizeVar.get()
    videoSource = videoSourceVar.get()
    audioSource = audioSourceVar.get()

    if(outputVar.get()==1):     #record to file
        if(inputVar.get()==1):  #desktop
            os.system(f"""ffmpeg -y -rtbufsize 200M -f gdigrab -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -i audio="{audioSource}" {compressor} -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -c:a aac -strict -2 -ac 2 -b:a 128k -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{outputFile}" """)
        elif(inputVar.get()==2): #media
            if(0):  #is picture
                os.system(f"""ffmpeg -y -loop 1 -i {mediaFile} -f dshow -i audio="{audioSource}" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "{outputFile}" """)
            else:   #is Video  
                os.system(f"""ffmpeg -y -i {mediaFile} -f dshow -i audio="{audioSource}" -c:a aac "{outputFile}" """)

        elif(inputVar.get()==3): #camera
            os.system(f"""ffmpeg -y -f dshow -i video="{videoSource}" -f dshow -channel_layout stereo -thread_queue_size 1024 -i audio="{audioSource}" {compressor} -c:v libx264 -r 10 -preset fast -tune zerolatency -crf 25 -pix_fmt yuv420p -c:a aac -strict -2 -ac 2 -b:a 128k "{outputFile}" """)

    elif(outputVar.get()==2):   #streaming to youtube
        if(inputVar.get()==1):  #desktop
            os.system(f"""ffmpeg -f gdigrab -framerate 30 -video_size {video_size} -i desktop -f dshow -i audio="{audioSource}" -c:v libx264 -preset fast -crf 26 -maxrate 2500k -bufsize 5000k -g 60 -vf format=yuv420p -c:a aac -b:a 128k -f flv {RTMPserver}/{streamingKey} """)
        elif(inputVar.get()==2): #media
            if(1):  #is picture
                os.system(f"""ffmpeg -y -loop 1 -i {mediaFile} -f dshow -i audio="{audioSource}" -c:v libx264 -tune stillimage -c:a aac -b:a 128k -f flv {RTMPserver}/{streamingKey} """)
            else:   #is Video  
                os.system(f"""ffmpeg -y -i {mediaFile} -f dshow -i audio="{audioSource}" -c:v libx264 -preset fast -crf 26 -maxrate 2500k -bufsize 5000k -g 60 -vf format=yuv420p -c:a aac -b:a 128k -f flv {RTMPserver}/{streamingKey} """)
        elif(inputVar.get()==3): #camera
            os.system(f"""ffmpeg -y -f dshow -i video="{videoSource}" -f dshow -i audio="{audioSource}" -c:v libx264 -preset fast -crf 26 -maxrate 2500k -bufsize 5000k -g 60 -vf format=yuv420p -c:a aac -b:a 128k -f flv {RTMPserver}/{streamingKey} """)


def preview():
    if(inputVar.get()==2):
        os.system(f"""ffplay {mediaFile}""")
    elif(inputVar.get()==3):
        os.system(f"""ffplay -f dshow -i video="{videoSource}" """)

 

def msgAbout():    
    messagebox.showinfo("เกี่ยวกับโปรแกรม", "โปรแกรม : Ruk-Streaming v 1.0\n ผู้พัฒนา : Tanunnas BK")

def openDir():
    global dirName
    dirName = filedialog.askdirectory(title="เลือกโฟลเดอร์สื่อ..", initialdir=curr_directory) 
    listPic.delete(0,"end")       #clear
    files = os.listdir(dirName) 
    for name in files:  
        if (name.endswith(".jpg") or name.endswith(".png") or name.endswith(".mp4")):   #แสดงเฉพาะ .jpg .png .mp4
            listPic.insert('end', name)

#endregion Main function

#region GUI
# Menubar
menubar = Menu(mainfrm)
file = Menu(menubar, tearoff=0)
file.add_command(label="Open Folder..", command=openDir)
file.add_separator()
file.add_command(label="Exit", command=mainfrm.quit)
menubar.add_cascade(label="File", menu=file)

selectmnu = Menu(menubar, tearoff=0)
selectmnu.add_checkbutton(label="HD 720p (1280x720)", onvalue="1280x720", variable=video_sizeVar)
selectmnu.add_checkbutton(label="Standard 480p (854x480)", onvalue="854x480", variable=video_sizeVar)
selectmnu.add_checkbutton(label="Traditional 360p (640x360)", onvalue="640x360", variable=video_sizeVar)
menubar.add_cascade(label="VDO size", menu=selectmnu)

select1mnu = Menu(menubar, tearoff=0)
select1mnu.add_checkbutton(label="WebCam", onvalue="USB Camera", variable=videoSourceVar)
select1mnu.add_checkbutton(label="ManyCam", onvalue="ManyCam Virtual Webcam", variable=videoSourceVar)
menubar.add_cascade(label="Camera", menu=select1mnu)

select2mnu = Menu(menubar, tearoff=0)
select2mnu.add_checkbutton(label="Microphone", onvalue="Microphone (USB Microphone)", variable=audioSourceVar)
select2mnu.add_checkbutton(label="Stereo Mix", onvalue="Stereo Mix (Realtek High Definition Audio)", variable=audioSourceVar)
select2mnu.add_checkbutton(label="ManyCam", onvalue="Microphone (ManyCam Virtual Microphone)", variable=audioSourceVar)
menubar.add_cascade(label="Audio", menu=select2mnu)

menubar.add_cascade(label="About", command=msgAbout)
mainfrm.config(menu=menubar)

lblfrm = ttk.LabelFrame(mainfrm, text="Media Files")
lblfrm.grid(column=0, row=0, columnspan=2, padx=10, pady=5, sticky="w")
listPic = Listbox(lblfrm, name="listPic", height=12, width=45)

listPic.pack(side="left", fill="y", pady=2)

scrollbar1 = Scrollbar(lblfrm, orient="vertical" )
scrollbar1.config(command=listPic.yview)            #เชื่อมกับ listbox
scrollbar1.pack(side="left", fill="y", pady=2)

listPic.config(yscrollcommand=scrollbar1.set)       #เชื่อมกับ scrollbar

lblfrm1 = ttk.LabelFrame(mainfrm, text="Video input")
lblfrm1.grid(column=0, row=1, padx=10, pady=0, sticky="w")
rdo1 = ttk.Radiobutton(lblfrm1, text="Desktop", width=21, variable=inputVar, value=1).grid(column=0, row=0, sticky="w", padx=10, pady=2)
rdo2 = ttk.Radiobutton(lblfrm1, text="Media", variable=inputVar, value=2).grid(column=0, row=1, sticky="w", padx=10, pady=2)
rdo3 = ttk.Radiobutton(lblfrm1, text="Camera", variable=inputVar, value=3).grid(column=0, row=2, sticky="w", padx=10, pady=2)

lblfrm2 = ttk.LabelFrame(mainfrm, text="Output")
lblfrm2.grid(column=1, row=1, padx=0, pady=0, sticky="w")
rdo4 = ttk.Radiobutton(lblfrm2, text="File", width=9, variable=outputVar, value=1).grid(column=0, row=0, sticky="w", padx=10, pady=2)
rdo5 = ttk.Radiobutton(lblfrm2, text="Streaming", variable=outputVar, value=2).grid(column=0, row=1, sticky="w", padx=10, pady=2)

lblfrm3 = ttk.LabelFrame(mainfrm, text="Streaming config")
lblfrm3.grid(column=0, row=2, columnspan=2, padx=10, pady=0, sticky="w")
lbl1 = ttk.Label(lblfrm3,text="Streaming key: ")
lbl1.grid(column=0, row=0, pady=5, padx=5)
enKey = ttk.Entry(lblfrm3, width=25)
enKey.grid(column=1, row=0, padx=7, pady=5)
bntPreview = ttk.Button(lblfrm3, text="Preview", command=preview)
bntPreview.grid(column=0, row=1, padx=10, pady=10)
bntStream = ttk.Button(lblfrm3, text="Streaming", command=stream)
bntStream.grid(column=1, row=1, padx=10, pady=10)
#bntStream.config(state="disabled")  #ปิดการใช้งานปุ่ม Stream

#endregion GUI

mainfrm.mainloop()
