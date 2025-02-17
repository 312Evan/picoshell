import gc
from machine import Pin, deepsleep, reset
from utime import sleep, time
import os

led = Pin("LED", Pin.OUT)

start_time = time()
active_tasks = []

def uptime():
    return time() - start_time

def system_info():
    print("PicoShell v0.2 - A lightweight PicoShell")
    print(f"Uptime: {uptime()} seconds")
    print("""______ _           _____ _          _ _ 
| ___ (_)         /  ___| |        | | |
| |_/ /_  ___ ___ \ `--.| |__   ___| | |
|  __/| |/ __/ _ \ `--. \ '_ \ / _ \ | |
| |   | | (_| (_) /\__/ / | | |  __/ | |
\_|   |_|\___\___/\____/|_| |_|\___|_|_|
""")
    print("Available Commands: math, led, file, sysinfo, taskman, reboot, shutdown, python")

def task_manager():
    print("\n--- Task Manager ---")
    print(f"Uptime: {uptime()} seconds")
    print(f"Memory Free: {gc.mem_free()} bytes")
    print("Active Tasks:", active_tasks if active_tasks else "None")

def python_mode():
    print("Python Mode Commands: write <file>, run <file>, list")
    command = input("Enter python command: ").strip().split()

    if len(command) == 0:
        print("Invalid command.")
        return

    action = command[0]
    if action == "list":
        print("Python Files:", [f for f in os.listdir() if f.endswith(".py")])

    elif action == "write" and len(command) > 1:
        filename = command[1]
        if not filename.endswith(".py"):
            filename += ".py"
        print(f"Writing to {filename}. Type 'END' to finish.")
        active_tasks.append(f"Writing {filename}")

        with open(filename, "w") as f:
            while True:
                line = input("> ")
                if line.strip().upper() == "END":
                    break
                f.write(line + "\n")

        print(f"Saved {filename}.")
        active_tasks.remove(f"Writing {filename}")

    elif action == "run" and len(command) > 1:
        filename = command[1]
        if not filename.endswith(".py"):
            filename += ".py"

        if filename in os.listdir():
            print(f"Executing {filename}...")
            active_tasks.append(f"Running {filename}")
            try:
                with open(filename) as f:
                    exec(f.read(), globals())
            except Exception as e:
                print(f"Execution Error: {e}")
            active_tasks.remove(f"Running {filename}")
        else:
            print("Error: File not found.")

    else:
        print("Invalid python command.")

import math
def math_operations():
    active_tasks.append("Math Operation")
    operation = input("Choose operation (add, sub, mul, div, pow, mod, sqrt, fact, sin, cos, tan): ").strip().lower()
    
    try:
        if operation in ["add", "sub", "mul", "div", "pow", "mod"]:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if operation == "add":
                print("Result:", num1 + num2)
            elif operation == "sub":
                print("Result:", num1 - num2)
            elif operation == "mul":
                print("Result:", num1 * num2)
            elif operation == "div":
                print("Result:", num1 / num2 if num2 != 0 else "Error: Division by zero!")
            elif operation == "pow":
                print("Result:", num1 ** num2)
            elif operation == "mod":
                print("Result:", num1 % num2)

        elif operation == "sqrt":
            num = float(input("Enter a number: "))
            print("Result:", math.sqrt(num) if num >= 0 else "Error: Cannot compute square root of a negative number!")

        elif operation == "fact":
            num = int(input("Enter an integer: "))
            print("Result:", math.factorial(num) if num >= 0 else "Error: Factorial is only for non-negative integers!")

        elif operation in ["sin", "cos", "tan"]:
            angle = float(input("Enter angle in degrees: "))
            rad = math.radians(angle)
            if operation == "sin":
                print("Result:", math.sin(rad))
            elif operation == "cos":
                print("Result:", math.cos(rad))
            elif operation == "tan":
                print("Result:", math.tan(rad))

        else:
            print("Invalid operation!")

    except ValueError:
        print("Error: Invalid number input!")

    active_tasks.remove("Math Operation")

def led_control():
    active_tasks.append("LED Control")
    action = input("LED on/off: ").strip().lower()
    if action == "on":
        led.on()
        print("LED is ON")
    elif action == "off":
        led.off()
        print("LED is OFF")
    else:
        print("Unknown command.")
    active_tasks.remove("LED Control")

def file_manager():
    active_tasks.append("File Manager")
    print("File commands: list, read [file], write [file], delete [file]")
    command = input("Enter file command: ").strip().split()
    if command[0] == "list":
        print("Files:", os.listdir())
    elif command[0] == "read" and len(command) > 1:
        try:
            with open(command[1], "r") as f:
                print(f.read())
        except Exception as e:
            print("Error reading file:", e)
    elif command[0] == "write" and len(command) > 1:
        data = input("Enter file content: ")
        try:
            with open(command[1], "w") as f:
                f.write(data)
            print("File written successfully.")
        except Exception as e:
            print("Error writing file:", e)
    elif command[0] == "delete" and len(command) > 1:
        try:
            os.remove(command[1])
            print(f"File '{command[1]}' deleted successfully.")
        except Exception as e:
            print("Error deleting file:", e)
    else:
        print("Invalid file command.")
    active_tasks.remove("File Manager")

def command_shell():
    while True:
        user_input = input("\nP$> ").strip().lower()
        if user_input == "math":
            math_operations()
        elif user_input == "led":
            led_control()
        elif user_input == "file":
            file_manager()
        elif user_input == "sysinfo":
            system_info()
        elif user_input == "taskman":
            task_manager()
        elif user_input.startswith("python"):
            python_mode()
        elif user_input == "reboot":
            print("Rebooting...")
            sleep(1)
            reset()
        elif user_input == "shutdown":
            print("Shutting down...")
            sleep(0.5)
            deepsleep()
        elif user_input == "exit":
            print("Exiting Pico shell...")
            break
        else:
            print("Unknown command. Type 'sysinfo' for help.")

print("Welcome to Pico Shell!")
system_info()
command_shell()
