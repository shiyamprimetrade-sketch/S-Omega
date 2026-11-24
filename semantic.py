"""Structural semantic verification for the pinned Alpha arithmetic subset."""
import ast
import keyword

OPS={ast.Add:"add",ast.Sub:"sub",ast.Mult:"mul",ast.Div:"div"}

def verify_source(spec, source):
    try:
        if not isinstance(source,bytes) or len(source)>16384:
            return False
        params=spec["parameters"]
        if not isinstance(params,list) or not 1<=len(params)<=8 or any(not isinstance(p,str) or not p.isascii() or not p.isidentifier() or keyword.iskeyword(p) or len(p)>64 for p in params) or len(set(params))!=len(params):
            return False
        tree=ast.parse(source.decode("utf-8"))
        if len(tree.body)!=1 or type(tree.body[0]) is not ast.FunctionDef:
            return False
        fn=tree.body[0]
        args=fn.args
        if fn.name!="compute" or fn.decorator_list or fn.returns or fn.type_comment or getattr(fn,"type_params",[]) or args.posonlyargs or args.kwonlyargs or args.vararg or args.kwarg or args.defaults or args.kw_defaults or any(a.annotation for a in args.args) or [a.arg for a in args.args]!=params or len(fn.body)!=1 or type(fn.body[0]) is not ast.Return:
            return False
        count=0
        def match(node,expr,depth=0):
            nonlocal count
            count+=1
            if depth>12 or count>127:
                return False
            if type(expr) is int and abs(expr)<=1000000:
                if expr<0:
                    return type(node) is ast.UnaryOp and type(node.op) is ast.USub and type(node.operand) is ast.Constant and type(node.operand.value) is int and node.operand.value==-expr
                return type(node) is ast.Constant and type(node.value) is int and node.value==expr
            if isinstance(expr,str):
                return expr in params and type(node) is ast.Name and node.id==expr
            if isinstance(expr,list) and len(expr)==3:
                return type(node) is ast.BinOp and type(node.op) in OPS and OPS[type(node.op)]==expr[0] and match(node.left,expr[1],depth+1) and match(node.right,expr[2],depth+1)
            return False
        return match(fn.body[0].value,spec["expression"])
    except (ValueError,TypeError,KeyError,SyntaxError,RecursionError,UnicodeError):
        return False
