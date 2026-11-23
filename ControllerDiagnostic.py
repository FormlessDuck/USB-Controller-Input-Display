import ctypes
import time
import sdl2

sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
joy = sdl2.SDL_JoystickOpen(0)

print(f"Device: {sdl2.SDL_JoystickName(joy).decode()}")
print(f"GUID: {sdl2.SDL_JoystickGetGUIDString(sdl2.SDL_JoystickGetGUID(joy), ctypes.create_string_buffer(33), 33)}")
print(f"Buttons: {sdl2.SDL_JoystickNumButtons(joy)} | Axes: {sdl2.SDL_JoystickNumAxes(joy)} | Hats: {sdl2.SDL_JoystickNumHats(joy)}")
print("Press Z now (Ctrl+C to stop)...")

try:
    while True:
        sdl2.SDL_JoystickUpdate()
        
        # Check all raw buttons
        btns = [i for i in range(sdl2.SDL_JoystickNumButtons(joy)) if sdl2.SDL_JoystickGetButton(joy, i)]
        
        # Check all raw axes (ignore near-zero center resting noise)
        axes = {
            i: sdl2.SDL_JoystickGetAxis(joy, i)
            for i in range(sdl2.SDL_JoystickNumAxes(joy))
            if abs(sdl2.SDL_JoystickGetAxis(joy, i)) > 8000
        }
        
        # Check all hats (D-pad / POV)
        hats = {
            i: sdl2.SDL_JoystickGetHat(joy, i)
            for i in range(sdl2.SDL_JoystickNumHats(joy))
            if sdl2.SDL_JoystickGetHat(joy, i) != 0
        }

        if btns or axes or hats:
            print(f"Buttons: {btns} | Axes: {axes} | Hats: {hats}")
        time.sleep(0.05)
except KeyboardInterrupt:
    sdl2.SDL_Quit()
