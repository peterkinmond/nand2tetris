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

@SETFALSE
D;JLE

(SETTRUE)
@SP
A=M
M=-1
@FINISH
0;JMP

(SETFALSE)
@SP
A=M
M=0
@FINISH
0;JMP

(FINISH)
@SP
M=M+1
