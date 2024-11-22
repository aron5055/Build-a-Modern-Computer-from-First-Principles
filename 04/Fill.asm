// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

    @SCREEN
    D=A
    @ptr
    M=D

(LOOP)
    @KBD
    D=M
    @BLACK
    D;JNE
    @WHITE
    0;JMP

(BLACK)
    @ptr
    A=M
    M=-1
    @UPDATE
    0;JMP

(WHITE)
    @ptr
    A=M
    M=0
    @UPDATE
    0;JMP

(UPDATE)
    @ptr
    D=M
    @24576 // 16384(SCREEN) + 8192(8K)
    D=D-A
    @SCREEN // reset
    D;JGE
    @ptr
    M=M+1
    @LOOP
    0;JMP
