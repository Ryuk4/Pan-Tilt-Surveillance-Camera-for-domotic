from Tkinter import *
import pigpio
import time
import cv2
import ImageTk
import Image

servo_pano = 18
servo_pano_min = -50
servo_pano_mid = 0
servo_pano_max = 50
#15.5*x+1275

servo_pano = 23
servo_pano_min = -10
servo_pano_mid = 0
servo_pano_max = 50
#15*x+650

pi = pigpio.pi()  #let's you control the GPIO pins of your raspberry pi
cap = cv2.VideoCapture(0)  #opens your camera with opencv 

class App:			
	def __init(self,master,cap):
		self.master = master
		self.cap = cap
		self.videoOn = False
		frame = Frame(self.master)
		frame.pack()
		self.var_pano = IntVar()
		self.var_incl = IntVar()
		scale_hori = Scale(frame, from_=-50, to=50, orient=HORIZONTAL, command=self.update_pano)
		scale_hori.grid(row=0)
		
		scale_vert = Scale(frame, from_=-10, to=50, orient=VERTICAL, command=self.update_incl)
		scale_vert.grid(row=1)
		button_start = Button(frame, text="Start Video", command=self.start_video)
		button_start.grid(row=2)
		button_stop = Button(frame, text="Stop Video, command=self.stop_video)
		button_stop.grid(row=3)
					
		self.cap.read()
		self.cap.read()
		self.cap.read()
		self.cap.read()    #clear camera buffer
		ret, img = self.cap.read()
		im = Image.fromarray(img)
		imtk = ImageTk.PhotoImage(image=im)
		self.label = Label(frame, image=imtk)
		self.label.image = imtk
		self.label.grid(row=4)
		
		self.master.bind('<Left>', self.left_key)
		self.master.bind('<Right>', self.right_key)
		self.master.bind('<Up>',self.up_key)
		self.master.bind('<Down>',self.down_key)
		self.master.bind('<space>', self.update_img)
			
	def update_pano(self,angle):
		duty = float(angle) * 15.5 + 1275
		pi.set_servo_pulsewidth(18,duty)
	
	def update_incl(self,angle):
		duty = float(angle) * 15 + 650
		pi.set_servo_pulsewidth(23,duty)
		
	def update_img_but(self):
		self.cap.read()
		self.cap.read()
		self.cap.read()
		self.cap.read()
		ret, img = self.cap.read()
		im = Image.fromarray(img)
		imtk = ImageTk.PhotoImage(image=im)
		self.label.configure(image=imtk)
		self.label.image = imtk
		if(self.videoOn):
			self.master.after(600,self.update_img_but)
			
	def start_video(self):
		self.videoOn = True
		self.update_img_but()

	def stop_video(self):
		self.videoOn = False

	def update_img(self,event):
		t1 = time.time()
		self.cap.read()
		self.cap.read()
		self.cap.read()
		self.cap.read()
		ret, img = self.cap.read()
		im = Image.fromarray(img)
		imtk = ImageTk.PhotoImage(image=im)
		self.label.configure(image=imtk)
		self.label.image = imtk
		t2 = time.time()
		print t2-t1

	def right_key(self,event):
		if self.var_pano > -50:
			self.var_pano.set(self.var_pano.get() - 5)
			self.update_pano(self.var_pano.get())
	
	def left_key(self,event):  
		if self.var_pano < 50:   
			self.var_pano.set(self.var_pano.get() + 5)   
			self.update_pano(self.var_pano.get())
	
	def up_key(self,event):  
		if self.var_incl > -10:   
			self.var_incl.set(self.var_incl.get() - 5)   
			self.update_incl(self.var_incl.get())
	
	def down_key(self,event):  
		if self.var_incl < 50:   
			self.var_incl.set(self.var_incl.get() + 5)   
			self.update_incl(self.var_incl.get())

root = Tk()
app = App(root,cap)
root.mainloop()
