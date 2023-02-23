import keyboard
keyboard.on_press_key("r", lambda _:print("You pressed r"))

while True:
    if keyboard.read_key() == "p":
        print("You pressed p")

    if keyboard.is_pressed("q"):
        print("You pressed q")
        
    if keyboard.read_key() == "w":
        print("You pressed w")