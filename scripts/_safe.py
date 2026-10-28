"""Safe expression evaluation shared by the everythingmath checkers (standard library only).

Expressions are parsed with `ast`, validated against a whitelist, and evaluated with no builtins.
`^` is accepted as power. Implicit multiplication is not supported: write 2*x, not 2x.
"""
import ast
import math
import random
from fractions import Fraction

MAX_POW_DIGITS = 20000


def _pow(a, b):
    if isinstance(b, (int, Fraction)) and not isinstance(b, bool):
        if abs(b) > 100000:
            raise ValueError("exponent too large")
        if isinstance(a, int) and isinstance(b, int) and b > 0 and abs(a) > 1:
            if b * math.log10(abs(a)) > MAX_POW_DIGITS:
                raise ValueError("result too large")
    r = a ** b
    if isinstance(r, complex):
        raise ValueError("complex result")
    return r


def _is_prime(n):
    n = int(n)
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _factor(n):
    n = int(n)
    out, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def _tau(n):
    r = 1
    for e in _factor(n).values():
        r *= e + 1
    return r


def _sigma(n):
    r = 1
    for p, e in _factor(n).items():
        r *= (p ** (e + 1) - 1) // (p - 1)
    return r


def _phi(n):
    r = int(n)
    for p in _factor(n):
        r = r // p * (p - 1)
    return r


def _is_square(n):
    n = int(n)
    return n >= 0 and math.isqrt(n) ** 2 == n


def _sign(x):
    return (x > 0) - (x < 0)


def _cbrt(x):
    return math.copysign(abs(x) ** (1.0 / 3.0), x)


def _digits(n, base):
    n = abs(int(n))
    out = ""
    while n:
        out = "0123456789abcdefghijklmnopqrstuvwxyz"[n % base] + out
        n //= base
    return out or "0"


INT_FUNCS = {
    "abs": abs, "min": min, "max": max, "gcd": math.gcd, "isqrt": math.isqrt,
    "comb": math.comb, "binom": math.comb, "perm": math.perm, "factorial": math.factorial,
    "is_prime": _is_prime, "is_square": _is_square, "tau": _tau, "sigma": _sigma, "phi": _phi,
    "lcm": lambda a, b: abs(a * b) // math.gcd(a, b) if a and b else 0,
    "digsum": lambda n, base=10: sum(int(c, 36) for c in _digits(n, base)),
}

FLOAT_FUNCS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos,
    "atan": math.atan, "atan2": math.atan2, "arcsin": math.asin, "arccos": math.acos,
    "arctan": math.atan, "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
    "asinh": math.asinh, "acosh": math.acosh, "atanh": math.atanh, "exp": math.exp,
    "log": math.log, "ln": math.log, "log2": math.log2, "log10": math.log10, "sqrt": math.sqrt,
    "cbrt": _cbrt, "floor": math.floor, "ceil": math.ceil, "gamma": math.gamma,
    "lgamma": math.lgamma, "erf": math.erf, "abs": abs, "min": min, "max": max, "sign": _sign,
    "sec": lambda x: 1 / math.cos(x), "csc": lambda x: 1 / math.sin(x),
    "cot": lambda x: 1 / math.tan(x), "hypot": math.hypot,
    "comb": math.comb, "binom": math.comb, "factorial": math.factorial, "gcd": math.gcd,
}

CONSTS = {"pi": math.pi, "e": math.e, "tau": math.tau, "inf": math.inf}


def _int_wrap(f):
    def g(*a):
        return f(*[int(x) if isinstance(x, Fraction) and x.denominator == 1 else x for x in a])
    return g


EXACT_FUNCS = {k: _int_wrap(v) for k, v in INT_FUNCS.items()}
EXACT_FUNCS.update({"floor": math.floor, "ceil": math.ceil})

_ALLOWED = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare, ast.Call, ast.Name,
    ast.Constant, ast.Load, ast.IfExp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.USub, ast.UAdd, ast.Not, ast.And, ast.Or, ast.Eq, ast.NotEq,
    ast.Lt, ast.LtE, ast.Gt, ast.GtE,
)


class _Rewrite(ast.NodeTransformer):
    def __init__(self, exact):
        self.exact = exact

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.Pow):
            return ast.copy_location(
                ast.Call(func=ast.Name("_pow", ast.Load()), args=[node.left, node.right], keywords=[]), node)
        return node

    def visit_Constant(self, node):
        if self.exact and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return ast.copy_location(
                ast.Call(func=ast.Name("_F", ast.Load()), args=[ast.Constant(repr(node.value))], keywords=[]), node)
        return node


def parse(src, names, mode="float"):
    """Validate and compile `src`. Returns f(env) -> value. `mode` is float, int or exact."""
    funcs = {"float": FLOAT_FUNCS, "int": INT_FUNCS, "exact": EXACT_FUNCS}[mode]
    consts = CONSTS if mode == "float" else {}
    try:
        tree = ast.parse(src.strip().replace("^", "**"), mode="eval")
    except SyntaxError as exc:
        raise ValueError("cannot parse %r: %s" % (src, exc.msg))
    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED):
            raise ValueError("%s is not allowed in expressions" % type(node).__name__)
        if isinstance(node, ast.Name) and node.id not in names and node.id not in consts \
                and node.id not in funcs and node.id not in ("True", "False"):
            raise ValueError("unknown name %r (variables: %s)" % (node.id, ", ".join(sorted(names)) or "none"))
        if isinstance(node, ast.Call) and not (isinstance(node.func, ast.Name) and node.func.id in funcs):
            raise ValueError("unknown function in %r" % src)
    tree = ast.fix_missing_locations(_Rewrite(mode == "exact").visit(tree))
    code = compile(tree, "<expr>", "eval")
    base = dict(funcs)
    base.update(consts)
    base["_pow"] = _pow
    base["_F"] = Fraction

    def run(env):
        scope = dict(base)
        scope.update(env)
        return eval(code, {"__builtins__": {}}, scope)
    return run


def used_names(src):
    """Names that appear in an expression (variables, constants and function names)."""
    tree = ast.parse(src.strip().replace("^", "**"), mode="eval")
    return {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}


def parse_vars(spec):
    """'x:-5:5,y:0:3' -> {'x': (-5.0, 5.0), 'y': (0.0, 3.0)}"""
    out = {}
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        bits = part.split(":")
        if len(bits) != 3:
            raise ValueError("variable spec must look like x:lo:hi, got %r" % part)
        out[bits[0]] = (float(bits[1]), float(bits[2]))
    return out


def sample_points(ranges, n, seed=1):
    rng = random.Random(seed)
    pts = []
    for i in range(n):
        p = {}
        for nm, (lo, hi) in ranges.items():
            if i == 0:
                p[nm] = lo + 0.5 * (hi - lo)
            elif i == 1:
                p[nm] = lo + 1e-3 * (hi - lo)
            elif i == 2:
                p[nm] = hi - 1e-3 * (hi - lo)
            else:
                p[nm] = rng.uniform(lo, hi)
        pts.append(p)
    return pts


UNDEFINED = (ValueError, ZeroDivisionError, OverflowError, TypeError)


def close(a, b, tol):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
