# macromag_os.py - Główny rdzeń i powłoka (Bash) systemu MacroMag-32
import os
import sys

# Tutaj w przyszłości zaimportujesz logikę ze swoich plików:
# from compiler import compile_asm
# from prototype import VirtualCPU

VERSION = "1.0.0-Alpha (Offline-First)"

class MacroMagBash:
    def __init__(self):
        self.running = True
        self.current_directory = "/"
        # Symulacja wirtualnych modułów sprzętowych w pamięci
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

        # 1. Komendy powłoki (Bash standard)
        if command == "help":
            print("\n--- MACROMAG-OS COMMANDS ---")
            print("  help              - Shows this documentation")
            print("  ver               - Display system and license info")
            print("  lshw              - List connected magnetic hardware modules")
            print("  compile [file]    - Call compiler.py pipeline to assembly")
            print("  run [bin]         - Execute Emulator.bin via prototype.py core")
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

        # 2. Emulacja Hardware i Integracja Plików
        elif command == "lshw":
            print("\n--- CONNECTED MAGNETIC HARDWARE ---")
            for slot, module in self.connected_modules.items():
                print(f"  [Slot: {slot}] --> Configured as: {module}")
            print("")

        elif command == "attach":
            if not args:
                print("Error: Specify module type (e.g., attach GPU, attach CRYPTO)")
            else:
                mod_type = args[0].upper()
                self.connected_modules[mod_type] = f"Generic Magnetic {mod_type} Block (Simulated)"
                print(f"⚡ HOT-PLUG SUCCESS: Module [{mod_type}] snapped via neodymium magnets!")

        elif command == "compile":
            if not args:
                print("Error: Please specify an .asm file. Example: compile program.asm")
            else:
                print(f"Calling internal compiler.py pipeline for target: {args[0]}...")
                # Tutaj wywołujesz funkcję ze swojego compiler.py
                print("Success: Generated Emulator.bin (32-bit execution bytecode).")

        elif command == "run":
            print("Initializing execution thread via prototype.py...")
            print("Status: Core executed deterministically in 12 clock cycles. Halt reached.")

        else:
            print(f"macromag-bash: command not found: {command}. (Remember: No internet to fetch packages!)")

    def start(self):
        self.show_welcome_message()
        while self.running:
            try:
                # Wygląd znaku zachęty w stylu basha
                prompt = f"maldyrek@macromag32:{self.current_directory}$ "
                user_input = input(prompt)
                self.execute_command(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\nUse 'exit' to shutdown system safely.")

if __name__ == "__main__":
    os_shell = MacroMagBash()
    os_shell.start()
