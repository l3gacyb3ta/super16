# super16
A strange little 16bit ISA/Architecture.  
  
## Theory
One instruction is composed of 32 bits, making up 3 catagories; Opcode, Register and data. The opcode is two hexadecimal digits, the register is another two, and the data is a 4-digit hexadecimal number split into two two-digit numbers. Here is an example instruction loading ```0xf988``` into ```r5```:  
| Opcode | Register | Data 1 | Data 2 |
|--------|----------|--------|--------|
| 0x20   | 0x05     | 0xf9   | 0x88   |
  
The full list of opcodes, as well as an example, the instruction & explaination are as follows:  
| opcode | instruction |                                                                             |
|--------|-------------|-----------------------------------------------------------------------------|
| 0x10   | store       | store reg reg2                                                              |
|        |             | Copy value from one reg to another                                          |
| 0x20   | load        | load reg val                                                                |
|        |             | Load a value into a reg                                                     |
| 0x30   | add         | add reg val                                                                 |
|        |             | Add value to reg                                                            |
| 0x31   | addr        | addr reg reg2                                                               |
|        |             | Adds reg2 to reg                                                            |
| 0x40   | sub         | sub reg val                                                                 |
|        |             | Subtracts val from reg                                                      |
| 0x41   | subr        | subr reg reg2                                                               |
|        |             | Subtracts reg2 from reg                                                     |
| 0x50   | mul         | mul reg val                                                                 |
|        |             | Multipy register by value                                                   |
| 0x51   | mulr        | mul reg reg2                                                                |
|        |             | Multiply reg by reg 2                                                       |
| 0x60   | div         | div reg val                                                                 |
|        |             | Intiger divides the register by the value                                   |
| 0x61   | divr        | div reg reg2                                                                |
|        |             | Initger devides reg by rg2                                                  |
| 0xff   | prt         | prt 0x0000 0x0000                                                           |
|        |             | Print ascii value in p0 reg                                                 |
| 0x0f   | scrn        | scrn 0x0000 val                                                             |
|        |             | Set pixel in x8 and y9 regs to the value (0: black) (1: white)              |
| 0xdd   | drw         | drw 0x0000 0x0000                                                           |
|        |             | Draw screen buffer                                                          |
| 0xf0   | cmp         | cmp reg reg2                                                                |
|        |             | Set cm reg to 0x0001 if bigger, 0x0000 if smaller, and 0xffff if their equal|
| 0xb0   | branch      | branch val label                                                            |
|        |             | Branch to loop if cm is val                                                 |
| 0xb1   | nbranch     | nbranch val label                                                           |
|        |             | Branch to loop if cm is not val                                             |
| 0xbb   | jump        | jump 0x0000 label                                                           |
|        |             | Jump to label                                                               |
| 0x00   | noop        | noop 0x000 0x000                                                            |
|        |             | Literally does nothing                                                      |
| 0xfe   | halt        | halt 0x0000 0x0000                                                          |
|        |             | Halts the cpu                                                               |
  
## Installing
Run ```git clone https://github.com/l3gacyb3ta/super16.git && cd super16```, then run whatever command you like! Examples are bellow in the example commands section.  
  
## How to run with emulator
As I have not yet learned how to build an actual sim in logisim or similar software (so many sim-s!), I have implemented this ISA in python. After running ```assembler.py``` with a valid asembly file as an argument, a pickle file named rom.pic will appear. In order to run it, simply execute ```cpu.py``` for normal use, and ```slowpu.py``` for debugging.  
  
## Binary compiling
In order to compile to a binary that would run on a theoretical S16 cpu, simply invoke ```binaryassembler.py``` with the asembley file as a parameter.  
  
## Examples
A set of example programs are provided in the ```tests/``` directory. This is a great place to begin programming for S16. I have also included a script ```test.sh``` to run a test file. To do that, simply run ```test.sh``` and type the name (without .asm) of the file you want to run, and it should run.  
  
## Example commands
* Running an assembly file:
```
$ python assembler.py tests/scrn.asm
$ python cpu.py
```
* Compiling to a binary:
```
$ python binaryassembler.py tests/scrn.asm
```