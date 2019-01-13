// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Pseudo-code
// LOOP:
//  needsfill = 0   // Tracks whether to fill or clear the screen
//  if KBD == 0 goto DRAW
//  needsfill = 1
//  goto DRAW
//
// DRAW:
//  n = 8192  // screen memory map is 8K (2^13)
//  i = 0
//
// DRAWLOOP:
//  if i > n goto LOOP
//    RAM[SCREEN + i] = needsfill
//    i = i + 1
//    goto DRAWLOOP

// LOOP:
(LOOP)
  //  needsfill = 0   // Tracks whether to fill or clear the screen
  @needsfill
  M=0

  //  if KBD == 0 goto DRAW
  @KBD
  D=M
  @DRAW
  D;JEQ
  //  needsfill = 1
  @needsfill
  M=1
  //  goto DRAW
  @DRAW
  0;JMP

// DRAW:
(DRAW)
  //  n = 8192  // screen memory map is 8K (2^13)
  @8192
  D=A
  @n
  M=D

  //  i = 0
  @i
  M=0

// DRAWLOOP:
(DRAWLOOP)
  //  if i == n goto LOOP
  @i
  D=M
  @n
  D=D-M
  @LOOP
  D;JEQ

  //    RAM[SCREEN + i] = needsfill
  @needsfill
  D=M
  @CLEAR
  D;JEQ

  @FILL
  D;JMP

// TODO: Can we combine the loops?
(FILL)
  @SCREEN
  D=A
  @i
  A=D+M
  M=-1
  
  //    i = i + 1
  @i
  M=M+1

  //    goto DRAWLOOP
  @DRAWLOOP
  0;JMP

(CLEAR)
  @SCREEN
  D=A
  @i
  A=D+M
  M=0 

  //    i = i + 1
  @i
  M=M+1

  //    goto DRAWLOOP
  @DRAWLOOP
  0;JMP
