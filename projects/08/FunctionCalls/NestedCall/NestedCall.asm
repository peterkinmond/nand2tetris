@256
D=A
@SP
M=D
// call Sys.init 0
// push NestedCall$ret.1
@NestedCall$ret.1
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
(NestedCall$ret.1)
// function Sys.init 0
(Sys.init)
// C_PUSH constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D
// C_PUSH constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D
// call Sys.main 0
// push NestedCall$ret.2
@NestedCall$ret.2
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
// goto Sys.main
@Sys.main
0;JMP
// (retAddrLabel)
(NestedCall$ret.2)
// C_POP temp 1
@5
D=A
@1
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
// label LOOP
(LOOP)
// goto LOOP
@LOOP
0;JMP
// function Sys.main 5
(Sys.main)
// C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D
// C_PUSH constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D
// C_PUSH constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP local 1
@LCL
D=M
@1
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
// C_PUSH constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP local 2
@LCL
D=M
@2
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
// C_PUSH constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP local 3
@LCL
D=M
@3
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
// C_PUSH constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Sys.add12 1
// push NestedCall$ret.3
@NestedCall$ret.3
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
@1
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto Sys.add12
@Sys.add12
0;JMP
// (retAddrLabel)
(NestedCall$ret.3)
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
// C_PUSH local 0
@LCL
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
// C_PUSH local 1
@LCL
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
// C_PUSH local 2
@LCL
D=M
@2
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
// C_PUSH local 3
@LCL
D=M
@3
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
// C_PUSH local 4
@LCL
D=M
@4
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
// add
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
// add
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
// add
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
@SP
M=M+1
// add
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
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
// function Sys.add12 0
(Sys.add12)
// C_PUSH constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 0
@SP
M=M-1
@SP
A=M
D=M
@THIS
M=D
// C_PUSH constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 1
@SP
M=M-1
@SP
A=M
D=M
@THAT
M=D
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
// C_PUSH constant 12
@12
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M+D
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
