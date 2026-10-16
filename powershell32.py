import re
import sys

class MacroShellInterpreter:
    def __init__(self):
        # 1. Baza danych 5 Ukrytych BIOS-ów (Phantom BIOS Registries)
        self.phantom_bios = {
            "CPU": {
                "version": "v1.2.4-Secure",
                "frequency": "400MHz",
                "core_state": "DETERMINISTIC",
                "efuse_bypass": "ENABLED [Protects against corporate bricking]"
            },
            "RAM": {
                "version": "v0.9.1-Direct",
                "allocation_policy": "STRICT-BOUNDARIES",
                "refresh_rate": "Auto-Optimized",
                "parity_check": "HARDWARE-ENFORCED"
            },
            "DISPLAY": {
                "version": "v2.1.0-ASCII",
                "mode": "PURE-TEXT-MONOSPACE",
                "buffer_address": "0x00FBF000",
                "contrast_lock": "STABLE"
            },
            "STORAGE": {
                "version": "v3.0.2-Mag",
                "filesystem": "M-FS [Offline-Secure]",
                "sector_size": "512-Bytes",
                "hardware_encryption": "ACTIVE [User-Generated Key]"
            },
            "GPS-CHIP": {
                "version": "v1.0.0-Legacy",
                "hardware_bridge": "TOMTOM-NAV3-BYPASS",
                "raw_nmea_feed": "STREAMING-LOCAL-ONLY",
                "telemetry_block": "TOTAL [100% Stealth Mode]"
            }
        }

        # Aktywne maszyny wirtualne w systemie
        self.virtual_machines = {}
        self.is_running = True

    def execute_command(self, user_input):
        cmd = user_input.strip()
        if not cmd or cmd.startswith("//"):
            return

        # --- NOWA KOMENDA 1: Get-Bios (Wyświetlanie rejestrów BIOS) ---
        if cmd.lower().startswith("get-bios"):
            match = re.search(r"-Module\s+(\w+)", cmd, re.IGNORECASE)
            if match:
                mod_name = match.group(1).upper()
                if mod_name in self.phantom_bios:
                    print(f"\n[MacroShell Object: PhantomBIOS-Registry-Dump ({mod_name})]")
                    print("-" * 55)
                    for key, val in self.phantom_bios[mod_name].items():
                        print(f" {key:<20} : {val}")
                    print("-" * 55 + "\n")
                else:
                    print(f"[ERROR] Module '{mod_name}' not found. Available modules: CPU, RAM, DISPLAY, STORAGE, GPS-CHIP")
            else:
                # Jeśli użytkownik wpisze samo Get-Bios, wyświetl listę dostępnych BIOS-ów
                print("\n[MacroShell Object: Registered-Phantom-BIOS-List]")
                print(f"{'Module Node':<15} | {'Firmware Version':<20}")
                print("-" * 38)
                for mod, data in self.phantom_bios.items():
                    print(f"{mod:<15} | {data['version']:<20}")
                print("Use: Get-Bios -Module [Name] to inspect hardware registers.\n")

        # --- NOWA KOMENDA 2: Set-Bios (Zmiana niskopoziomowych parametrów) ---
        elif cmd.lower().startswith("set-bios"):
            # Składnia: Set-Bios -Module CPU -Key core_state -Value COMPATIBILITY
            match = re.search(r"-Module\s+(\w+)\s+-Key\s+(\w+)\s+-Value\s+(.+)", cmd, re.IGNORECASE)
            if match:
                mod_name = match.group(1).upper()
                key_name = match.group(2).lower()
                new_value = match.group(3)

                if mod_name in self.phantom_bios:
                    if key_name in self.phantom_bios[mod_name]:
                        self.phantom_bios[mod_name][key_name] = f"{new_value} [MODIFIED BY USER]"
                        print(f"[SUCCESS] Interconnect Written: {mod_name} -> {key_name} set to '{new_value}'.")
                    else:
                        print(f"[ERROR] Registry key '{key_name}' does not exist in {mod_name} BIOS.")
                else:
                    print(f"[ERROR] Module '{mod_name}' not found.")
            else:
                print("[ERROR] Invalid syntax. Use: Set-Bios -Module CPU -Key core_state -Value COMPATIBILITY")

        # --- KLASYCZNE KOMENDY POWŁOKI MACROSHELL ---
        elif cmd.lower() == "get-vm":
            print("\n[MacroShell Object: VirtualMachineList]")
            if not self.virtual_machines:
                print("No active virtual nodes registered in RAM.")
            else:
                print(f"{'VM Node Name':<20} | {'Memory Allocated':<15} | {'Runtime Status':<10}")
                print("-" * 55)
                for name, config in self.virtual_machines.items():
                    print(f"{name:<20} | {config['memory']:<15} | {config['status']:<10}")
            print("")

        elif cmd.lower().startswith("new-vm"):
            match = re.search(r"-Name\s+(\w+)\s+-Mem\s+(\w+)", cmd, re.IGNORECASE)
            if match:
                vm_name = match.group(1)
                vm_mem = match.group(2)
                self.virtual_machines[vm_name] = {"memory": vm_mem, "status": "STOPPED"}
                print(f"[SUCCESS] Object created: VM '{vm_name}' registered with {vm_mem} memory boundary.")
            else:
                print("[ERROR] Invalid syntax. Use: New-VM -Name [Alpha] -Mem [128KB]")

        elif cmd.lower().startswith("start-vm"):
            match = re.search(r"-Name\s+(\w+)", cmd, re.IGNORECASE)
            if match and match.group(1) in self.virtual_machines:
                vm_name = match.group(1)
                self.virtual_machines[vm_name]["status"] = "RUNNING"
                print(f"[SUCCESS] Hypervisor intercepted instruction. VM '{vm_name}' is now ACTIVE in text container.")
            else:
                print("[ERROR] VM not found or bad syntax. Use: Start-VM -Name [Alpha]")

        elif cmd.lower() == "exit":
            print("\nCollapsing MacroShell runtime safely. System standby. Manifest secured.")
            self.is_running = False
        else:
            print(f"[ERROR] Command '{cmd}' not recognized in MacroMag architecture registries.")

    def start_repl(self):
        print("==========================================================")
        print(" MACROMAG-32 ARCHITECTURE - MICRO-LOGIC TERMINAL v0.3.0   ")
        print(" 100% Offline Environment | 5 Phantom BIOS Nodes Active   ")
        print("==========================================================")
        print("Hardware-First Prompts: Get-Bios, Get-Bios -Module CPU, Set-Bios, Get-VM\n")
        
        while self.is_running:
            try:
                user_input = input("M-Core:\\> ")
                self.execute_command(user_input)
            except (KeyboardInterrupt, EOFError):
                print("\nForced interrupt. Exiting safely.")
                break

if __name__ == "__main__":
    shell = MacroShellInterpreter()
    shell.start_repl()
