"""This modules provides the DiscreteExpression class to provide
common methods for the discrete-time representations.

Copyright 2020 Michael Hayes, UCECE

"""

import numpy as np
from .expr import Expr

class DiscreteExpression(Expr):

    """Superclass of discrete-time, discrete-frequency, and z-domain
    expressions."""

    def __call__(self, arg, **assumptions):
        """Transform domain or substitute arg for variable. 
        
        Substitution is performed if arg is a tuple, list, numpy
        array, or constant.  If arg is a tuple or list return a list.
        If arg is an numpy array, return numpy array.

        Domain transformation is performed if arg is a domain variable
        or an expression of a domain variable.

        See also evaluate.

        """

        from .symbols import f, n, k, z, F, omega, Omega

        if isinstance(arg, (tuple, list)):
            return [self._subs1(self.var, arg1) for arg1 in arg]

        if isinstance(arg, np.ndarray):
            return np.array([self._subs1(self.var, arg1) for arg1 in arg])

        if id(arg) in (id(n), id(z), id(k), id(f), id(F), id(omega), id(Omega)):
            return self.transform(arg, **assumptions)

        if arg in (n, k, z, f, F, omega, Omega):
            return self.transform(arg, **assumptions)    

        # Do we really want to this?   
        return super(DiscreteExpression, self).__call__(arg, **assumptions)

    def transform(self, arg, **assumptions):

        from .symbols import f, n, k, z, F, omega, Omega        

        # Is this wise?   It makes sense for Voltage and Impedance objects
        # but may cause too much confusion for other expressions
        if arg is n and self.is_Z_domain:
            return self.IZT(**assumptions)
        elif arg is n and self.is_discrete_fourier_domain:
            return self.IDFT(**assumptions)
        elif arg is z and self.is_discrete_time_domain:
            return self.ZT(**assumptions)
        elif arg is z and self.is_discrete_fourier_domain:
            return self.IDFT(**assumptions).ZT(**assumptions)
        elif arg is k and self.is_discrete_time_domain:
            return self.DFT(**assumptions)
        elif arg is k and self.is_Z_domain:
            N = assumptions.pop('N', None)
            evaluate = assumptions.pop('evaluate', True)
            return self.IZT(**assumptions).DFT(N, evaluate)
        elif arg is f and (self.is_discrete_time_domain or self.is_Z_domain):
            return self.DTFT(**assumptions)
        elif arg is F and (self.is_discrete_time_domain or self.is_Z_domain):
            return self.DTFT(F, **assumptions)                
        elif arg is omega and (self.is_discrete_time_domain or self.is_Z_domain):
            return self.DTFT(omega, **assumptions)
        elif arg is Omega and (self.is_discrete_time_domain or self.is_Z_domain):
            return self.DTFT(Omega, **assumptions)

        raise ValueError('Unhandled transform')
        
        # Do we really want to this?   
        super(DiscreteExpression, self).transform(arg, **assumptions)
