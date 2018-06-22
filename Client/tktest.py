
import tkinter as tk
import cv2
from PIL import Image, ImageTk

cap = cv2.VideoCapture(0)


root = tk.Tk()
root.geometry("500x500")
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(100, show_frame)

show_frame()
root.mainloop()