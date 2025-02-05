import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from enum import Enum
import re

class Format(Enum):
    R = "R"
    I = "I"
    J = "J"

class Register:
    def __init__(self, name, number, value=0):
        self.name = name
        self.number = number
        self.value = value

class MIPSInstruction:
    def __init__(self, opcode: str, inst_format: Format, funct: str = None):
        self.opcode = opcode
        self.format = inst_format
        self.funct = funct

    def to_binary(self, rs: int, rt: int, rd: int = 0, shamt: int = 0, immediate: int = 0):
        if self.format == Format.R:
            return f"{self.opcode}{bin(rs)[2:].zfill(5)}{bin(rt)[2:].zfill(5)}{bin(rd)[2:].zfill(5)}{bin(shamt)[2:].zfill(5)}{self.funct}"
        elif self.format == Format.I:
            return f"{self.opcode}{bin(rs)[2:].zfill(5)}{bin(rt)[2:].zfill(5)}{bin(immediate & 0xFFFF)[2:].zfill(16)}"
        else:  # Format.J
            return f"{self.opcode}{bin(immediate)[2:].zfill(26)}"

class MIPSSimulator:
    def __init__(self):
        self.registers = [
            Register("$zero", 0), Register("$at", 1),
            Register("$v0", 2), Register("$v1", 3),
            Register("$a0", 4), Register("$a1", 5),
            Register("$a2", 6), Register("$a3", 7),
            Register("$t0", 8), Register("$t1", 9),
            Register("$t2", 10), Register("$t3", 11),
            Register("$t4", 12), Register("$t5", 13),
            Register("$t6", 14), Register("$t7", 15),
            Register("$s0", 16), Register("$s1", 17),
            Register("$s2", 18), Register("$s3", 19),
            Register("$s4", 20), Register("$s5", 21),
            Register("$s6", 22), Register("$s7", 23),
            Register("$t8", 24), Register("$t9", 25),
            Register("$k0", 26), Register("$k1", 27),
            Register("$gp", 28), Register("$sp", 29),
            Register("$fp", 30), Register("$ra", 31)
        ]
        
        self.instruction_memory = {}  # Address -> (Instruction, Binary)
        self.data_memory = bytearray(1024)  # 1KB data memory
        self.pc = 0
        
        self.instruction_set = {
            "add": MIPSInstruction("000000", Format.R, "100000"),
            "sub": MIPSInstruction("000000", Format.R, "100010"),
            "and": MIPSInstruction("000000", Format.R, "100100"),
            "or":  MIPSInstruction("000000", Format.R, "100101"),
            "slt": MIPSInstruction("000000", Format.R, "101010"),
            "sll": MIPSInstruction("000000", Format.R, "000000"),
            "srl": MIPSInstruction("000000", Format.R, "000010"),
            "jr":  MIPSInstruction("000000", Format.R, "001000"),
            "addi": MIPSInstruction("001000", Format.I),
            "lw":   MIPSInstruction("100011", Format.I),
            "sw":   MIPSInstruction("101011", Format.I),
            "beq":  MIPSInstruction("000100", Format.I),
            "bne":  MIPSInstruction("000101", Format.I),
            "j":    MIPSInstruction("000010", Format.J),
            "jal":  MIPSInstruction("000011", Format.J)
        }

    def get_register_number(self, reg_name: str) -> int:
        for reg in self.registers:
            if reg.name == reg_name:
                return reg.number
        raise ValueError(f"Unknown register: {reg_name}")

    def get_register_by_number(self, number: int) -> Register:
        return self.registers[number]

    def parse_instruction(self, instruction: str) -> tuple:
        parts = instruction.strip().split()
        op = parts[0]
        args = [arg.strip(",") for arg in parts[1:]]
        
        if op not in self.instruction_set:
            raise ValueError(f"Unknown instruction: {op}")
            
        inst = self.instruction_set[op]
        binary = ""
        
        try:
            if inst.format == Format.R:
                if op in ["sll", "srl"]:
                    rd = self.get_register_number(args[0])
                    rt = self.get_register_number(args[1])
                    shamt = int(args[2])
                    binary = inst.to_binary(0, rt, rd, shamt)
                elif op == "jr":
                    rs = self.get_register_number(args[0])
                    binary = inst.to_binary(rs, 0, 0)
                else:
                    rd = self.get_register_number(args[0])
                    rs = self.get_register_number(args[1])
                    rt = self.get_register_number(args[2])
                    binary = inst.to_binary(rs, rt, rd)
                    
            elif inst.format == Format.I:
                if op in ["lw", "sw"]:
                    rt = self.get_register_number(args[0])
                    offset = int(args[1].split("(")[0])
                    rs = self.get_register_number(args[1].split("(")[1].strip(")"))
                    binary = inst.to_binary(rs, rt, immediate=offset)
                else:
                    rt = self.get_register_number(args[0])
                    rs = self.get_register_number(args[1])
                    imm = int(args[2])
                    binary = inst.to_binary(rs, rt, immediate=imm)
                    
            else:  # Format.J
                target = int(args[0])
                binary = inst.to_binary(0, 0, immediate=target)
                
            return (instruction, binary)
            
        except Exception as e:
            raise ValueError(f"Error parsing instruction '{instruction}': {str(e)}")

    def execute_instruction(self, instruction: str):
        parts = instruction.split()
        op = parts[0]
        args = [arg.strip(",") for arg in parts[1:]]
        
        inst = self.instruction_set[op]
        
        try:
            if inst.format == Format.R:
                if op in ["sll", "srl"]:
                    rd_num = self.get_register_number(args[0])
                    rt_num = self.get_register_number(args[1])
                    shamt = int(args[2])
                    
                    rd = self.get_register_by_number(rd_num)
                    rt = self.get_register_by_number(rt_num)
                    
                    if op == "sll":
                        rd.value = (rt.value << shamt) & 0xFFFFFFFF
                    else:  # srl
                        rd.value = (rt.value >> shamt) & 0xFFFFFFFF
                elif op == "jr":
                    rs_num = self.get_register_number(args[0])
                    rs = self.get_register_by_number(rs_num)
                    self.pc = rs.value
                else:
                    rd_num = self.get_register_number(args[0])
                    rs_num = self.get_register_number(args[1])
                    rt_num = self.get_register_number(args[2])
                    
                    rd = self.get_register_by_number(rd_num)
                    rs = self.get_register_by_number(rs_num)
                    rt = self.get_register_by_number(rt_num)
                    
                    if op == "add":
                        rd.value = (rs.value + rt.value) & 0xFFFFFFFF
                    elif op == "sub":
                        rd.value = (rs.value - rt.value) & 0xFFFFFFFF
                    elif op == "and":
                        rd.value = rs.value & rt.value
                    elif op == "or":
                        rd.value = rs.value | rt.value
                    elif op == "slt":
                        rd.value = 1 if rs.value < rt.value else 0
                        
            elif inst.format == Format.I:
                if op in ["lw", "sw"]:
                    rt_num = self.get_register_number(args[0])
                    offset = int(args[1].split("(")[0])
                    rs_num = self.get_register_number(args[1].split("(")[1].strip(")"))
                    
                    rt = self.get_register_by_number(rt_num)
                    rs = self.get_register_by_number(rs_num)
                    addr = (rs.value + offset) & 0xFFFFFFFF
                    
                    if addr >= len(self.data_memory):
                        raise ValueError(f"Memory access out of bounds: {addr}")
                    
                    if op == "lw":
                        rt.value = int.from_bytes(self.data_memory[addr:addr+4], 'big')
                    else:  # sw
                        value = rt.value.to_bytes(4, 'big')
                        self.data_memory[addr:addr+4] = value
                else:
                    rt_num = self.get_register_number(args[0])
                    rs_num = self.get_register_number(args[1])
                    imm = int(args[2])
                    
                    rt = self.get_register_by_number(rt_num)
                    rs = self.get_register_by_number(rs_num)
                    
                    if op == "addi":
                        rt.value = (rs.value + imm) & 0xFFFFFFFF
                    elif op == "beq":
                        if rs.value == rt.value:
                            self.pc += imm * 4
                    elif op == "bne":
                        if rs.value != rt.value:
                            self.pc += imm * 4
                            
            else:  # Format.J
                target = int(args[0])
                if op == "jal":
                    self.registers[31].value = self.pc + 4
                self.pc = target * 4
                
        except Exception as e:
            raise ValueError(f"Error executing instruction '{instruction}': {str(e)}")

class MIPSSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MIPS Simulator - 32 Bit Ide")
        self.simulator = MIPSSimulator()
        self.create_gui()
        
    def create_gui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(sticky="nsew")
        
        # Left panel
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, padx=5, sticky="nsew")
        
        # Assembly code input with gray background
        code_frame = ttk.Frame(left_frame)
        code_frame.pack(fill=tk.BOTH, expand=True)
        
        self.code_text = scrolledtext.ScrolledText(code_frame, width=40, height=15, bg='lightgray')
        self.code_text.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        control_frame = ttk.Frame(left_frame)
        control_frame.pack(pady=5)
        ttk.Button(control_frame, text="Assemble", command=self.assemble).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Step", command=self.step, state=tk.DISABLED).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Run", command=self.run_program, state=tk.DISABLED).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=2)
        
        # Store button references
        self.step_button = control_frame.winfo_children()[1]
        self.run_button = control_frame.winfo_children()[2]
        
        # Right side layouts
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, padx=5, sticky="nsew")
        
        # Register display
        reg_frame = ttk.Frame(right_frame)
        reg_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Name", "Number", "Value", "DecimalValue")
        self.reg_tree = ttk.Treeview(reg_frame, columns=columns, show="headings")
        for col in columns:
            self.reg_tree.heading(col, text=col)
            self.reg_tree.column(col, width=100)
        self.reg_tree.pack(fill=tk.BOTH, expand=True)
        
        # Instruction memories frame
        inst_memories_frame = ttk.LabelFrame(right_frame, text="Instruction Memories")
        inst_memories_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Instruction Memory table
        inst_memory_frame = ttk.LabelFrame(inst_memories_frame, text="Instruction Memory")
        inst_memory_frame.pack(fill=tk.BOTH, expand=True)
        
        self.inst_memory_tree = ttk.Treeview(inst_memory_frame,
                                           columns=("Address", "Value"),
                                           show="headings", height=6)
        self.inst_memory_tree.heading("Address", text="Address")
        self.inst_memory_tree.heading("Value", text="Value")
        self.inst_memory_tree.pack(fill=tk.BOTH, expand=True)
        
        # Instructions frame
        instructions_frame = ttk.LabelFrame(inst_memories_frame, text="Instructions")
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        
        self.instructions_text = scrolledtext.ScrolledText(instructions_frame, height=4)
        self.instructions_text.pack(fill=tk.BOTH, expand=True)
        
        # Machine Code frame
        machine_code_frame = ttk.LabelFrame(inst_memories_frame, text="Machine Code")
        machine_code_frame.pack(fill=tk.BOTH, expand=True)
        
        self.machine_code_text = scrolledtext.ScrolledText(machine_code_frame, height=4)
        self.machine_code_text.pack(fill=tk.BOTH, expand=True)
        
        # Memory section
        mem_frame = ttk.LabelFrame(right_frame, text="Memory")
        mem_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.mem_tree = ttk.Treeview(mem_frame, columns=("Address", "MemoryValue"), 
                                    show="headings", height=6)
        self.mem_tree.heading("Address", text="Address")
        self.mem_tree.heading("MemoryValue", text="MemoryValue")
        self.mem_tree.pack(fill=tk.BOTH, expand=True)
        
        self.initialize_displays()
        
    def initialize_displays(self):
        # Initialize memory display with empty values
        for item in self.mem_tree.get_children():
            self.mem_tree.delete(item)
            
        for addr in range(0, 1024, 4):
            self.mem_tree.insert("", tk.END, values=(
                f"0x{addr:08x}",
                "0x00000000"
            ))
            
        # Initialize instruction memory
        for item in self.inst_memory_tree.get_children():
            self.inst_memory_tree.delete(item)
            
        for addr in range(0, 1024, 4):
            self.inst_memory_tree.insert("", tk.END, values=(
                f"0x{addr:08x}",
                "0x00000000"
            ))
        
        # Clear instruction text and machine code
        self.instructions_text.delete("1.0", tk.END)
        self.machine_code_text.delete("1.0", tk.END)
            
        self.update_displays()
    
    def assemble(self):
        try:
            # Clear previous state
            self.simulator.instruction_memory.clear()
            self.simulator.pc = 0
            
            # Clear displays
            for item in self.inst_memory_tree.get_children():
                self.inst_memory_tree.delete(item)
            self.instructions_text.delete("1.0", tk.END)
            self.machine_code_text.delete("1.0", tk.END)
            
            # Get assembly code lines
            code_lines = [line.strip() for line in self.code_text.get("1.0", tk.END).splitlines() if line.strip()]
            
            # Process each instruction
            for i, line in enumerate(code_lines):
                instruction, binary = self.simulator.parse_instruction(line)
                addr = i * 4
                self.simulator.instruction_memory[addr] = (instruction, binary)
                
                # Update instruction memory display
                self.inst_memory_tree.insert("", tk.END, values=(
                    f"0x{addr:08x}",
                    binary
                ))
                
                # Update instructions text
                self.instructions_text.insert(tk.END, f"{instruction}\n")
                
                # Update machine code text
                self.machine_code_text.insert(tk.END, f"{binary}\n")
            
            # Enable step and run buttons
            self.step_button.config(state=tk.NORMAL)
            self.run_button.config(state=tk.NORMAL)
            
            messagebox.showinfo("Success", "Program assembled successfully")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def step(self):
        try:
            if self.simulator.pc in self.simulator.instruction_memory:
                # Clear previous highlights
                self.instructions_text.tag_remove("current", "1.0", tk.END)
                
                # Get current instruction
                instruction, _ = self.simulator.instruction_memory[self.simulator.pc]
                line_number = self.simulator.pc // 4
                
                # Highlight current instruction
                start = f"{line_number + 1}.0"
                end = f"{line_number + 2}.0"
                self.instructions_text.tag_add("current", start, end)
                self.instructions_text.tag_config("current", background="yellow")
                
                # Execute instruction
                self.simulator.execute_instruction(instruction)
                if "j" not in instruction and "beq" not in instruction and "bne" not in instruction:
                    self.simulator.pc += 4
                
                self.update_displays()
                
                # Disable step and run buttons if program is finished
                if self.simulator.pc > max(self.simulator.instruction_memory.keys()):
                    self.step_button.config(state=tk.DISABLED)
                    self.run_button.config(state=tk.DISABLED)
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def run_program(self):
        try:
            max_addr = max(self.simulator.instruction_memory.keys())
            while self.simulator.pc <= max_addr:
                self.step()
                self.root.update()
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def reset(self):
        # Reset simulator
        self.simulator = MIPSSimulator()
        
        # Clear code text and disable buttons
        self.code_text.delete("1.0", tk.END)
        self.step_button.config(state=tk.DISABLED)
        self.run_button.config(state=tk.DISABLED)
        
        # Clear all displays
        self.initialize_displays()
    
    def update_displays(self):
        # Update register display
        for item in self.reg_tree.get_children():
            self.reg_tree.delete(item)
            
        for reg in self.simulator.registers:
            self.reg_tree.insert("", tk.END, values=(
                reg.name,
                reg.number,
                f"0x{reg.value & 0xFFFFFFFF:08x}",
                reg.value
            ))
        
        # Update memory display
        for addr in range(0, len(self.simulator.data_memory), 4):
            value = int.from_bytes(self.simulator.data_memory[addr:addr+4], 'big')
            for item in self.mem_tree.get_children():
                if self.mem_tree.item(item)['values'][0] == f"0x{addr:08x}":
                    self.mem_tree.item(item, values=(
                        f"0x{addr:08x}",
                        f"0x{value:08x}"
                    ))
                    break

def run_gui():
    root = tk.Tk()
    app = MIPSSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()