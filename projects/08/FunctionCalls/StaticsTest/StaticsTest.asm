@256
D=A
@SP
M=D
// call Sys.init 0
// push StaticsTest$ret.1
@StaticsTest$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-5-nArgs
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Sys.init
@Sys.init
0;JMP
// (retAddrLabel)
(StaticsTest$ret.1)
// function Class1.set 0
(Class1.set)
// C_PUSH argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_POP static 0
@SP
M=M-1
@SP
A=M
D=M
@Class1.0
M=D
// C_PUSH argument 1
@ARG
D=M
@1
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_POP static 1
@SP
M=M-1
@SP
A=M
D=M
@Class1.1
M=D
// C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// return
// endFrame = LCL
@LCL
D=M
@R13
M=D
// retAddr = *(endFrame - 5)
@5
D=A
@R13
D=M-D
A=D
D=M
@R14
M=D
// *ARG = pop()
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
// SP = ARG + 1
@ARG
D=M+1
@SP
M=D
// THAT = *(endFrame - 1)
@1
D=A
@R13
D=M-D
A=D
D=M
@THAT
M=D
// THIS = *(endFrame - 2)
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
// ARG = *(endFrame - 3)
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
// LCL = *(endFrame - 4)
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
// goto retAddr
@R14
A=M
0;JMP
// function Class1.get 0
(Class1.get)
// C_PUSH static 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH static 1
@Class1.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
// return
// endFrame = LCL
@LCL
D=M
@R13
M=D
// retAddr = *(endFrame - 5)
@5
D=A
@R13
D=M-D
A=D
D=M
@R14
M=D
// *ARG = pop()
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
// SP = ARG + 1
@ARG
D=M+1
@SP
M=D
// THAT = *(endFrame - 1)
@1
D=A
@R13
D=M-D
A=D
D=M
@THAT
M=D
// THIS = *(endFrame - 2)
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
// ARG = *(endFrame - 3)
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
// LCL = *(endFrame - 4)
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
// goto retAddr
@R14
A=M
0;JMP
// function Sys.init 0
(Sys.init)
// C_PUSH constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class1.set 2
// push Sys$ret.1
@Sys$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-5-nArgs
@SP
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Class1.set
@Class1.set
0;JMP
// (retAddrLabel)
(Sys$ret.1)
// C_POP temp 0
@5
D=A
@0
D=D+A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
// C_PUSH constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class2.set 2
// push Sys$ret.2
@Sys$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-5-nArgs
@SP
D=M
@5
D=D-A
@2
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Class2.set
@Class2.set
0;JMP
// (retAddrLabel)
(Sys$ret.2)
// C_POP temp 0
@5
D=A
@0
D=D+A
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@R13
A=M
M=D
// call Class1.get 0
// push Sys$ret.3
@Sys$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-5-nArgs
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Class1.get
@Class1.get
0;JMP
// (retAddrLabel)
(Sys$ret.3)
// call Class2.get 0
// push Sys$ret.4
@Sys$ret.4
D=A
@SP
A=M
M=D
@SP
M=M+1
// push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
// push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-5-nArgs
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Class2.get
@Class2.get
0;JMP
// (retAddrLabel)
(Sys$ret.4)
// label WHILE
(WHILE)
// goto WHILE
@WHILE
0;JMP
// function Class2.set 0
(Class2.set)
// C_PUSH argument 0
@ARG
D=M
@0
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_POP static 0
@SP
M=M-1
@SP
A=M
D=M
@Class2.0
M=D
// C_PUSH argument 1
@ARG
D=M
@1
D=D+A
@R13
M=D
@R13
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_POP static 1
@SP
M=M-1
@SP
A=M
D=M
@Class2.1
M=D
// C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// return
// endFrame = LCL
@LCL
D=M
@R13
M=D
// retAddr = *(endFrame - 5)
@5
D=A
@R13
D=M-D
A=D
D=M
@R14
M=D
// *ARG = pop()
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
// SP = ARG + 1
@ARG
D=M+1
@SP
M=D
// THAT = *(endFrame - 1)
@1
D=A
@R13
D=M-D
A=D
D=M
@THAT
M=D
// THIS = *(endFrame - 2)
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
// ARG = *(endFrame - 3)
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
// LCL = *(endFrame - 4)
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
// goto retAddr
@R14
A=M
0;JMP
// function Class2.get 0
(Class2.get)
// C_PUSH static 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH static 1
@Class2.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
// return
// endFrame = LCL
@LCL
D=M
@R13
M=D
// retAddr = *(endFrame - 5)
@5
D=A
@R13
D=M-D
A=D
D=M
@R14
M=D
// *ARG = pop()
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
// SP = ARG + 1
@ARG
D=M+1
@SP
M=D
// THAT = *(endFrame - 1)
@1
D=A
@R13
D=M-D
A=D
D=M
@THAT
M=D
// THIS = *(endFrame - 2)
@2
D=A
@R13
D=M-D
A=D
D=M
@THIS
M=D
// ARG = *(endFrame - 3)
@3
D=A
@R13
D=M-D
A=D
D=M
@ARG
M=D
// LCL = *(endFrame - 4)
@4
D=A
@R13
D=M-D
A=D
D=M
@LCL
M=D
// goto retAddr
@R14
A=M
0;JMP
