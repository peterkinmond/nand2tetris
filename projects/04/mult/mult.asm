// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Pseudo-code
//  n = R0
//  m = R1
//  i = 1
//  sum = 0
// LOOP:
//  if i > n goto STOP
//    sum = sum + m
//    i = i + 1
//    goto LOOP
// STOP:
//  R2 = sum

// Real code
  //  n = R0
  @R0
  D=M
  @n
  M=D

  //  m = R1
  @R1
  D=M
  @m
  M=D

  //  i = 1
  @i
  M=1

  //  sum = 0
  @sum
  M=0

// LOOP:
(LOOP)
  //  if i > n goto STOP
  @i
  D=M
  @n
  D=D-M
  @STOP
  D;JGT

  //    sum = sum + m
  @m
  D=M
  @sum
  M=D+M

  //    i = i + 1
  @i
  M=M+1

  //    goto LOOP
  @LOOP
  0;JMP

// STOP:
(STOP)
  //  R2 = sum
  @sum
  D=M
  @R2
  M=D

(END)
  @END
  0;JMP
