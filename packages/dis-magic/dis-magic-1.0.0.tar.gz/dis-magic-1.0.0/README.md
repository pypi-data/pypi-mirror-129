This allows you to visualize the bytecode of a cell in IPython upon running it.

## Installation

    pip3 install dis-magic

To manually load, run the following in your IPython prompt:
    
    %load_ext dis_magic

To automatically load, add the following to your [IPython configuration file](https://ipython.org/ipython-doc/3/config/intro.html):
    
    c = get_config()
    c.InteractiveShellApp.extensions.append('dis_magic')
    
## Usage

Verifying Python follows PEMDAS:

    In [6]: %dis foo = 6 ** 2 + 6
      1           0 LOAD_CONST               0 (42)
                  2 STORE_NAME               0 (foo)
                  4 LOAD_CONST               1 (None)
                  6 RETURN_VALUE
        
You can use it in a cell too:

    In [4]: %%dis
       ...:
       ...: def fibonacci(n: int) -> int:
       ...:     if n <= 1: return 1
       ...:     return fibonacci(n - 2) + fibonacci(n - 1)
       ...:
      2           0 LOAD_NAME                0 (int)
                  2 LOAD_NAME                0 (int)
                  4 LOAD_CONST               0 (('n', 'return'))
                  6 BUILD_CONST_KEY_MAP      2
                  8 LOAD_CONST               1 (<code object fibonacci at 0x111457b30, file "<dis>", line 2>)
                 10 LOAD_CONST               2 ('fibonacci')
                 12 MAKE_FUNCTION            4 (annotations)
                 14 STORE_NAME               1 (fibonacci)
                 16 LOAD_CONST               3 (None)
                 18 RETURN_VALUE
    
    Disassembly of <code object fibonacci at 0x111457b30, file "<dis>", line 2>:
      3           0 LOAD_FAST                0 (n)
                  2 LOAD_CONST               1 (1)
                  4 COMPARE_OP               1 (<=)
                  6 POP_JUMP_IF_FALSE       12
                  8 LOAD_CONST               1 (1)
                 10 RETURN_VALUE
    
      4     >>   12 LOAD_GLOBAL              0 (fibonacci)
                 14 LOAD_FAST                0 (n)
                 16 LOAD_CONST               2 (2)
                 18 BINARY_SUBTRACT
                 20 CALL_FUNCTION            1
                 22 LOAD_GLOBAL              0 (fibonacci)
                 24 LOAD_FAST                0 (n)
                 26 LOAD_CONST               1 (1)
                 28 BINARY_SUBTRACT
                 30 CALL_FUNCTION            1
                 32 BINARY_ADD
                 34 RETURN_VALUE