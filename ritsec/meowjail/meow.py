# coding: horror
from horror import horror

@horror
def meow(stdin):
    section .bss
        sum resd 1
        cbuf resb 1

    section .text
        global _start

    _start:
        mov dword [sum], 0
    rloop:
        call getchar
        cmp rax, 0
        je eloop
        mov al, byte [cbuf]
        cmp al, 0x2c
        je comma
        cmp al, 226
        je c226
        cmp al, 240
        je c240
        jmp rloop
    comma:
        inc dword [sum]
        jmp rloop
    c226:
        call getchar
        cmp rax, 0
        je eloop
        mov al, byte [cbuf]
        cmp al, 156
        je c226_156
        jmp c226_else
    c226_156:
        call getchar
        cmp rax, 0
        je eloop
        add dword [sum], 10
        jmp rloop
    c226_else:
        call getchar
        call getchar
        call getchar
        call getchar
        jmp rloop
    c240:
        call getchar
        cmp rax, 0
        je eloop
        call getchar
        cmp rax, 0
        je eloop
        mov al, byte [cbuf]
        cmp al, 171
        je c240_171
        cmp al, 146
        je c240_146
        cmp al, 165
        je c240_165
        cmp al, 145
        je c240_145
        jmp c240_def
    c240_171:
        add dword [sum], 200
        jmp c240_def
    c240_146:
        add dword [sum], 50
        jmp c240_def
    c240_165:
        add dword [sum], 5
        jmp c240_def
    c240_145:
        call getchar
        call getchar
        call getchar
        call getchar
        mov eax, dword [sum]
        call putchar
        mov dword [sum], 0
    c240_def:
        call getchar
        jmp rloop
    eloop:
        mov rax, 60
        xor rdi, rdi
        syscall

    getchar:
        push rbp
        mov rbp, rsp
        mov rax, 0
        mov rdi, 0
        mov rsi, cbuf
        mov rdx, 1
        syscall
        cmp rax, 0
        jle .eof
        movzx eax, byte [cbuf]
        jmp .end
    .eof:
        xor eax, eax
    .end:
        mov rsp, rbp
        pop rbp
        ret

    putchar:
        push rbp
        mov rbp, rsp
        mov [cbuf], al
        mov rax, 1
        mov rdi, 1
        mov rsi, cbuf
        mov rdx, 1
        syscall
        mov rsp, rbp
        pop rbp
        ret

meoww = input("use your words: ")
if len(meoww) > 800:
    print("mrowww :(")
    exit(1)
meowww = meow(meoww)
try:
    meowwww = eval(meowww, {'__builtins__': None})
except:
    print("meep :(")
    exit(1)

print("meowmeow!!!")