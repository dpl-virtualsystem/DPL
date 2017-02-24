# DPL
A virtual system, much like CHIP-8.

Opcode reference in `opcodes.txt` and assembler and patch tool in marked directories.

## Specs
DPL has a 256x256 screen, and a 16 button keypad.  
Programs are stored in ROM (memory bank 0x0) starting at $0000.  
Keypad state is at $0000 in RAM (emory bank 0x1).
VRAM (memory bank 0x2) is accessed as 0xXXYY where X is the X coord and Y is the Y coord. (i.e; upper left corner is 0x0000, lower right is 0xFFFF)
ROMs are limited to being 65536 bytes in size.

Keypad state format

0000 0000  
1234 5678

1. Up (default W)
2. Down (default S)
3. Left (default A)
4. Right (default D)
5. Button 1 (default Q)
6. Button 2 (default E)
7. Button 3 (default Z)
8. Button 4 (default X)
