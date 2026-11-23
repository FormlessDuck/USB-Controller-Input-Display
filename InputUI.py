import ctypes
import sdl2
import customtkinter as ctk

class InputDisplay(ctk.CTk):

    def __init__(self):
        super().__init__()

        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK | sdl2.SDL_INIT_GAMECONTROLLER)

        self.standardController = None # For use with standard controllers, i.e, XBox, Playstation, Switch
        self.genericController = None #For use with generic gamepads that use raw usb data
        self.activeDevice = None # Id of connected controller

        self.prevButtons = {} # dictionary of previous state of all controller inputs.

        self.statusLabel = ctk.CTkLabel(self, text = "Waiting for input...")
        self.statusLabel.pack(pady = 20)

        self.buttonLabel = ctk.CTkLabel(self, text = "Press a button...")
        self.buttonLabel.pack(pady = 20)

        self.axisLabel = ctk.CTkLabel(self, text = "Left Stick: (0.00, 0.00)")
        self.axisLabel.pack(pady = 20)



        self.connectController()
        self.updateLoop()

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
            for button in range(sdl2.SDL_CONTROLLER_BUTTON_MAX):
                isPressed = bool(sdl2.SDL_GameControllerGetButton(self.standardController, button))
                if isPressed and not self.prevButtons.get(button, False):
                    buttonName = sdl2.SDL_GameControllerGetStringForButton(button).decode("utf-8").upper()
                    print(f"{buttonName} pressed.")
                    self.buttonLabel.configure(text = f"Last Button: {buttonName}")
                self.prevButtons[button] = isPressed

            # grab normalized analog axis positions
            leftX = sdl2.SDL_GameControllerGetAxis(self.standardController, sdl2.SDL_CONTROLLER_AXIS_LEFTX) / 32767.0
            leftY = sdl2.SDL_GameControllerGetAxis(self.standardController, sdl2.SDL_CONTROLLER_AXIS_LEFTY) / 32767.0
            leftTrigger = sdl2.SDL_GameControllerGetAxis(self.standardController, sdl2.SDL_CONTROLLER_AXIS_TRIGGERLEFT) / 32767.0
            rightTrigger = sdl2.SDL_GameControllerGetAxis(self.standardController, sdl2.SDL_CONTROLLER_AXIS_TRIGGERRIGHT) / 32767.0

            weirdo = sdl2.SDL_GameControllerGetJoystick(self.standardController)
            if sdl2.SDL_JoystickNumAxes(weirdo) > 4:
                zPressed = sdl2.SDL_JoystickGetAxis(weirdo, 4) > 0
                if zPressed and not self.prevButtons.get("Z", False):
                    self.buttonLabel.configure(text = "Last Button: Z")
                self.prevButtons["Z"] = isPressed

            self.axisLabel.configure(text = f"Left Stick: ({leftX: .2f}, {leftY: .2f})")

        elif self.genericController:
            numButtons = sdl2.SDL_JoystickNumButtons(self.genericController)
            for button in range(numButtons):
                isPressed = bool(sdl2.SDL_JoystickGetButton(self.genericController, button))
                if isPressed and not self.prevButtons.get(button, False):
                    print(f"{button} pressed.")
                    self.buttonLabel.configure(text = f"Last Button: {button}")
                self.prevButtons[button] = isPressed

            if sdl2.SDL_JoystickNumAxes(self.genericController) >= 2:
                leftX = sdl2.SDL_JoystickGetAxis(self.genericController, 0) /32767.0
                leftY = sdl2.SDL_JoystickGetAxis(self.genericController, 1) / 32767.0

                self.axisLabel.configure(text = f"Left Stick: ({leftX: .2f}, {leftY: .2f})")

            weirdo = self.genericController
            if sdl2.SDL_JoystickNumAxes(weirdo) > 4:
                zPressed = sdl2.SDL_JoystickGetAxis(weirdo, 4) > 0
                if zPressed and not self.prevButtons.get("Z", False):
                    self.buttonLabel.configure(text = "Last Button: Z")
                self.prevButtons["Z"] = isPressed
        

        self.after(16, self.updateLoop)

app = InputDisplay()
app.mainloop()




