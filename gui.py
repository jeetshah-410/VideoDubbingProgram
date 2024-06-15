from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Button, PhotoImage
from main import main_func

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Translator\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
def display_selected_option():

    display_label.config(text='''JEET SHAH
    SARVESH HIWARKAR
    RISHIRAJ AWASTHI
    PARIKSHIT DAIVADNYA
    PRAHARSH BHONDE
    SANIKA GAIKWAD''')

    window.after(5000, clear_displayed_text)
def update_gif(label, frame_number, gif_frames, after_id):
    frame = gif_frames[frame_number]
    label.configure(image=frame)
    frame_number = (frame_number + 1) % len(gif_frames)
    after_id[0] = label.after(100, update_gif, label, frame_number, gif_frames, after_id)

def main1():
    gif_path = "load" 
    gif_image = Image.open(gif_path)

    gif_frames = []
    try:
        while True:
            frame = gif_image.copy()
            gif_frames.append(ImageTk.PhotoImage(frame))
            gif_image.seek(len(gif_frames)) 
    except EOFError:
        pass

    gif_label = tk.Label(window)
    gif_label.pack()
    x_position = 550
    y_position = 150
    gif_label.place(x=x_position, y=y_position)

    after_id = [None]  
    update_gif(gif_label, 0, gif_frames, after_id)



def clear_displayed_text():
    display_label.config(text="ACKNOWLEDGEMENTS: ")
def open_file_dialog():
    global a
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])
    if file_path:
        display_label.config(text="VIDEO FILE SELECTED SUCCESSFULLY!!!")
        window.after(2000, clear_displayed_text)
    
    a = file_path


def setselect():
    selected_option = dropdown_var.get()
    print(selected_option)
    if selected_option=="HINDI":
        b='hi'
    elif selected_option=="MARATHI":
        b='mr'
    elif selected_option=="GUJRATI":
        b='gu'
    elif selected_option=="TAMIL":
        b='ta'
    elif selected_option=="TELUGU":
        b='te'
    elif selected_option=="KANNADA":
        b='kn'
    elif selected_option=="MALAYALAM":
        b='ml'
    elif selected_option=="BENGALI":
        b='bn'

    print(b)
    display_label.config(text=f"THE SELECTED LANGUAGE IS: {selected_option}")
    window.after(3000, clear_displayed_text)
    main_func(video_file= a, lang = b)


def gifdisp():
    gif_path = "loading.gif"
    gif_image = Image.open(gif_path)
    gif_photo = ImageTk.PhotoImage(gif_image)


window.geometry("1063x579")
window.configure(bg = "#FFFFFF")



canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 579,
    width = 1063,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    532.0,
    289.0,
    image=image_image_1
)

canvas.create_rectangle(
    531.0,
    133.0,
    532.0,
    579.0,
    fill="#FFFAFA",
    outline="")

canvas.create_rectangle(
    8.0,
    132.0,
    1082.0,
    134.0,
    fill="#FFFFFF",
    outline="")
dropdown_var = tk.StringVar()

# label to display the selected option
display_label = tk.Label(window, text="ACKNOWLEDGEMENTS: ", font=("Times New Roman",15))
display_label.pack(pady=100)
x_position = 650
y_position = 250
display_label.place(x=x_position, y=y_position)
display_label1 = tk.Label(window, text="SELECT LANGUAGE: ", font=("Times New Roman",15))
display_label1.pack(pady=100)
x_position = 150
y_position = 250
display_label1.place(x=x_position, y=y_position)

# dropdown menu
options = ["MARATHI", "HINDI", "GUJRATI", "TAMIL", "TELUGU", "KANNADA", "MALAYALAM", "BENGALI"]
dropdown = tk.OptionMenu(window, dropdown_var, *options)
dropdown.pack(pady=10)
x_position = 200
y_position = 300
dropdown.place(x=x_position, y=y_position)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command= open_file_dialog,
    relief="flat"
)
button_1.place( y=159.0,
    width=324.0000305175781,
    height=63.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=display_selected_option,
    relief="flat"
)
button_2.place(
    x=0.0,
    y=541.0,
    width=150.0,
    height=37.99732971191406
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=setselect,
    relief="flat"
)
button_3.place(
    x=165.0,
    y=385.0,
    width=124.0,
    height=41.0
)




window.resizable(False, False)
window.mainloop()
