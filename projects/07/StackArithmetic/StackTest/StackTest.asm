// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
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
D=M
@SETTRUE1
D;JEQ
(SETFALSE1)
@SP
A=M
M=0
@FINISH1
0;JMP
(SETTRUE1)
@SP
A=M
M=-1
@FINISH1
0;JMP
(FINISH1)
@SP
M=M+1
// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
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
D=M
@SETTRUE2
D;JEQ
(SETFALSE2)
@SP
A=M
M=0
@FINISH2
0;JMP
(SETTRUE2)
@SP
A=M
M=-1
@FINISH2
0;JMP
(FINISH2)
@SP
M=M+1
// C_PUSH constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
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
D=M
@SETTRUE3
D;JEQ
(SETFALSE3)
@SP
A=M
M=0
@FINISH3
0;JMP
(SETTRUE3)
@SP
A=M
M=-1
@FINISH3
0;JMP
(FINISH3)
@SP
M=M+1
// C_PUSH constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
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
D=M
@SETTRUE4
D;JLT
(SETFALSE4)
@SP
A=M
M=0
@FINISH4
0;JMP
(SETTRUE4)
@SP
A=M
M=-1
@FINISH4
0;JMP
(FINISH4)
@SP
M=M+1
// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
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
D=M
@SETTRUE5
D;JLT
(SETFALSE5)
@SP
A=M
M=0
@FINISH5
0;JMP
(SETTRUE5)
@SP
A=M
M=-1
@FINISH5
0;JMP
(FINISH5)
@SP
M=M+1
// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
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
D=M
@SETTRUE6
D;JLT
(SETFALSE6)
@SP
A=M
M=0
@FINISH6
0;JMP
(SETTRUE6)
@SP
A=M
M=-1
@FINISH6
0;JMP
(FINISH6)
@SP
M=M+1
// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
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
D=M
@SETTRUE7
D;JGT
(SETFALSE7)
@SP
A=M
M=0
@FINISH7
0;JMP
(SETTRUE7)
@SP
A=M
M=-1
@FINISH7
0;JMP
(FINISH7)
@SP
M=M+1
// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
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
D=M
@SETTRUE8
D;JGT
(SETFALSE8)
@SP
A=M
M=0
@FINISH8
0;JMP
(SETTRUE8)
@SP
A=M
M=-1
@FINISH8
0;JMP
(FINISH8)
@SP
M=M+1
// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
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
D=M
@SETTRUE9
D;JGT
(SETFALSE9)
@SP
A=M
M=0
@FINISH9
0;JMP
(SETTRUE9)
@SP
A=M
M=-1
@FINISH9
0;JMP
(FINISH9)
@SP
M=M+1
// C_PUSH constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 53
@53
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
// C_PUSH constant 112
@112
D=A
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
// neg
@SP
M=M-1
@SP
A=M
M=-M
@SP
M=M+1
// and
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M&D
@SP
M=M+1
// C_PUSH constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M|D
@SP
M=M+1
// not
@SP
M=M-1
@SP
A=M
M=!M
@SP
M=M+1
