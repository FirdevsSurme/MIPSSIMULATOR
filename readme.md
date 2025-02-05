# MIPS ASSEMBLE SIMULATER #

# TEAM MEMBERS
Dilanur Aygün 212010020111
Zeynep Tuba Başar 212010020059
Berranur Özyalvaç 212010020049
Firdevs Sürmegözlüer 222010020041

# OVERVIEW
This project implements a simulator for a subset of the MIPS 32-bit architecture. The goal is to provide an educational tool for understanding computer architecture, instruction set architecture, and system simulation. The simulator allows you to execute basic MIPS instructions and observe how the processor handles them.

# FEATURES
Supported Instruction Types
This simulator supports the following MIPS instruction types:
R-Format Instructions,
R-Format instructions are used for arithmetic and logical operations. These instructions operate on registers and manipulate data within the CPU.
add rd, rs, rt: Adds the values of rs and rt, stores the result in rd.
sub rd, rs, rt: Subtracts rt from rs, stores the result in rd.
and rd, rs, rt: Performs a bitwise AND of rs and rt, stores the result in rd.
or rd, rs, rt: Performs a bitwise OR of rs and rt, stores the result in rd.
slt rd, rs, rt: Sets rd to 1 if rs is less than rt, otherwise 0.
sll rd, rt, shamt: Shifts rt left by shamt positions, stores the result in rd.
srl rd, rt, shamt: Shifts rt right by shamt positions, stores the result in rd.
I-Format Instructions
I-Format instructions are used for memory access and branching. These instructions often use an immediate value along with register operands.
addi rt, rs, imm: Adds the immediate value imm to rs, stores the result in rt.
lw rt, offset(rs): Loads a word from memory at address rs + offset into rt.
sw rt, offset(rs): Stores the word in rt into memory at address rs + offset.
beq rs, rt, label: Branches to label if rs equals rt.
bne rs, rt, label: Branches to label if rs is not equal to rt.
J-Format Instructions
J-Format instructions are used for jumping to specific addresses in the program.
j target: Jumps to the target address.
jal target: Jumps to the target address and saves the return address in the ra register.
jr rs: Jumps to the address stored in the rs register.

# CORE FEATURES
Program Counter Management
The program counter (PC) tracks the address of the next instruction to be executed. After each instruction, the PC is updated:
Sequential instructions: The PC is incremented by 4 (since each instruction is 4 bytes long).
Branch or jump instructions: The PC is updated based on the target address or offset provided by the instruction.
Memory Management
The simulator handles both instruction and data memory. Both are allocated a fixed size of 512 bytes, ensuring the memory is managed and bounded.
Instruction Memory (IM): Stores the MIPS assembly code. It has a capacity of 512 bytes.
Data Memory (DM): Stores the data values. It also has a capacity of 512 bytes.
Memory Access: The lw (load word) and sw (store word) instructions interact with memory by reading and writing data at the specified memory locations.
Bounds Checking: The simulator ensures that memory access stays within the 512-byte boundary, avoiding out-of-bounds errors.
Fetch-Decode-Execute Cycle
The simulator implements the classic fetch-decode-execute cycle, which is the fundamental cycle in the operation of a processor:
Fetch: The instruction at the current Program Counter (PC) is fetched from memory.
Decode: The instruction is decoded to determine the operation to be performed, as well as its operands (such as registers and immediate values).
Execute: The operation is performed, and the results are written back to either registers or memory.

# Installation
To run the MIPS Assembler and Simulator, Python 3.x must be installed on your machine. Tkinter, which is used for the graphical user interface (GUI), comes pre-installed with Python.
Requirements:
Python 3.x
Tkinter (comes with Python)
Running the Simulator
Download or clone the repository to your local machine.

Open a terminal and navigate to the project directory.

Run the simulator by executing the following command:
 python mips_simulator.py

The GUI will open, where you can input assembly code and run the simulation.

# Usage
Once the GUI is loaded, you can interact with the simulator in the following way:
Enter Assembly Code:
The left pane of the interface allows you to input or edit MIPS assembly code.
Run Instructions:

Assemble & Run: Click this button to assemble and run the entire program.
Step: Use this button to execute the program one instruction at a time, observing the changes in registers and memory.
View Output:

Binary Output: Displays the binary representation of each instruction.
Registers: Displays the current state of all 32 registers.
Memory: Displays the contents of memory, showing the first 512 bytes.
Clear: This button clears all inputs and outputs and resets the registers and memory.

# Architecture
The MIPS simulator is implemented in Python, and the system is modularized into different components:
Instruction Parser: Converts MIPS assembly code into binary instructions.
Execution Cycle: Fetches, decodes, and executes instructions, updating registers and memory.
GUI: A Tkinter-based graphical interface that allows users to interact with the simulator, input MIPS code, and view results step by step.
Key Files:
mips_simulator.py: The main file that runs the MIPS simulator.
gui.py: Contains the GUI code using Tkinter.
assembler.py: Handles parsing assembly code and converting it into binary instructions.
simulator.py: Manages the MIPS simulation cycle, including updating registers and memory.

# Testing
Several tests have been written to ensure that the simulator works as expected. These tests cover various aspects of the simulator, including instruction parsing, binary conversion, and execution.
Test Coverage
Instruction Decoding: Ensures that each instruction is decoded correctly.
Execution: Verifies that each instruction executes correctly and updates registers and memory as expected.
Error Handling: Handles edge cases, such as invalid instructions or memory access errors.

# Known Limitations
Currently, only a subset of MIPS instructions are supported. Additional instructions may be added in the future.
Memory management is simplified to a fixed 512-byte capacity for both instruction and data memory.
Advanced features like pipelining and parallel execution are not yet supported.

# Conclusion
The MIPS Assembler and Simulator project is a useful educational tool for understanding computer architecture and instruction execution. It provides a hands-on way to explore how a processor handles MIPS assembly instructions, performs memory access, and manages the program counter. With further improvements, the simulator can be expanded to support more advanced features and instructions.


