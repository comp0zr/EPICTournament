import tkinter as tk
import fileinput
import threading
import cv2
import datetime
from PIL import ImageTk, Image
from FaceRecognition import *

class SetupWizard(object):       
    window = None
    panel = None
    video_frame = None
    image_panel = None
    next_button = None
    instruction_text = None

    initialize_step = True    
    is_recording = False

    detector = None

    curr_step = 0    
    steps = []
    instructions = []    
    
    user_data = []

    """____________________________________________"""

    def Initilize(self):
        file = open('WizardInstructions.txt')
        text = file.read()                

        self.instructions = text.split('___\n')
        self.window = tk.Tk()        
        self.window.geometry("900x600")                              

        self.instruction_text = tk.Text(self.window, height = 8, width = 100)
        self.instruction_text.configure(font=("Calibri Light",18))
        self.instruction_text.pack()
        self.instruction_text.insert(tk.END, self.instructions[0])
        
        self.image_panel = tk.Label(self.window)
        
        self.steps = [
            self.SetUpCamera, 
            self.AdjustPosture, 
            self.RecordData
        ]

        self.next_button = tk.Button(self.window, text = "Next", command=self.NextStep)
        self.next_button.pack(anchor = "sw", side="bottom", ipadx=30, ipady=10)


    def __init__(self):
        self.Initilize()                
        self.RunWizard()            
            

    def RunWizard(self):
        while True:
            self.steps[self.curr_step]()
            self.window.update_idletasks()            
            self.window.update()


    def NextStep(self):                
        self.curr_step += 1
        self.instruction_text.delete("1.0", "end")
        self.instruction_text.insert(tk.END, self.instructions[self.curr_step])
        self.initialize_step = True
        
    
    # Step 1
    def SetUpCamera(self):        
        image = Image.open("C:/EPIC/Images/WebcamPositionExample.jpg")
        image = ImageTk.PhotoImage(image.resize((350,200)))

        if self.initialize_step == True:
            self.image_panel = tk.Label()
            self.image_panel.image = image            
            self.image_panel.pack(ipady=50)
            self.initialize_step = False
        else:
            self.image_panel.configure(image=image)
            self.image_panel.image = image
    
    # Step 2
    def AdjustPosture(self):                
        image = ImageTk.PhotoImage(
            Image.open("C:/EPIC/Images/Ergonomics_example.png").resize((154,200))
        )

        if self.initialize_step == True:            
            self.image_panel.configure()
            self.initialize_step = False
        

        self.image_panel.configure(image=image)
        self.image_panel.image = image        
        self.image_panel.update_idletasks()
        self.image_panel.update()            
        
    temp = []
    display_times = {}

    # Step 3
    def RecordData(self):        
        if self.initialize_step == True:            
            self.user_data = []
            self.next_button.configure(text="Begin Capture", command=self.StartCapture)            
            self.initialize_step = False            
            return

        if self.is_recording:
            data = self.detector.GetData()
            frame, rects = data            

            self.temp += rects

            if len(self.temp) >= 100:
                rects = self.temp
                self.temp = []

                filtered = FaceData.Filter(rects)
                self.user_data.extend(filtered)

                print(F"RECTS: {len(rects)}")
                print(F"FILTERED: {len(filtered)}")
                print(F"TOTAL: {len(self.user_data)}")
                print('='*20)

                filtered = [Rect(int(rect), color=(0,255,0)) for rect in filtered]
                rects = [Rect(int(rect), color=(255,0,0)) for rect in rects if rect not in filtered]
                self.UpdateDisplay([frame, filtered + rects])
            else:
                self.UpdateDisplay([frame, rects])
            
            if len(self.user_data) >= 100:
                self.is_recording = False
                self.NextStep()


    def StartCapture(self):
        self.next_button["state"] = "disabled"
        self.detector = FaceDetector(self.window)
        self.is_recording = True

        thread = threading.Thread(target=self.detector.Execute, args=())
        thread.start()



    def UpdateDisplay(self, data):                 
        frame, objects = data

        for obj in objects:
            if type(obj) is Rect:                             
                obj.Display(frame)

        try:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        
            image = Image.fromarray(image)    
            image = ImageTk.PhotoImage(image)
    
            if self.image_panel is None:            
                self.image_panel = tk.Label(image = image)
                self.image_panel.image = image
                self.image_panel.pack(side='left', padx=10, pady=10)
            else:
                self.image_panel.configure(image=image)
                self.image_panel.image = image 
        except:
            pass
        self.window.update_idletasks()
        self.window.update()