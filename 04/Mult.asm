// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//      i = 0
//      mult = 0
// loop i < R1:
//      mult = mult + R0
//      i = i + 1
// R2 = mult

    // i = 0; mult = 0
    @0
    D=A
    @i
    M=D
    @mult
    M=D

(LOOP)
    // while (i < R1) {}
    @R1
    D=M
    @i
    D=D-M
    @STOP
    D;JLE
    // mult = mult + R0
    @R0
    D=M
    @mult
    M=D+M
    // i = i + 1
    @i
    M=M+1
    @LOOP
    0;JMP
(STOP)
    // R2 = mult
    @mult
    D=M
    @R2
    M=D
(END)
    @END
    0;JMP
