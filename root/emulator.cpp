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
#include <fstream>

class MacroMag32Core {
private:
    const size_t RAM_SIZE = 65536;
    std::vector<uint8_t> ram;
    std::vector<uint32_t> R;
    uint32_t PC;
    int watchdog_counter;
    bool is_running;
    bool zero_flag;

public:
    MacroMag32Core() : ram(RAM_SIZE, 0), R(15, 0), PC(0x0000), watchdog_counter(100), is_running(true), zero_flag(false) {
        std::cout << "[MacroMag-32] Inicjalizacja fizycznej architektury logicznej...\n";
    }

    bool get_is_running() const {
        return is_running;
    }

    /** Zrzuca pełną zawartość pamięci RAM do pliku binarnego (Core Dump) */
    void dump_ram_to_file(const std::string& dump_filename) {
        std::ofstream dump_file(dump_filename, std::ios::binary);
        if (!dump_file.is_open()) {
            std::cerr << "[ERROR] Nie można zapisać zrzutu pamięci RAM do " << dump_filename << "\n";
            return;
        }

        // Zapis całego bloku pamięci RAM za jednym zamachem
        dump_file.write(reinterpret_cast<const char*>(ram.data()), ram.size());
        dump_file.close();
        std::cout << "[MacroMag-32] Zrzut pamięci (Core Dump) zapisany pomyślnie w: " << dump_filename << "\n";
    }

    bool load_binary_file(uint32_t address, const std::string& filename) {
        std::ifstream file(filename, std::ios::binary);
        if (!file.is_open()) {
            std::cerr << "[CRITICAL] Błąd sprzętowy: Nie można otworzyć pliku " << filename << "\n";
            return false;
        }

        std::cout << "[MacroMag-32] Ładowanie pliku: " << filename << "\n";
        char byte;
        uint32_t current_address = address;

        while (file.get(byte)) {
            if (current_address < RAM_SIZE) {
                ram[current_address] = static_cast<uint8_t>(byte);
                current_address++;
            } else {
                std::cout << "[WARNING] Przepełnienie bufora pamięci RAM! Obcięto plik.\n";
                break;
            }
        }
        std::cout << "[MacroMag-32] Załadowano " << (current_address - address) << " bajtów do RAM.\n";
        file.close();
        return true;
    }

    void run_cycle() {
        if (!is_running) return;

        if (PC + 3 >= RAM_SIZE) {
            std::cout << "[CRITICAL] Zawał Serca Taktowania: Przepełnienie licznika PC!\n";
            is_running = false;
            return;
        }

        uint8_t b0 = ram[PC];
        uint8_t b1 = ram[PC + 1];
        uint8_t b2 = ram[PC + 2];
        uint8_t b3 = ram[PC + 3];

        uint32_t opcode = (static_cast<uint32_t>(b0) << 24) |
                          (static_cast<uint32_t>(b1) << 16) |
                          (static_cast<uint32_t>(b2) << 8)  |
                          b3;
        PC += 4;

        uint8_t instruction_type = (opcode >> 24) & 0xFF;

        if (instruction_type == 0x01) { // MOV
            uint8_t reg_idx = (opcode >> 16) & 0xFF;
            uint16_t value = opcode & 0xFFFF;
            if (reg_idx < 15) {
                R[reg_idx] = value;
                std::cout << "[EXECUTE] MOV: Wpisano wartość " << value << " do Rejestru R" << static_cast<int>(reg_idx) << "\n";
            }
        }
        else if (instruction_type == 0x02) { // ADD
            uint8_t reg_dest = (opcode >> 16) & 0xFF;
            uint8_t reg_src = (opcode >> 8) & 0xFF;
            if (reg_dest < 15 && reg_src < 15) {
                R[reg_dest] += R[reg_src];
                std::cout << "[EXECUTE] ADD: Dodano R" << static_cast<int>(reg_src) << " do R" << static_cast<int>(reg_dest) << ". Nowe R" << static_cast<int>(reg_dest) << " = " << R[reg_dest] << "\n";
            }
        }
        else if (instruction_type == 0xAA) { // BIOS
            launch_hidden_bios();
        }
        else if (instruction_type == 0xFF) { // HALT
            std::cout << "[EXECUTE] HALT: Otrzymano rozkaz zatrzymania układu.\n";
            is_running = false;
        }

        watchdog_counter--;
        if (watchdog_counter <= 0) {
            std::cout << "[CRITICAL] WATCHDOG TIMEOUT: Awaryjne wyłączenie jednostki!\n";
            is_running = false;
        }
    }

    void launch_hidden_bios() {
        std::cout << "\n==================================================\n";
        std::cout << "     MACROMAG-32 INDUSTRIAL BIOS v0.1 (OFFLINE)     \n";
        std::cout << "==================================================\n";
        std::cout << " STAN REJESTRÓW: [";
        for (int i = 0; i < 4; ++i) {
            std::cout << "R" << i << ":" << R[i] << (i < 3 ? ", " : "");
        }
        std::cout << "]\n";
        std::cout << " LICZNIK PROGRAMU (PC): 0x" << std::hex << std::uppercase << PC << std::dec << "\n";
        std::cout << " STATUS STRAŻNIKA (WATCHDOG): " << watchdog_counter << "\n";
        std::cout << "==================================================\n";
        std::cout << "Naciśnij [ENTER], aby opuścić strefę bezpieczną BIOS...";
        std::string dummy;
        std::getline(std::cin, dummy);
    }
};

int main(int argc, char* argv[]) {
    MacroMag32Core cpu;
    std::string firmware_path = "program.bin";

    if (argc > 1) {
        firmware_path = argv[1];
    }

    if (!cpu.load_binary_file(0x0000, firmware_path)) {
        return 1;
    }

    std::cout << "[MacroMag-32] Start głównego zegara.\n\n";
    
    while (cpu.get_is_running()) {
        cpu.run_cycle();
    }

    // AUTOMATYCZNY ZRZUT PAMIĘCI RAM PO ZATRZYMANIU PROCESORA
    std::cout << "\n[MacroMag-32] Zamykanie jądra systemowego...\n";
    cpu.dump_ram_to_file("core_dump.bin");

    return 0;
}
