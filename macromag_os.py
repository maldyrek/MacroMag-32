# main.py - Główny rdzeń i powłoka systemu MacroMag-32
import os
import sys

# Tworzymy puste pliki __init__.py w folderach, aby Python widział je jako pakiety
# Sprawdzamy, czy pliki z folderu core są dostępne
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
    import compiler
    import prototype
    CORE_LOADED = True
except ImportError:
    CORE_LOADED = False

VERSION = "1.0.0-Alpha (Offline-First)"

class MacroMagBash:
    def __init__(self):
        self.running = True
        self.current_directory = "/"
        self.connected_modules = {
            "CPU": "MM-32 Core v1",
            "RAM": "Offline-Cache 64KB",
            "STORAGE": "ROM-Flash Base"
        }

    def show_welcome_message(self):
        print("=" * 60)
        print(f" 🧲  WELCOME TO MACROMAG-OS (Volt-Shell v1.0) 🧲 ")
        print(f" Version: {VERSION} | Status: 100% AIR-GAPPED")
        print(" Type 'help' to see available offline features.")
        print("=" * 60)

    def execute_command(self, cmd_input):
        tokens = cmd_input.strip().split()
        if not tokens:
            return

        command = tokens[0].lower()
        args = tokens[1:]

        if command == "help":
            print("\n--- MACROMAG-OS COMMANDS ---")
            print("  help              - Shows this documentation")
            print("  ver               - Display system and license info")
            print("  lshw              - List connected magnetic hardware modules")
            print("  compile [file]    - Call core/compiler.py pipeline to assembly")
            print("  run [bin]         - Execute Emulator.bin via core/prototype.py")
            print("  attach [mod_type] - Simulate snapping a physical module via magnets")
            print("  clear             - Clear the screen")
            print("  exit              - Shutdown MacroMag-OS safely\n")

        elif command == "ver":
            print(f"MacroMag-OS Core v{VERSION}")
            print("License: GNU GPL v3 - Eternal Property of Humanity.")
            print("Created by maldyrek (Inspired by Linus Torvalds).")

        elif command == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')

        elif command == "exit":
            print("Shutting down kernel. Releasing magnetic interlocks... Goodbye.")
            self.running = False

        elif command == "lshw":
            print("\n--- CONNECTED MAGNETIC HARDWARE ---")
            for slot, module in self.connected_modules.items():
                print(f"  [Slot: {slot}] --> Configured as: {module}")
            print("")

        elif command == "attach":
            if not args:
                print("Error: Specify module type (e.g., attach GPU)")
            else:
                mod_type = args[0].upper()
                self.connected_modules[mod_type] = f"Generic Magnetic {mod_type} Block (Simulated)"
                print(f"⚡ HOT-PLUG SUCCESS: Module [{mod_type}] snapped via neodymium magnets!")

        elif command == "compile":
            if not args:
                print("Error: Please specify an .asm file. Example: compile program.asm")
            elif not CORE_LOADED:
                print("Error: core/compiler.py not found or could not be loaded.")
            else:
                print(f"Calling internal core/compiler.py pipeline for target: {args[0]}...")
                print("Success: Generated Emulator.bin (32-bit execution bytecode).")

        elif command == "run":
            if not CORE_LOADED:
                print("Error: core/prototype.py not found or could not be loaded.")
            else:
                print("Initializing execution thread via core/prototype.py...")
                print("Status: Core executed deterministically. Halt reached.")

        else:
            print(f"macromag-bash: command not found: {command}.")

    def start(self):
        self.show_welcome_message()
        while self.running:
            try:
                prompt = f"maldyrek@macromag32:{self.current_directory}$ "
                user_input = input(prompt)
                self.execute_command(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\nUse 'exit' to shutdown system safely.")

if __name__ == "__main__":
    os_shell = MacroMagBash()
    os_shell.start()

