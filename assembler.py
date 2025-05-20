import struct

# Instruction encoding map
ISA = {
    'ADD':  (0b000, 0), 'ADDi': (0b000, 1),
    'NAND': (0b001, 0), 'NANDi':(0b001, 1),
    'SRL':  (0b010, 0), 'SRLi': (0b010, 1),
    'LT':   (0b011, 0), 'LTi':  (0b011, 1),
    'CP':   (0b100, 0), 'CPi':  (0b100, 1),
    'CPI':  (0b101, 0), 'CPIi': (0b101, 1),
    'BZJ':  (0b110, 0), 'BZJi': (0b110, 1),
    'MUL':  (0b111, 0), 'MULi': (0b111, 1),
}

def assemble_instruction(mnemonic, a, b):
    if mnemonic not in ISA:
        raise ValueError(f"Invalid instruction: {mnemonic}")
    opcode, im = ISA[mnemonic]
    if not (0 <= a < (1 << 14)) or not (0 <= b < (1 << 14)):
        raise ValueError(f"A or B out of range (must be 14-bit): A={a}, B={b}")
    instruction = (opcode << 29) | (im << 28) | (a << 14) | b
    return instruction

def assemble_file(input_path, output_path):
    with open(input_path, 'r') as asm_file, open(output_path, 'wb') as bin_file:
        for line_num, line in enumerate(asm_file, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments
            try:
                parts = line.split()
                if len(parts) != 3:
                    raise ValueError("Expected format: INSTR A B")
                mnemonic, a_str, b_str = parts
                a = int(a_str)
                b = int(b_str)
                instr = assemble_instruction(mnemonic, a, b)
                bin_file.write(struct.pack('<I', instr))  # little-endian
            except Exception as e:
                print(f"Error on line {line_num}: {line}")
                print(f"  {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 vscpu_assembler.py input.asm output.bin")
        sys.exit(1)
    assemble_file(sys.argv[1], sys.argv[2])

