import os
import tkinter   as tk
import threading as thrd
from time               import sleep
from tkinter.messagebox import showerror
from functools          import partial
from playsound          import playsound
from win10toast         import ToastNotifier as notif

class Timer:
	iconPath  = "icon.ico"
	soundPath = "alert.mp3"

	def __init__(self):
		self.initWindow()
		self.initVar()
		self.initUI()
		
		self.isLoop = False
		self.root.mainloop()

	def initWindow(self):
		self.root = tk.Tk()
		self.root.configure(bg="black")
		self.root.geometry("360x240")
		self.root.title("Countdown Timer")
		self.root.iconbitmap(self.iconPath)
		self.root.resizable(False, False)
		self.root.bind_all("<Button-1>", lambda evt: evt.widget.focus_set())
		self.root.bind_all("<Button-2>", lambda evt: evt.widget.focus_set())
		self.root.bind_all("<Button-3>", lambda evt: evt.widget.focus_set())
		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)

	def initVar(self):
		self.hourValue = tk.StringVar(value="00")
		self.hourValue.trace('w', partial(self.limitInput, self.hourValue))
		self.minValue = tk.StringVar(value="00")
		self.minValue.trace('w', partial(self.limitInput, self.minValue))
		self.secValue = tk.StringVar(value="00")
		self.secValue.trace('w', partial(self.limitInput, self.secValue))

		self.msecValue = tk.StringVar(value="00")
		self.msecValue.trace('w', partial(self.limitInput, self.msecValue))

	def initUI(self):
		frame = tk.Frame(self.root, bg="black")
		frame.grid(row=0, column=0)

		padding = {"padx": 0, "pady": 10}
		
		tk.Label(frame, font=("Helvetica", 36, "bold"), width=1, text="∶", fg="white", bg="black").grid(row=0, column=1)
		tk.Label(frame, font=("Helvetica", 36, "bold"), width=1, text="∶", fg="white", bg="black").grid(row=0, column=3)
		
		self.e1 = tk.Entry(frame, font=("Helvetica", 36), width=2, justify="center", fg="black", bg="white", disabledforeground="black", disabledbackground="white", textvariable=self.hourValue)
		self.e2 = tk.Entry(frame, font=("Helvetica", 36), width=2, justify="center", fg="black", bg="white", disabledforeground="black", disabledbackground="white", textvariable=self.minValue)
		self.e3 = tk.Entry(frame, font=("Helvetica", 36), width=2, justify="center", fg="red",   bg="white", disabledforeground="red",   disabledbackground="white", textvariable=self.secValue)
		self.e1.grid(row=0, column=0, **padding)
		self.e2.grid(row=0, column=2, **padding)
		self.e3.grid(row=0, column=4, **padding)

		tk.Button(frame, font=("Helvetica", 16), width=6, text="Start", command=self.startTimer).grid(row=1, column=0, **padding)
		tk.Button(frame, font=("Helvetica", 16), width=6, text="Stop",  command=self.stopTimer).grid(row=1, column=2, **padding)
		tk.Button(frame, font=("Helvetica", 16), width=6, text="Clear", command=self.clearTimer).grid(row=1, column=4, **padding)

	def limitInput(self, curVar, *args):
		value = curVar.get()
		if len(value) > 2: curVar.set(value[:2])

	def startTimer(self):
		if int(self.hourValue.get()) + int(self.minValue.get()) / 60 + int(self.secValue.get()) / 3600 > 24:
			showerror("Error", "Time exceeds one day.")
			return

		if self.hourValue.get() == "00" and self.minValue.get() == "00" and self.secValue.get() == "00":
			showerror("Error", "Time is set to zero.")
			return

		if not self.hourValue.get().isnumeric() or not self.minValue.get().isnumeric() or not self.secValue.get().isnumeric():
			showerror("Error", "Error invalid input.")
			self.clearTimer()
			return

		if not self.isLoop:
			thrd.Thread(target=self.countDown).start()
	
	def countDown(self):
		self.isLoop = True

		self.e1.configure(state="disabled")
		self.e2.configure(state="disabled")
		self.e3.configure(state="disabled")

		h, m, s = int(self.hourValue.get()), int(self.minValue.get()), int(self.secValue.get())
		ttSec = h * 3600 + m * 60 + s

		while ttSec > 0 and self.isLoop:
			ttSec -= 1

			m, s = divmod(ttSec, 60)
			h, m = divmod(m, 60)

			self.hourValue.set(f"{h:02}")
			self.minValue.set(f"{m:02}")
			self.secValue.set(f"{s:02}")
			sleep(1)

		if self.isLoop:
			self.isLoop = False
			notif().show_toast("Countdown Timer", "Time is up!", self.iconPath, 3, True)
			playsound(self.soundPath)
			self.e1.configure(state="normal")
			self.e2.configure(state="normal")
			self.e3.configure(state="normal")

	def stopTimer(self):
		self.isLoop = False
		self.e1.configure(state="normal")
		self.e2.configure(state="normal")
		self.e3.configure(state="normal")
	
	def clearTimer(self):
		self.isLoop = False
		self.hourValue.set("00")
		self.minValue.set("00")
		self.secValue.set("00")
		self.e1.configure(state="normal")
		self.e2.configure(state="normal")
		self.e3.configure(state="normal")

if __name__ == "__main__":
	Timer()