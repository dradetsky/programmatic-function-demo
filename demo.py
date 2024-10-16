import ast
from ast import (
    Module,
    arguments,

    Add,
    Mult,
    Load,
)
from functools import (
    partial,
)
from types import (
    FunctionType,
    CodeType,
)
# for use in a prog-defined method
import datetime

fake_line_col = {
    'lineno': 0,
    'end_lineno': 0,
    'col_offset': 0,
    'end_col_offset': 0,
}

# NOTE: Most of the elements of AST require a bunch of repetitive attributes
# (notably line numbers, which would normally be derived when parsing files of
# Python source), which if actually added to the expressions below would make
# them unreadable. So we curry those args in so the source can be read.
arg         = partial(ast.arg, **fake_line_col)
FunctionDef = partial(ast.FunctionDef, **fake_line_col)
Constant    = partial(ast.Constant, **fake_line_col)
BinOp       = partial(ast.BinOp, **fake_line_col)
Return      = partial(ast.Return, **fake_line_col)
Call        = partial(ast.Call, **fake_line_col)

Name      = partial(ast.Name, ctx=Load(), **fake_line_col)
Attribute = partial(ast.Attribute, ctx=Load(), **fake_line_col)


# === Argument lists ===
#
# def foobar(a, b):
f_args = arguments(
    args = [
        arg(arg='a'),
        arg(arg='b'),
    ],
    vararg=None, kwarg=None, defaults=[], kwonlyargs=[], kw_defaults=[],
)

# def foobar():
f_no_args = arguments(args=[], vararg=None, kwarg=None, defaults=[], kwonlyargs=[], kw_defaults=[])

# === Function bodies ===
#
# return 2*a+b
f_expr_body = Return(
    value=BinOp(
        left=BinOp(
            left=Constant(value=2),
            op=Mult(),
            right=Name(id='a')
        ),
        op=Add(),
        right=Name(id='b')
    ),
)

# return pow(a, 3)
f_bif_body = Return(
    value=Call(
        func=Name(id='pow'),
        args=[
            Name(id='a'),
            Constant(value=3),
        ],
        keywords=[],
    ),
)

# return g(a)
# where g is a user-defined function
f_udf_body = Return(
    value=Call(
        func=Name(id='g'),
        args=[
            Name(id='a'),
        ],
        keywords=[],
    ),
)

def g(x):
    return 5*x

f_libcall_body = Return(
    value=Call(
        func=Attribute(
            value=Attribute(
                value=Name(id='datetime'),
                attr='datetime'
            ),
            attr='now',
        ),
        args=[],
        keywords=[],
    ),
)

# NOTE:
#
# 1. The name value below is actually used in error messages, as in
#
#     TypeError: who_cares_wont_check_this() takes 0 positional arguments but 2 were given
#
# 2. It's necessary to pass in any referenced names you want to use besides the
#    built-in names. I'd call this `environment`, but the cpython codebase uses
#    the word `namespace` for whatever reason. Look, I just work here.
def make_fn(args, body, name='who_cares_wont_check_this', namespace={}):
    fn_ast = FunctionDef(
        name=name,
        args=args,
        body=[body],
        decorator_list=[]
    )
    mod_ast = Module(body=[fn_ast])
    mod_code = compile(mod_ast, '<not-a-real-file>', 'exec')
    # NOTE: copied this line; didn't take the time to understand it properly
    fn_code = [c for c in mod_code.co_consts if isinstance(c, CodeType)][0]

    fn = FunctionType(fn_code, namespace)
    return fn

def demo():
    f = make_fn(f_args, f_expr_body)
    print('f(a, b): 2*a+b')
    print(f(3,7))
    print(f(4,7))
    print(f(4,6))
    f = make_fn(f_args, f_bif_body)
    print('f(a, b): a**3')
    print(f(3,7))
    print(f(4,7))
    print(f(4,6))
    f = make_fn(f_args, f_udf_body, namespace=dict(g=g))
    print('f(a, b): g(a)')
    print(f(3,7))
    print(f(4,7))
    print(f(4,6))
    f = make_fn(f_no_args, f_libcall_body, namespace=dict(datetime=datetime))
    print('f(): datetime.datetime.now()')
    print(f())
    print(f())
    print(f())

if __name__ == '__main__':
    demo()
