"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc=0  # Program Counter address of current executing instruction
        self.reg=[0]*7 # General Purpose Registers
        self.reg.append(0xF4) # 256 bit Storage
        self.ram=[0]*255 # This will serve as 256 Bytes of RAM storage
        self.IR=0 # Instruction Register running Instruction
        self.sp = 7 # Stack pointer Pointing at the top of the stack
        """Both Are needed to keep track of where in memory we are, 
            as well as what is being stored"""
        self.MAR=0 # Memory Address Register 
        self.MDR=0 # Memory Data Register
        self.FL=0 # Flags given based on CMP opcode

        # List of all the instructions for passing the ALU Binding CPU functionality to args received in run-time
        self.inst={
            0b10000010:self.LDI,
            0b01000111:self.PRN,
            0b10100000:self.ADD,
            0b10100010:self.MUL,
            0b10100111:self.CMP,
            0b01000101:self.PUSH,
            0b01000110:self.POP,
            0b01010000:self.CALL,
            0b00010001:self.RET,
            0b01010100:self.JMP,
            0b01010110:self.JNE,
            0b01010101:self.JEQ,
            0b10000100:self.ST,
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        while running is True:
            self.IR = self.ram_read(self.pc)
            if self.IR == 0b00000001:
                #HLT
                running=False
            elif self.IR == 0b10000010:
                     #LDI
                self.pc += 3
            elif self.IR == 0b01000111:
                 #PRN
                print(8)
                self.pc += 1
            else:
                print("Invalid Instruction")
                running = False




    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR]=MDR
