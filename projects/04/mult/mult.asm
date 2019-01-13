// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Pseudo-code
//  if R0 == 0 goto STOP (since product will be 0)
//  n = R0
//  if R1 == 0 goto STOP (since product will be 0)
//  m = R1
//  i = 1
//  product = 0
// LOOP:
//  if i > n goto STOP
//    product = product + m
//    i = i + 1
//    goto LOOP
// STOP:
//  R2 = product

// Real code
  // if R0 == 0 goto STOP
  @R0
  D=M
  @STOP
  D;JEQ

  //  n = R0
  @n
  M=D

  // if R1 == 0 goto STOP
  @R1
  D=M
  @STOP
  D;JEQ

  //  m = R1
  @m
  M=D

  //  i = 1
  @i
  M=1

  //  product = 0
  @product
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

  //    product = product + m
  @m
  D=M
  @product
  M=D+M

  //    i = i + 1
  @i
  M=M+1

  //    goto LOOP
  @LOOP
  0;JMP

// STOP:
(STOP)
  //  R2 = product
  @product
  D=M
  @R2
  M=D

(END)
  @END
  0;JMP
