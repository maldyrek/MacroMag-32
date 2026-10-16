// ==============================================================================
//  PROJECT: MacroMag-32 (The Black Box Computer Emulator)
//  CORE FILE: emulator.cpp
//  LICENSE: GNU General Public License v3 (GPL-3.0)
//  FILOZOFIA: 100% Offline-First, Determinizm Czasu Rzeczywistego, Zero Śmieci
// ==============================================================================

#include <iostream>
#include <vector>
#include <cstdint>
#include <iomanip>
#include <string>

class MacroMag32Core {
private:
    // 1. PRZESTRZEŃ PAMIĘCI RAM (32-bitowe adresowanie)
    // Blok pamięci o rozmiarze 64 KB na pierwszy testowy rozruch.
    const size_t RAM_SIZE = 65536;
    std::vector<uint8_t> ram;

    // 2. REJESTRY PROCESORA (32-bitowe komórki ultraszybkiej pamięci czipu)
    // R0 do R14 - rejestry ogólnego przeznaczenia (32-bitowe liczby całkowite bez znaku)
    std::vector<uint32_t> R;

    // R15 / PC (Program Counter) - Licznik Programu. Wskazuje adres następnej instrukcji.
    uint32_t PC;

    // 3. SPRZĘTOWY WATCHDOG (Strażnik Systemu)
    int watchdog_counter;

    // Status procesora (Flagi stanu)
    bool is_running;
    bool zero_flag;

public:
    MacroMag32Core() : ram(RAM_SIZE, 0), R(15, 0), PC(0x0000), watchdog_counter(100), is_running(true), zero_flag(false) {
        std::cout << "[MacroMag-32] Inicjalizacja fizycznej architektury logicznej...\n";
    }

    // Sprawdzenie, czy procesor nadal pracuje
    bool get_is_running() const {
        return is_running;
    }

    /** Wstrzykuje surowy kod maszynowy (operację) bezpośrednio do pamięci RAM. */
    void load_functional_operation(uint32_t address, const std::vector<uint8_t>& bytecode) {
        for (size_t i = 0; i < bytecode.size(); ++i) {
            if (address + i < RAM_SIZE) {
                ram[address + i] = bytecode[i];
            }
        }
    }

    /** Pojedyncze tyknięcie zegara (Taktowanie). Cykl: Pobierz -> Rozszyfruj -> Wykonaj */
    void run_cycle() {
        if (!is_running) return;

        // --- 1. FETCH (Pobranie instrukcji z RAM) ---
        // Ponieważ instrukcja zajmuje 4 bajty, sprawdzamy czy PC + 3 nie przekracza pamięci
        if (PC + 3 >= RAM_SIZE) {
            std::cout << "[CRITICAL] Zawał Serca Taktowania: Przepełnienie licznika PC!\n";
            is_running = false;
            return;
        }

        // Nasze instrukcje są 4-bajtowe (32-bitowe opcody)
        uint8_t b0 = ram[PC];
        uint8_t b1 = ram[PC + 1];
        uint8_t b2 = ram[PC + 2];
        uint8_t b3 = ram[PC + 3];

        uint32_t opcode = (static_cast<uint32_t>(b0) << 24) |
                          (static_cast<uint32_t>(b1) << 16) |
                          (static_cast<uint32_t>(b2) << 8)  |
                          b3;
        PC += 4;

        // --- 2. DECODE & EXECUTE (Krzemowy labirynt dekodera rozkazów) ---
        // Wyciągamy pierwszy bajt (Instruction ID) - on decyduje, która bramka się otwiera
        uint8_t instruction_type = (opcode >> 24) & 0xFF;

        // [OPERACJA FUNKCJONALNA 0x01]: Wpisz wartość do rejestru (MOV)
        if (instruction_type == 0x01) {
            uint8_t reg_idx = (opcode >> 16) & 0xFF;
            uint16_t value = opcode & 0xFFFF;
            if (reg_idx < 15) {
                R[reg_idx] = value;
                std::cout << "[EXECUTE] MOV: Wpisano wartość " << value << " do Rejestru R" << static_cast<int>(reg_idx) << "\n";
            }
        }
        // [OPERACJA FUNKCJONALNA 0x02]: Dodaj wartości rejestrów (ADD)
        else if (instruction_type == 0x02) {
            uint8_t reg_dest = (opcode >> 16) & 0xFF;
            uint8_t reg_src = (opcode >> 8) & 0xFF;
            if (reg_dest < 15 && reg_src < 15) {
                R[reg_dest] += R[reg_src];
                std::cout << "[EXECUTE] ADD: Dodano R" << static_cast<int>(reg_src) 
                          << " do R" << static_cast<int>(reg_dest) 
                          << ". Nowa wartość R" << static_cast<int>(reg_dest) << " = " << R[reg_dest] << "\n";
            }
        }
        // [OPERACJA FUNKCJONALNA 0xAA]: Wywołaj Ukryty BIOS Poziomu 0 (Hardware Service Screen)
        else if (instruction_type == 0xAA) {
            launch_hidden_bios();
        }
        // [OPERACJA FUNKCJONALNA 0xFF]: Twarde zatrzymanie procesora (HALT)
        else if (instruction_type == 0xFF) {
            std::cout << "[EXECUTE] HALT: Otrzymano rozkaz zatrzymania układu.\n";
            is_running = false;
        }

        // --- 3. KONTROLA STRAŻNIKA (Watchdog) ---
        watchdog_counter--;
        if (watchdog_counter <= 0) {
            std::cout << "[CRITICAL] WATCHDOG TIMEOUT: System zamarzł. Fizyczny restart układu!\n";
            is_running = false;
        }
    }

