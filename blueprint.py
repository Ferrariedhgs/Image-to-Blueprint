import tkinter as tk
from tkinter import Tk, Button, filedialog, Label, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np

PREVIEW_W = 300
PREVIEW_H = 200

raw_img=np.zeros((1,1,3), np.uint8)
converted_img=np.zeros((1,1,3), np.uint8)
conv_img_preview=Image.new('RGB', (1,1))

def load_file():
    global raw_img
    path = filedialog.askopenfilename()
    raw_img = cv2.imread(path)
    raw_img_preview=Image.fromarray(raw_img)
    raw_img_preview.thumbnail((PREVIEW_W, PREVIEW_H))

    tk_img = ImageTk.PhotoImage(raw_img_preview)
    raw_image_label.config(image=tk_img)
    raw_image_label.image = tk_img

    conv_image_label.image = tk_img
    conv_image_label.config(image=tk_img)


def conv_image():
    global converted_img
    converted_img= cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)

    if mode_var.get()==0: #Sobel
        img_s_dx = cv2.Sobel(converted_img, cv2.CV_64F, 1, 0)
        img_s_dy = cv2.Sobel(converted_img, cv2.CV_64F, 0, 1)
    elif mode_var.get()==1: #Scharr
        img_s_dx = cv2.Scharr(converted_img, cv2.CV_64F, 1, 0)
        img_s_dy = cv2.Scharr(converted_img, cv2.CV_64F, 0, 1)
    converted_img = cv2.addWeighted(img_s_dx, 0.5, img_s_dy, 0.5, 0)
    converted_img = cv2.convertScaleAbs(converted_img)

    #turn black to blue
    mask = cv2.inRange(converted_img, 0,slider_threshold.get())
    converted_img= cv2.cvtColor(converted_img, cv2.COLOR_GRAY2BGR)
    converted_img[mask > 0] = [255, 0, 0]

    #add grid
    rows=int(slider_rows.get())
    cols=int(slider_columns.get())
    thickness = int(slider_thickness.get())
    color = (255, 255, 255)
    height, width = converted_img.shape[:2]

    if thickness>0:
        #draw vertical lines
        for c in range(1, cols):
            x = c * width // cols
            cv2.line(converted_img, (x, 0), (x, height), color, thickness)

        #draw horizontal lines
        for r in range(1, rows):
            y = r * height // rows
            cv2.line(converted_img, (0, y), (width, y), color, thickness)

    #cv2.imshow("Converted Image",converted_img)

    rgb_conv_img_preview = cv2.cvtColor(converted_img, cv2.COLOR_BGR2RGB)
    conv_img_preview=Image.fromarray(rgb_conv_img_preview)
    conv_img_preview.thumbnail((PREVIEW_W, PREVIEW_H))
    
    tk_img = ImageTk.PhotoImage(conv_img_preview)
    conv_image_label.config(image=tk_img)
    conv_image_label.image = tk_img

def save_image():
    path = filedialog.asksaveasfilename(
    defaultextension=".png",
    filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
    )
    cv2.imwrite(path, converted_img)
    messagebox.showinfo("Info","Image saved")



root = Tk()
root.title("Image to blueprint")
root.geometry("700x500")




#buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

img_load = Button(button_frame, text="Load Image", command=load_file)
img_load.grid(row=0, column=0, padx=10)

img_conv=Button(button_frame,text="Convert Image", command=conv_image)
img_conv.grid(row=0, column=1, padx=10)

img_conv=Button(button_frame,text="Save Image", command=save_image)
img_conv.grid(row=0, column=2, padx=10)

grid_label=tk.Label(button_frame,text="Grid")
grid_label.grid(row=1, column=1, pady=(40,0))


slider_rows = tk.Scale(button_frame, from_=0, to=50, orient=tk.HORIZONTAL)
slider_rows.grid(row=2, column=0, padx=10)

slider_columns = tk.Scale(button_frame, from_=0, to=50, orient=tk.HORIZONTAL)
slider_columns.grid(row=2, column=1, padx=10)

slider_thickness = tk.Scale(button_frame, from_=0, to=25, orient=tk.HORIZONTAL)
slider_thickness.grid(row=2, column=2, padx=10)

row_label=tk.Label(button_frame,text="Rows")
row_label.grid(row=3, column=0, padx=10)
col_label=tk.Label(button_frame,text="Columns")
col_label.grid(row=3, column=1, padx=10)
thk_label=tk.Label(button_frame,text="Thickness")
thk_label.grid(row=3, column=2, padx=10)

slider_threshold = tk.Scale(button_frame, from_=0, to=255, orient=tk.HORIZONTAL)
slider_threshold.grid(row=4, column=2, padx=10)
slider_threshold.set(40)
thk_label=tk.Label(button_frame,text="Filter Threshold")
thk_label.grid(row=5, column=2, padx=10)

mode_var = tk.IntVar(value=0)
mode_sobel = tk.Radiobutton(button_frame, text="Sobel Filter", variable=mode_var, value=0)
mode_scharr = tk.Radiobutton(button_frame, text="Scharr Filter", variable=mode_var, value=1)
mode_sobel.grid(row=4, column=0, padx=10)
mode_scharr.grid(row=4, column=1, padx=10)



#images
image_grid=tk.Frame(root)
image_grid.pack(pady=10)

raw_image_label = tk.Label(
    image_grid,
    width=PREVIEW_W,
    height=PREVIEW_H,
)
raw_image_label.grid(row=0, column=0, padx=10, pady=10)

conv_image_label = tk.Label(
    image_grid,
    width=PREVIEW_W,
    height=PREVIEW_H,
)
conv_image_label.grid(row=0, column=1, padx=10, pady=10)





root.mainloop()
