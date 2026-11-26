import json
import ctypes
import sdl2
import customtkinter as ctk
from PIL import Image, ImageTk

class InputDisplay(ctk.CTk):

    def __init__(self):
        super().__init__(fg_color = "Gray25")

        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK | sdl2.SDL_INIT_GAMECONTROLLER)

        self.n64MapDefault = {
            "A": "B",
            "B": "A", 
            "X": "C-LEFT", 
            "Y": "C-DOWN", 
            "START": "C-UP",
            "BACK": "C-RIGHT", 
            "LEFTSHOULDER": "L", 
            "RIGHTSHOULDER": "R", 
            "DPUP": "D-UP", 
            "DPDOWN": "D-DOWN", 
            "DPLEFT": "D-LEFT",
            "DPRIGHT": "D-RIGHT",
            "GUIDE": "START",
            "Z": "Z"
        }

        self.n64Layout = {
            "A": (280, 220),
            "B": (245, 175),
            "C-UP": (335, 125),
            "C-DOWN": (335, 185),
            "C-LEFT": (305, 155),
            "C-RIGHT": (365, 155),
            "START": (175, 175),
            "Z": (173, 125),
            "L": (100, 110),
            "R": (245, 110),
            "D-RIGHT": (80, 175),
            "D-UP": (80, 175),
            "D-LEFT": (80, 175),
            "D-DOWN": (80, 175), 
            "THUMB_BASE": (175, 265)
        }

        self.standardController = None # For use with standard controllers, i.e, XBox, Playstation, Switch
        self.genericController = None #For use with generic gamepads that use raw usb data
        self.activeDevice = None # Id of connected controller

        self.prevButtons = {} # dictionary of previous state of all controller inputs.

        self.statusLabel = ctk.CTkLabel(self, text = "Looking for Controller...")
        self.statusLabel.pack(pady = 10)

        self.canvas = ctk.CTkCanvas(
            self, 
            width = 450,
            height = 350,
            bg = "Gray25",
            highlightthickness = 0
        )
        self.canvas.pack()

        self.UIElements = {
            "A": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/A_Button.png").resize((48, 48))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/A_Button_Pressed.png").resize((48, 48))),
            ),
            "B": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/B_Button.png").resize((48, 48))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/B_Button_Pressed.png").resize((48, 48))),
            ),
            "C-UP": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/C_UP_Button.png").resize((32, 32))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/C_UP_Button_Pressed.png").resize((32, 32))),
            ),
            "C-DOWN": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/C_DOWN_Button.png").resize((32, 32))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/C_DOWN_Button_Pressed.png").resize((32, 32))),
            ),
            "C-LEFT": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/C_LEFT_Button.png").resize((32, 32))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/C_LEFT_Button_Pressed.png").resize((32, 32))),
            ),
            "C-RIGHT": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/C_RIGHT_Button.png").resize((32, 32))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/C_RIGHT_Button_Pressed.png").resize((32, 32))),
            ),
            "START": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/START_Button.png").resize((48, 48))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/START_Button_Pressed.png").resize((48, 48))),
            ),
            "Z": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/Z_Button.png").resize((32, 32))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/Z_Button_Pressed.png").resize((32, 32))),
            ),
            "L": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/L_Button.png").resize((64, 64))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/L_Button_Pressed.png").resize((64, 64))),
            ),
            "R": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/R_Button.png").resize((64, 64))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/R_Button_Pressed.png").resize((64, 64)))
            ), 
            "D-RIGHT": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/D_RIGHT_Button.png").resize((96, 96))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/D_RIGHT_Button_Pressed.png").resize((96, 96)))
            ),
            "D-UP": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/D_UP_Button.png").resize((96, 96))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/D_UP_Button_Pressed.png").resize((96, 96)))
            ),
            "D-LEFT": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/D_LEFT_Button.png").resize((96, 96))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/D_LEFT_Button_Pressed.png").resize((96, 96)))
            ),
            "D-DOWN": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/D_DOWN_Button.png").resize((96, 96))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/D_DOWN_Button_Pressed.png").resize((96, 96)))
            ), 
            "THUMB_BASE": (
                ImageTk.PhotoImage(Image.open("UIElements/N64/THUMB_BASE.png").resize((96, 96))),
                ImageTk.PhotoImage(Image.open("UIElements/N64/THUMB_BASE.png").resize((96, 96)))
            )
        }

        self.UIButtons = {}
        for button, (xPosition, yPosition) in self.n64Layout.items():
            unpressedImg = self.UIElements[button][0]
            buttonId = self.canvas.create_image(xPosition, yPosition, image = unpressedImg, anchor = "center")
            self.UIButtons[button] = buttonId

        self.stickImage = ImageTk.PhotoImage(Image.open("UIElements/N64/THUMB_STICK.png").resize((96, 96)))
        self.stickX, self.stickY = self.n64Layout["THUMB_BASE"]
        self.stickId = self.canvas.create_image(self.stickX, self.stickY, image = self.stickImage, anchor = "center")

        self.stickCenter = self.canvas.coords(self.stickId)
        self.MAX_OFFSET = 12
        self.prevStick = (0.0, 0.0)


        self.connectController()
        self.updateLoop()

    def updateButtonImage(self, button, isPressed):
        wasPressed = self.prevButtons.get(button, False)

        if isPressed != wasPressed and button in self.UIButtons:    
            newImg = self.UIElements[button][1 if isPressed else 0]
            self.canvas.itemconfig(self.UIButtons[button], image = newImg)

        self.prevButtons[button] = isPressed

    def updateStickImage(self, leftX, leftY):
        if (leftX, leftY) != self.prevStick:
            x, y = self.stickCenter
            self.canvas.coords(
                self.stickId, 
                x + (leftX * self.MAX_OFFSET),
                y + (leftY * self.MAX_OFFSET)
            )
            self.prevStick = (leftX, leftY)
            
    def connectController(self): # Looks for detected controllers and connects first available. Accounts for whether the controller has standard mapping or is generic
        self.closeActive()

        for i in range(sdl2.SDL_NumJoysticks()):
            if sdl2.SDL_IsGameController(i):
                self.standardController = sdl2.SDL_GameControllerOpen(i)
                gamepad = sdl2.SDL_GameControllerGetJoystick(self.standardController)
                self.activeDevice = sdl2.SDL_JoystickInstanceID(gamepad)
                name = sdl2.SDL_GameControllerName(self.standardController).decode("utf-8", errors = "ignore")
                self.statusLabel.configure(text = f"Connected (Standard): {name}")
                return
            else:
                self.genericController = sdl2.SDL_JoystickOpen(i)
                self.activeDevice = sdl2.SDL_JoystickInstanceID(self.genericController)
                name = sdl2.SDL_JoystickName(self.genericController).decode("utf-8", errors = "ignore")
                self.statusLabel.configure(text = f"Connected (Generic): {name}")
                return

        self.statusLabel.configure(text = "No Controller Detected")

    def closeActive(self): 
        if self.standardController:
            sdl2.SDL_GameControllerClose(self.standardController)
            self.standardController = None
        if self.genericController:
            sdl2.SDL_JoystickClose(self.genericController)
            self.genericController = None
        self.activeDevice = None
        self.prevButtons.clear()      
        
    def updateLoop(self): # Input polling loop
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_JOYDEVICEADDED and self.activeDevice is None:
                self.connectController()
            elif event.type == sdl2.SDL_JOYDEVICEREMOVED and event.jdevice.which == self.activeDevice:
                self.connectController()

        if self.standardController:

            # grab normalized analog axis positions
            leftX = sdl2.SDL_GameControllerGetAxis(self.standardController, sdl2.SDL_CONTROLLER_AXIS_LEFTX) / 32767.0
            leftY = sdl2.SDL_GameControllerGetAxis(self.standardController, sdl2.SDL_CONTROLLER_AXIS_LEFTY) / 32767.0
            leftTrigger = sdl2.SDL_GameControllerGetAxis(self.standardController, sdl2.SDL_CONTROLLER_AXIS_TRIGGERLEFT) / 32767.0
            rightTrigger = sdl2.SDL_GameControllerGetAxis(self.standardController, sdl2.SDL_CONTROLLER_AXIS_TRIGGERRIGHT) / 32767.0

            self.updateStickImage(leftX, leftY)

            for button in range(sdl2.SDL_CONTROLLER_BUTTON_MAX):
                isPressed = bool(sdl2.SDL_GameControllerGetButton(self.standardController, button))
                buttonName = self.n64MapDefault.get(sdl2.SDL_GameControllerGetStringForButton(button).decode("utf-8").upper())
                self.updateButtonImage(buttonName, isPressed)
            
            # This block handles N64 controllers specifically, as the Z trigger reads as axis 4, rather than a button. This code reads the axis, and adds the button to the button dict.
            # some usb adapters poll at lower rates, so a held button, especially one that reads as an analog axis, will dip low for a frame when held. I updated this block to account for that so the button doesnt refire every frame unless i want it to. 
            joy = sdl2.SDL_GameControllerGetJoystick(self.standardController)
            if sdl2.SDL_JoystickNumAxes(joy) > 4:
                axisVal = sdl2.SDL_JoystickGetAxis(joy, 4)

                if axisVal > 16000:
                    self.zLow = 0
                    zPressed = True
                elif axisVal < 8000:
                    self.zLow = getattr(self, "zLow", 0) + 1
                    zPressed = self.prevButtons.get("Z", False) if self.zLow < 2 else False
                else:
                    zPressed = self.prevButtons.get("Z", False)

                buttonName = self.n64MapDefault.get("Z", "Z")
                self.updateButtonImage(buttonName, zPressed)

        elif self.genericController:
            numButtons = sdl2.SDL_JoystickNumButtons(self.genericController)

            if sdl2.SDL_JoystickNumAxes(self.genericController) >= 2:
                leftX = sdl2.SDL_JoystickGetAxis(self.genericController, 0) /32767.0
                leftY = sdl2.SDL_JoystickGetAxis(self.genericController, 1) / 32767.0

            for button in range(numButtons):
                isPressed = bool(sdl2.SDL_GameControllerGetButton(self.standardController, button))
                buttonName = self.n64MapDefault.get(sdl2.SDL_GameControllerGetStringForButton(button).decode("utf-8").upper())
                self.updateButtonImage(buttonName, isPressed)

            joy = sdl2.SDL_GameControllerGetJoystick(self.standardController)
            if sdl2.SDL_JoystickNumAxes(joy) > 4:
                axisVal = sdl2.SDL_JoystickGetAxis(joy, 4)
            
                if axisVal > 16000:
                    self.zLow = 0
                    zPressed = True
                elif axisVal < 8000:
                    self.zLow = getattr(self, "zLow", 0) + 1
                    zPressed = self.prevButtons.get("Z", False) if self.zLow < 2 else False
                else:
                    zPressed = self.prevButtons.get("Z", False)
            
                buttonName = self.n64MapDefault.get("Z", "Z")
                self.updateButtonImage(buttonName, zPressed)
        
        # waits for 16 ms before calling the loop again. results in approx. 60 fps update time
        self.after(16, self.updateLoop)


app = InputDisplay()
app.mainloop()




