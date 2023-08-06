"""This module contains functions for simplifying expressions.

Copyright 2020--2021 Michael Hayes, UCECE

"""

from sympy import Add, Mul, DiracDelta, Heaviside, Integral, oo, sin, cos, sqrt, atan2, pi, Symbol, solve, Min, Max
from .extrafunctions import UnitStep, UnitImpulse, rect, dtrect


def simplify_dirac_delta_product_term(expr):
    """ Simplify f(t) * DiracDelta(t) to f(0) * DiracDelta(t)."""

    if not expr.has(DiracDelta):
        return expr
    
    def query(expr):

        return expr.is_Mul and expr.has(DiracDelta)

    def value(expr):

        arg = None
        factors = expr.args
        dirac = None
        parts = []
        for factor in factors:
            if factor.is_Function and factor.func == DiracDelta:
                arg = factor.args[0]
                dirac = factor
            else:
                parts.append(factor)        

        if arg is None or not arg.has(Symbol):
            return expr
        results = solve(arg, dict=True)
        # Note, the eval method is called for functions.
        const = Mul(*parts).subs(results[0])
        return const * dirac

    return expr.replace(query, value)


def simplify_dirac_delta_product(expr, expand=False):
    """Simplify f(t) * DiracDelta(t) to f(0) * DiracDelta(t)."""

    if not expr.has(DiracDelta):
        return expr

    # Could also convert delta(a * t) to delta(t) / a
    
    if not expand:
        return simplify_dirac_delta_product_term(expr)
    
    terms = expr.expand().as_ordered_terms()

    return Add(*[simplify_dirac_delta_product_term(term) for term in terms])


def simplify_dirac_delta(expr, var=None):

    if not expr.has(DiracDelta):
        return expr
    
    expr = simplify_dirac_delta_product(expr)
    if var is not None:

        # Convert delta(a * t) to delta(t) / a
        expr = expr.expand(diracdelta=True, wrt=var)        
    return expr


# def simplify_heaviside_product(expr):
#
#     heaviside_products = []
#
#     def pre(expr):
#         if (expr.is_Mul and expr.args[0].func == Heaviside and
#               expr.args[1].func == Heaviside):
#             heaviside_products.append(expr)            
#        
#         for arg in expr.args:
#             pre(arg)    
#
#     pre(expr)
#            
#     for product in heaviside_products:
#         # TODO
#         pass
#
#     return expr


def simplify_power(expr):

    powers = []    
    
    def pre(expr):
        if (expr.is_Pow and expr.args[0].func in (Heaviside, UnitStep, rect, dtrect) and
            expr.args[1].is_constant):
            powers.append(expr)            
        
        for arg in expr.args:
            pre(arg)

    pre(expr)

    for power in powers:
        expr = expr.replace(power, power.args[0])            
    return expr


def simplify_heaviside_integral(expr):

    if not expr.has(Integral):
        return expr

    def query(expr):

        if not isinstance(expr, Integral):
            return False
        return expr.has(Heaviside) or expr.has(UnitStep)

    def value(expr):

        integrand = expr.args[0]
        var = expr.args[1][0]
        lower_limit = expr.args[1][1]
        upper_limit = expr.args[1][2]

        # Rewrite integral limits if Heaviside is a factor of the
        # integrand.

        result = 1
        for factor in integrand.as_ordered_factors():
            if isinstance(factor, (Heaviside, UnitStep)):
                arg = factor.args[0]
                if arg == var:
                    lower_limit = Max(lower_limit, 0)
                    factor = 1
                elif arg == -var:
                    upper_limit = Min(upper_limit, 0)
                    factor = 1
                elif (arg.is_Add and arg.args[1].is_Mul and
                      arg.args[1].args[0] == -1 and arg.args[1].args[1] == var):
                    upper_limit = Min(upper_limit, arg.args[0])
                    # Cannot remove Heaviside function in general.
                    
            result *= factor

        ret = Integral(result, (var, lower_limit, upper_limit))
        return ret
    
    expr = expr.replace(query, value)
    
    return expr


def simplify_heaviside_scale(expr, var):

    terms = expr.as_ordered_terms()
    if len(terms) > 1:
        result = 0
        for term in terms:
            result += simplify_heaviside_scale(term, var)
        return result

    def query(expr):

        return expr.is_Function and expr.func in (Heaviside, UnitStep)

    def value(expr):

        arg = expr.args[0]

        if not arg.as_poly(var).is_linear:
            return expr

        arg = arg.expand()
        a = arg.coeff(var, 1)
        b = arg.coeff(var, 0)
        if a == 0:
            return expr

        return expr.func(var + (b / a).cancel())
    
    return expr.replace(query, value)    


def simplify_heaviside(expr, var=None):

    if not expr.has(Heaviside) and not expr.has(UnitStep):
        return expr
    
    expr = simplify_heaviside_integral(expr)
    expr = simplify_power(expr)
    if var is not None:
        expr = simplify_heaviside_scale(expr, var)    
    return expr


def simplify_rect(expr, var=None):

    if not expr.has(rect) and not expr.has(dtrect):
        return expr

    expr = simplify_power(expr)    
    return expr

    
def simplify_sin_cos(expr, as_cos=False, as_sin=False):

    if not (expr.has(sin) and expr.has(cos)):
        return expr
    
    terms = expr.expand().as_ordered_terms()

    rest = 0
    cos_part = None
    sin_part = None    
    
    for term in terms:
        if term.has(sin) and sin_part is None:
            sin_part = term
        elif term.has(cos) and cos_part is None:
            cos_part = term
        else:
            rest += term

    if cos_part is None or sin_part is None:
        return expr

    cfactors = cos_part.expand().as_ordered_factors()
    sfactors = sin_part.expand().as_ordered_factors()

    commonfactors = []
    for factor in cfactors:
        if factor in sfactors:
            commonfactors.append(factor)

    for factor in commonfactors:
        sfactors.remove(factor)
        cfactors.remove(factor)

    cosfactor = None
    sinfactor = None    
    for cfactor in cfactors:
        if cfactor.has(cos):
            cosfactor = cfactor
            break
        
    for sfactor in sfactors:
        if sfactor.has(sin):
            sinfactor = sfactor
            break
        
    if cosfactor is None or sinfactor is None:
        return expr

    if cosfactor.args[0] != sinfactor.args[0]:
        return expr
        
    cfactors.remove(cosfactor)
    sfactors.remove(sinfactor)    

    c = Mul(*cfactors)
    s = Mul(*sfactors)
    A = sqrt(c * c + s * s) * Mul(*commonfactors)
    phi = atan2(s, c)

    if as_sin:
        return rest + A * sin(cosfactor.args[0] - phi + pi / 2, evaluate=False)

    if as_cos:
        return rest + A * cos(cosfactor.args[0] - phi, evaluate=False)

    # SymPy will choose sin or cos as convenient.
    return rest + A * cos(cosfactor.args[0] - phi)


def simplify_unit_impulse(expr, var=None):

    if not expr.has(UnitImpulse):
        return expr

    def query(expr):

        return expr.is_Function and expr.func is UnitImpulse

    def value(expr):

        arg = expr.args[0]

        if not arg.as_poly(var).is_linear:
            return expr

        arg = arg.expand()
        a = arg.coeff(var, 1)
        b = arg.coeff(var, 0)
        if a == 0:
            return expr

        return expr.func(var + (b / a).cancel())
    
    return expr.replace(query, value)        
