import customtkinter as ctk
import XInput
from PIL import Image, ImageTk

def main():

    TRANSPARENT_KEY = "#FF00FF"

    app = ctk.CTk()
    app.geometry("400x400")
    app.title("Test")
    app.configure(fg_color = TRANSPARENT_KEY)
    app.bind("<Escape>", lambda event: app.destroy())
    
    app.wm_attributes("-transparentcolor", TRANSPARENT_KEY)
    #app.overrideredirect(True)

    canvas = ctk.CTkCanvas(
        app, 
        width = 300,
        height = 300,
        bg = TRANSPARENT_KEY,
        highlightthickness = 0,
    )

    canvas.pack(pady = 20)

    

    app.mainloop()


main()