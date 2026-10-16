# ==============================================================================
#  PROJECT: MacroMag-32 (The Black Box Computer Emulator)
#  CORE FILE: emulator.py
#  LICENSE: GNU General Public License v3 (GPL-3.0)
#  FILOZOFIA: 100% Offline-First, Determinizm Czasu Rzeczywistego, Zero Śmieci
# ==============================================================================

import os
import sys

class MacroMag32Core:
    def __init__(self):
        print("[MacroMag-32] Inicjalizacja fizycznej architektury logicznej...")
        
        # 1. PRZESTRZEŃ PAMIĘCI RAM (32-bitowe adresowanie)
        # Tworzymy wirtualny blok pamięci o rozmiarze 64 KB na pierwszy testowy rozruch.
        # W architekturze 32-bitowej możemy rozbudować to do 4 GB (4 * 1024 * 1024 * 1024 bajtów).
        self.RAM_SIZE = 65536  
        self.ram = [0] * self.RAM_SIZE
        
        # 2. REJESTRY PROCESORA (32-bitowe komórki ultraszybkiej pamięci czipu)
        # R0 do R14 - rejestry ogólnego przeznaczenia (trzymają 32-bitowe liczby całkowite)
        self.R = [0] * 15
        
        # R15 / PC (Program Counter) - Licznik Programu. Wskazuje adres następnej instrukcji.
        self.PC = 0x0000
        
        # 3. SPRZĘTOWY WATCHDOG (Strażnik Systemu)
        # Jeśli ta wartość spadnie do zera bez zresetowania przez system - następuje twardy restart.
        self.watchdog_counter = 100
        
        # Status procesora (Flagi stanu)
        self.is_running = True
        self.zero_flag = False

    def load_functional_operation(self, address, bytecode):
        """Wstrzykuje surowy kod maszynowy (operację) bezpośrednio do pamięci RAM."""
        for i, byte in enumerate(bytecode):
            if address + i < self.RAM_SIZE:
                self.ram[address + i] = byte

    def run_cycle(self):
        """Pojedyncze tyknięcie zegara (Taktowanie). Cykl: Pobierz -> Rozszyfruj -> Wykonaj"""
        if not self.is_running:
            return

        # --- 1. FETCH (Pobranie instrukcji z RAM) ---
        if self.PC >= self.RAM_SIZE:
            print("[CRITICAL] Zawał Serca Taktowania: Przepełnienie licznika PC!")
            self.is_running = False
            return

        # Nasze instrukcje są 4-bajtowe (32-bitowe opcody)
        b0 = self.ram[self.PC]
        b1 = self.ram[self.PC + 1]
        b2 = self.ram[self.PC + 2]
        b3 = self.ram[self.PC + 3]
        
        opcode = (b0 << 24) | (b1 << 16) | (b2 << 8) | b3
        self.PC += 4

        # --- 2. DECODE & EXECUTE (Krzemowy labirynt dekodera rozkazów) ---
        # Wyciągamy pierwszy bajt (Instruction ID) - on decyduje, która bramka się otwiera
        instruction_type = (opcode >> 24) & 0xFF

        # [OPERACJA FUNKCJONALNA 0x01]: Wpisz wartość do rejestru (MOV)
        if instruction_type == 0x01:
            reg_idx = (opcode >> 16) & 0xFF
            value = opcode & 0xFFFF
            self.R[reg_idx] = value
            print(f"[EXECUTE] MOV: Wpisano wartość {value} do Rejestru R{reg_idx}")

        # [OPERACJA FUNKCJONALNA 0x02]: Dodaj wartości rejestrów (ADD)
        elif instruction_type == 0x02:
            reg_dest = (opcode >> 16) & 0xFF
            reg_src = (opcode >> 8) & 0xFF
            self.R[reg_dest] += self.R[reg_src]
            print(f"[EXECUTE] ADD: Dodano R{reg_src} do R{reg_dest}. Nowa wartość R{reg_dest} = {self.R[reg_dest]}")

        # [OPERACJA FUNKCJONALNA 0xAA]: Wywołaj Ukryty BIOS Poziomu 0 (Hardware Service Screen)
        elif instruction_type == 0xAA:
            self.launch_hidden_bios()

        # [OPERACJA FUNKCJONALNA 0xFF]: Twarde zatrzymanie procesora (HALT)
        elif instruction_type == 0xFF:
            print("[EXECUTE] HALT: Otrzymano rozkaz zatrzymania układu.")
            self.is_running = False

        # --- 3. KONTROLA STRAŻNIKA (Watchdog) ---
        self.watchdog_counter -= 1
        if self.watchdog_counter <= 0:
            print("[CRITICAL] WATCHDOG TIMEOUT: System zamarzł. Fizyczny restart układu!")
            self.is_running = False

    def launch_hidden_bios(self):
        """Fizyczny, tekstowy BIOS Poziomu 0 wywoływany instrukcją maszynową"""
        print("\n" + "="*50)
        print("     MACROMAG-32 INDUSTRIAL BIOS v0.1 (OFFLINE)     ")
        print("="*50)
        print(f" STAN REJESTRÓW: { [f'R{i}:{val}' for i, val in enumerate(self.R[:4])] }")
        print(f" LICZNIK PROGRAMU (PC): {hex(self.PC)}")
        print(f" STATUS STRAŻNIKA (WATCHDOG): {self.watchdog_counter}")
        print("="*50)
        input("Naciśnij [ENTER], aby opuścić strefę bezpieczną BIOS...")
        print("Powrót do wykonywania wątku głównego jądra.\n")

# ==============================================================================
# ROZRUCH TESTOWY (URUCHOMIENIE EMULATORA)
# ==============================================================================
if __name__ == "__main__":
    cpu = MacroMag32Core()

    # Tworzymy testowy program (Ciąg bajtów - nasz autorski kod maszynowy / BIOS):
    # Instrukcja 1: MOV R0, 500  (Bajt 0x01, Rejestr 0x00, Wartość 0x01F4) -> 0x010001F4
    # Instrukcja 2: MOV R1, 100  (Bajt 0x01, Rejestr 0x01, Wartość 0x0064) -> 0x01010064
    # Instrukcja 3: ADD R0, R1   (Bajt 0x02, Rejestr docelowy 0x00, Rejestr źródłowy 0x01) -> 0x02000100
    # Instrukcja 4: Wywołaj BIOS (Bajt 0xAA) -> 0xAA000000
    # Instrukcja 5: HALT         (Bajt 0xFF) -> 0xFF000000

    test_program = [
        0x01, 0x00, 0x01, 0xF4,
        0x01, 0x01, 0x00, 0x64,
        0x02, 0x00, 0x01, 0x00,
        0xAA, 0x00, 0x00, 0x00,
        0xFF, 0x00, 0x00, 0x00
    ]

    # Wgrywamy program do pamięci RAM od adresu 0x0000
    cpu.load_functional_operation(0x0000, test_program)

    # Uruchamiamy taktowanie zegara
    print("[MacroMag-32] Włączenie zasilania. Start głównego zegara.\n")
    while cpu.is_running:
        cpu.run_cycle()
