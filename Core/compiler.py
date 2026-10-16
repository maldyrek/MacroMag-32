# ==============================================================================
#  PROJECT: MacroMag-32 (The Black Box Computer Compiler)
#  CORE FILE: compiler.py
#  LICENSE: GNU General Public License v3 (GPL-3.0)
#  FILOZOFIA: 100% Offline-First, Szybka translacja na bytecode binarny
# ==============================================================================

import sys

def parse_register(reg_str):
    """Zamienia ciąg 'R0'..'R14' na wartość numeryczną."""
    reg_str = reg_str.strip().upper().replace(",", "")
    if not reg_str.startswith("R"):
        raise ValueError(f"Nieprawidłowy rejestr: {reg_str}")
    idx = int(reg_str[1:])
    if idx < 0 or idx > 14:
        raise ValueError(f"Rejestr poza zakresem R0-R14: {reg_str}")
    return idx

def compile_asm(source_file, output_file):
    print(f"[ASSEMBLER] Rozpoczynam kompilację pliku: {source_file}")
    bytecode = bytearray()

    try:
        with open(source_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] Nie znaleziono pliku źródłowego: {source_file}")
        return

    for line_num, line in enumerate(lines, 1):
        # Usuwanie komentarzy i białych znaków
        line = line.split(";")[0].split("#")[0].strip()
        if not line:
            continue  # Pusta linia lub sam komentarz

        parts = line.split()
        instruction = parts[0].upper()

        try:
            if instruction == "MOV":
                # Format: MOV R0, 500
                reg_idx = parse_register(parts[1])
                val = int(parts[2].replace(",", ""))
                if val < 0 or val > 0xFFFF:
                    raise ValueError(f"Wartość MOV poza zakresem 16-bitowym (0-65535): {val}")
                
                # Budowanie 32-bitowej instrukcji: [0x01] [REG] [VAL_HIGH] [VAL_LOW]
                bytecode.append(0x01)
                bytecode.append(reg_idx)
                bytecode.append((val >> 8) & 0xFF)
                bytecode.append(val & 0xFF)

            elif instruction == "ADD":
                # Format: ADD R0, R1
                reg_dest = parse_register(parts[1])
                reg_src = parse_register(parts[2])
                
                # Budowanie 32-bitowej instrukcji: [0x02] [DEST] [SRC] [0x00]
                bytecode.append(0x02)
                bytecode.append(reg_dest)
                bytecode.append(reg_src)
                bytecode.append(0x00)

            elif instruction == "BIOS":
                # Format: BIOS
                bytecode.extend([0xAA, 0x00, 0x00, 0x00])

            elif instruction == "HALT":
                # Format: HALT
                bytecode.extend([0xFF, 0x00, 0x00, 0x00])

            else:
                raise ValueError(f"Nieznana instrukcja: {instruction}")

        except Exception as e:
            print(f"[COMPILE ERROR] Linia {line_num}: {e}")
            return

    # Zapis surowego pliku binarnego
    with open(output_file, "wb") as f:
        f.write(bytecode)
    
    print(f"[ASSEMBLER] Sukces! Wygenerowano plik: {output_file} ({len(bytecode)} bajtów).")

if __name__ == "__main__":
    # Przykład użycia: python compiler.py program.asm program.bin
    src = sys.argv[1] if len(sys.argv) > 1 else "program.asm"
    out = sys.argv[2] if len(sys.argv) > 2 else "program.bin"
    compile_asm(src, out)
