This allows you to visualize the AST of a cell in IPython upon running it.

## Installation

    pip3 install ast-magic

To manually load, run the following in your IPython prompt:
    
    %load_ext ast_magic

To automatically load, add the following to your [IPython configuration file](https://ipython.org/ipython-doc/3/config/intro.html):
    
    c = get_config()
    c.InteractiveShellApp.extensions.append('ast_magic')
    
## Usage

Verifying Python follows PEMDAS:

    In [1]: %ast (1 + 1) ** 2 * 5 - 4
    Module(
        body=[
            Expr(
                value=BinOp(
                    left=BinOp(
                        left=BinOp(
                            left=BinOp(
                                left=Constant(value=1),
                                op=Add(),
                                right=Constant(value=1)),
                            op=Pow(),
                            right=Constant(value=2)),
                        op=Mult(),
                        right=Constant(value=5)),
                    op=Sub(),
                    right=Constant(value=4)))],
        type_ignores=[])
        
You can use it in a cell too:

    In [1]: %%ast
       ...:
       ...: def fibonacci(n: int) -> int:
       ...:     if n <= 1: return 1
       ...:     return fibonacci(n - 2) + fibonacci(n - 1)
       ...:
    Module(
        body=[
            FunctionDef(
                name='fibonacci',
                args=arguments(
                    posonlyargs=[],
                    args=[
                        arg(
                            arg='n',
                            annotation=Name(id='int', ctx=Load()))],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]),
                body=[
                    If(
                        test=Compare(
                            left=Name(id='n', ctx=Load()),
                            ops=[
                                LtE()],
                            comparators=[
                                Constant(value=1)]),
                        body=[
                            Return(
                                value=Constant(value=1))],
                        orelse=[]),
                    Return(
                        value=BinOp(
                            left=Call(
                                func=Name(id='fibonacci', ctx=Load()),
                                args=[
                                    BinOp(
                                        left=Name(id='n', ctx=Load()),
                                        op=Sub(),
                                        right=Constant(value=2))],
                                keywords=[]),
                            op=Add(),
                            right=Call(
                                func=Name(id='fibonacci', ctx=Load()),
                                args=[
                                    BinOp(
                                        left=Name(id='n', ctx=Load()),
                                        op=Sub(),
                                        right=Constant(value=1))],
                                keywords=[])))],
                decorator_list=[],
                returns=Name(id='int', ctx=Load()))],
        type_ignores=[])