    /** Fizyczny, tekstowy BIOS Poziomu 0 wywoływany instrukcją maszynową */
    void launch_hidden_bios() {
        std::cout << "\n==================================================\n";
        std::cout << "     MACROMAG-32 INDUSTRIAL BIOS v0.1 (OFFLINE)     \n";
        std::cout << "==================================================\n";
        
        std::cout << " STAN REJESTRÓW: [";
        for (int i = 0; i < 4; ++i) {
            std::cout << "R" << i << ":" << R[i] << (i < 3 ? ", " : "");
        }
        std::cout << "]\n";

        // Formatowanie wyświetlania adresu PC jako HEX (np. 0x10)
        std::cout << " LICZNIK PROGRAMU (PC): 0x" << std::hex << std::uppercase << PC << std::dec << "\n";
        std::cout << " STATUS STRAŻNIKA (WATCHDOG): " << watchdog_counter << "\n";
        std::cout << "==================================================\n";
        
        std::cout << "Naciśnij [ENTER], aby opuścić strefę bezpieczną BIOS...";
        std::string dummy;
        std::getline(std::cin, dummy); // Czeka na enter
        
        std::cout << "Powrót do wykonywania wątku głównego jądra.\n\n";
    }
};

// ==============================================================================
// ROZRUCH TESTOWY (URUCHOMIENIE EMULATORA)
// ==============================================================================
int main() {
    MacroMag32Core cpu;

    // Tworzymy testowy program (Ciąg bajtów - nasz autorski kod maszynowy / BIOS):
    std::vector<uint8_t> test_program = {
        0x01, 0x00, 0x01, 0xF4, // Instrukcja 1: MOV R0, 500  (0x010001F4)
        0x01, 0x01, 0x00, 0x64, // Instrukcja 2: MOV R1, 100  (0x01010064)
        0x02, 0x00, 0x01, 0x00, // Instrukcja 3: ADD R0, R1   (0x02000100)
        0xAA, 0x00, 0x00, 0x00, // Instrukcja 4: Wywołaj BIOS (0xAA000000)
        0xFF, 0x00, 0x00, 0x00  // Instrukcja 5: HALT         (0xFF000000)
    };

    // Wgrywamy program do pamięci RAM od adresu 0x0000
    cpu.load_functional_operation(0x0000, test_program);

    // Uruchamiamy taktowanie zegara
    std::cout << "[MacroMag-32] Włączenie zasilania. Start głównego zegara.\n\n";
    
    while (cpu.get_is_running()) {
        cpu.run_cycle();
    }

    return 0;
}
