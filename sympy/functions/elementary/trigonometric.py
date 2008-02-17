
from sympy.core.basic import Basic, S, C, sympify
from sympy.core.function import Lambda, Function
from miscellaneous import sqrt
from sympy.core.cache import cacheit

###############################################################################
########################## TRIGONOMETRIC FUNCTIONS ############################
###############################################################################

class sin(Function):

    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return cos(self.args[0])
        else:
            raise ArgumentIndexError(self, argindex)

    def inverse(self, argindex=1):
        return asin

    @classmethod
    def _eval_apply_subs(self, *args):
        return

    @classmethod
    def canonize(cls, arg):
        arg = sympify(arg)

        if isinstance(arg, C.Number):
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Zero:
                return S.Zero
            elif arg.is_negative:
                return -cls(-arg)
        else:
            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return S.ImaginaryUnit * C.sinh(i_coeff)
            else:
                pi_coeff = arg.as_coefficient(S.Pi)

                if pi_coeff is not None:
                    if pi_coeff.is_integer:
                        return S.Zero
                    elif isinstance(pi_coeff, C.Rational):
                        cst_table = {
                            2 : S.One,
                            3 : S.Half*sqrt(3),
                            4 : S.Half*sqrt(2),
                            6 : S.Half,
                        }

                        try:
                            result = cst_table[pi_coeff.q]

                            if (pi_coeff.p // pi_coeff.q) % 2 == 1:
                                return -result
                            else:
                                return result
                        except KeyError:
                            pass

                coeff, terms = arg.as_coeff_terms()

                if coeff.is_negative:
                    return -cls(-arg)


    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)

            if len(previous_terms) > 2:
                p = previous_terms[-2]
                return -p * x**2 / (n*(n-1))
            else:
                return (-1)**(n//2) * x**(n)/C.Factorial(n)

    def _eval_rewrite_as_exp(self, arg):
        exp, I = C.exp, S.ImaginaryUnit
        return (exp(arg*I) - exp(-arg*I)) / (2*I)

    def _eval_rewrite_as_cos(self, arg):
        return -cos(arg + S.Pi/2)

    def _eval_rewrite_as_tan(self, arg):
        tan_half = tan(S.Half*arg)
        return 2*tan_half/(1 + tan_half**2)

    def _eval_rewrite_as_cot(self, arg):
        cot_half = S.Cot(S.Half*arg)
        return 2*cot_half/(1 + cot_half**2)

    def _eval_conjugate(self):
        return self.func(self.args[0].conjugate())

    def _eval_expand_complex(self, *args):
        if self.args[0].is_real:
            return self
        re, im = self.args[0].as_real_imag()
        return sin(re)*C.cosh(im) + S.ImaginaryUnit*cos(re)*C.sinh(im)

    def _eval_expand_trig(self, *args):
        arg = self.args[0].expand()
        x = None
        if isinstance(arg, C.Add):
            x = arg.args[0]
            y = C.Add(*arg.args[1:])
        else:
            coeff, terms = arg.as_coeff_terms()
            if not (coeff is S.One) and isinstance(coeff, C.Integer) and terms:
                x = C.Mul(*terms)
                y = (coeff-1)*x
        if x is not None:
            return (sin(x)*cos(y) + sin(y)*cos(x)).expand(trig=True)
        return sin(arg)

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if C.Order(1,x).contains(arg):
            return arg
        else:
            return self.func(arg)

    def _eval_is_real(self):
        return self.args[0].is_real

    def _eval_is_bounded(self):
        arg = self.args[0]
        if arg.is_real:
            return True

    def _sage_(self):
        import sage.all as sage
        return sage.sin(self.args[0]._sage_())

class cos(Function):

    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return -sin(self.args[0])
        else:
            raise ArgumentIndexError(self, argindex)

    def inverse(self, argindex=1):
        return acos

    @classmethod
    def _eval_apply_subs(self, *args):
        return

    @classmethod
    def canonize(cls, arg):
        arg = sympify(arg)

        if isinstance(arg, C.Number):
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Zero:
                return S.One
            elif arg.is_negative:
                return cls(-arg)
        else:
            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return C.cosh(i_coeff)
            else:
                pi_coeff = arg.as_coefficient(S.Pi)

                if pi_coeff is not None:
                    if isinstance(pi_coeff, C.Rational):
                        cst_table = {
                            1 : S.One,
                            2 : S.Zero,
                            3 : S.Half,
                            4 : S.Half*sqrt(2),
                            6 : S.Half*sqrt(3),
                        }

                        try:
                            result = cst_table[pi_coeff.q]

                            if (2*pi_coeff.p // pi_coeff.q) % 4 in (1, 2):
                                return -result
                            else:
                                return result
                        except KeyError:
                            pass

                coeff, terms = arg.as_coeff_terms()

                if coeff.is_negative:
                    return cls(-arg)


    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n < 0 or n % 2 == 1:
            return S.Zero
        else:
            x = sympify(x)

            if len(previous_terms) > 2:
                p = previous_terms[-2]
                return -p * x**2 / (n*(n-1))
            else:
                return (-1)**(n//2)*x**(n)/C.Factorial(n)

    def _eval_rewrite_as_exp(self, arg):
        exp, I = C.exp, S.ImaginaryUnit
        return (exp(arg*I) + exp(-arg*I)) / 2

    def _eval_rewrite_as_sin(self, arg):
        return sin(arg + S.Pi/2)

    def _eval_rewrite_as_tan(self, arg):
        tan_half = tan(S.Half*arg)**2
        return (1-tan_half)/(1+tan_half)

    def _eval_rewrite_as_cot(self, arg):
        cot_half = S.Cot(S.Half*arg)**2
        return (cot_half-1)/(cot_half+1)

    def _eval_conjugate(self):
        return self.func(self.args[0].conjugate())

    def _eval_expand_complex(self, *args):
        if self.args[0].is_real:
            return self
        re, im = self.args[0].as_real_imag()
        return cos(re)*C.cosh(im) - \
            S.ImaginaryUnit*sin(re)*C.sinh(im)

    def _eval_expand_trig(self, *args):
        arg = self.args[0].expand()
        x = None
        if isinstance(arg, C.Add):
            x = arg.args[0]
            y = C.Add(*arg.args[1:])
            return (cos(x)*cos(y) - sin(y)*sin(x)).expand(trig=True)
        else:
            coeff, terms = arg.as_coeff_terms()
            if not (coeff is S.One) and isinstance(coeff, C.Integer) and terms:
                x = C.Mul(*terms)
                return C.chebyshevt(coeff, cos(x))
        return cos(arg)

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if C.Order(1,x).contains(arg):
            return S.One
        else:
            return self.func(arg)

    def _eval_is_real(self):
        return self.args[0].is_real

    def _eval_is_bounded(self):
        arg = self.args[0]

        if arg.is_real:
            return True

    def _sage_(self):
        import sage.all as sage
        return sage.cos(self.args[0]._sage_())

class tan(Function):

    nargs = 1

    def fdiff(self, argindex=1):
        if argindex==1:
            return S.One + self**2
        else:
            raise ArgumentIndexError(self, argindex)

    def inverse(self, argindex=1):
        return atan

    @classmethod
    def _eval_apply_subs(self, *args):
        return

    @classmethod
    def canonize(cls, arg):
        arg = sympify(arg)

        if isinstance(arg, C.Number):
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Zero:
                return S.Zero
            elif arg.is_negative:
                return -cls(-arg)
        else:
            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return S.ImaginaryUnit * C.tanh(i_coeff)
            else:
                pi_coeff = arg.as_coefficient(S.Pi)

                if pi_coeff is not None:
                    if pi_coeff.is_integer:
                        return S.Zero
                    elif isinstance(pi_coeff, C.Rational):
                        cst_table = {
                           #2 : S.ComplexInfinity,
                            3 : sqrt(3),
                            4 : S.One,
                            6 : 1 / sqrt(3),
                        }

                        try:
                            result = cst_table[pi_coeff.q]

                            if (2*pi_coeff.p // pi_coeff.q) % 4 in (1, 3):
                                return -result
                            else:
                                return result
                        except KeyError:
                            pass

                coeff, terms = arg.as_coeff_terms()

                if coeff.is_negative:
                    return -cls(-arg)


    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)

            a, b = ((n-1)//2), 2**(n+1)

            B = C.bernoulli(n+1)
            F = C.Factorial(n+1)

            return (-1)**a * b*(b-1) * B/F * x**n

    def _eval_conjugate(self):
        return self.func(self.args[0].conjugate())

    def _eval_expand_complex(self, *args):
        if self.args[0].is_real:
            return self
        re, im = self.args[0].as_real_imag()
        denom = cos(re)**2 + C.sinh(im)**2
        return (sin(re)*cos(re) + \
            S.ImaginaryUnit*C.sinh(im)*C.cosh(im))/denom

    def _eval_expand_trig(self, *args):
        return self

    def _eval_rewrite_as_exp(self, arg):
        exp, I = C.exp, S.ImaginaryUnit
        neg_exp, pos_exp = exp(-arg*I), exp(arg*I)
        return I*(neg_exp-pos_exp)/(neg_exp+pos_exp)

    def _eval_rewrite_as_sin(self, arg):
        return 2*sin(x)**2/sin(2*x)

    def _eval_rewrite_as_cos(self, arg):
        return -cos(x + S.Pi/2)/cos(x)

    def _eval_rewrite_as_cot(self, arg):
        return 1/S.Cot(arg)

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if C.Order(1,x).contains(arg):
            return S.One
        else:
            return self.func(arg)

    def _eval_is_real(self):
        return self.args[0].is_real

    def _eval_is_bounded(self):
        arg = self.args[0]

        if arg.is_imaginary:
            return True

class cot(Function):

    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return -S.One - S.Cot**2
        else:
            raise ArgumentIndexError(self, argindex)

    def inverse(self, argindex=1):
        return S.ACot

    @classmethod
    def _eval_apply_subs(self, *args):
        return

    @classmethod
    def canonize(cls, arg):
        arg = sympify(arg)

        if isinstance(arg, C.Number):
            if arg is S.NaN:
                return S.NaN
            #elif arg is S.Zero:
            #    return S.ComplexInfinity
            elif arg.is_negative:
                return -cls(-arg)
        else:
            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return -S.ImaginaryUnit * C.coth(i_coeff)
            else:
                pi_coeff = arg.as_coefficient(S.Pi)

                if pi_coeff is not None:
                    #if pi_coeff.is_integer:
                    #    return S.ComplexInfinity
                    if isinstance(pi_coeff, C.Rational):
                        cst_table = {
                            2 : S.Zero,
                            3 : 1 / sqrt(3),
                            4 : S.One,
                            6 : sqrt(3)
                        }

                        try:
                            result = cst_table[pi_coeff.q]

                            if (2*pi_coeff.p // pi_coeff.q) % 4 in (1, 3):
                                return -result
                            else:
                                return result
                        except KeyError:
                            pass

                coeff, terms = arg.as_coeff_terms()

                if coeff.is_negative:
                    return -cls(-arg)


    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n == 0:
            return 1 / sympify(x)
        elif n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)

            B = S.Bernoulli(n+1)
            F = C.Factorial(n+1)

            return (-1)**((n+1)//2) * 2**(n+1) * B/F * x**n

    def _eval_conjugate(self):
        assert len(self.args) == 1
        return self.func(self.args[0].conjugate())

    def _eval_expand_complex(self, *args):
        if self.args[0].is_real:
            return self
        re, im = self.args[0].as_real_imag()
        denom = sin(re)**2 + C.sinh(im)**2
        return (sin(re)*cos(re) - \
            S.ImaginaryUnit*C.sinh(im)*C.cosh(im))/denom

    def _eval_rewrite_as_exp(self, arg):
        exp, I = C.exp, S.ImaginaryUnit
        neg_exp, pos_exp = exp(-arg*I), exp(arg*I)
        return I*(pos_exp+neg_exp)/(pos_exp-neg_exp)

    def _eval_rewrite_as_sin(self, arg):
        return 2*sin(2*x)/sin(x)**2

    def _eval_rewrite_as_cos(self, arg):
        return -cos(x)/cos(x + S.Pi/2)

    def _eval_rewrite_as_tan(self, arg):
        return 1/tan(arg)

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if C.Order(1,x).contains(arg):
            return S.One
        else:
            return self.func(arg)

    def _eval_is_real(self):
        return self.args[0].is_real

###############################################################################
########################### TRIGONOMETRIC INVERSES ############################
###############################################################################

class asin(Function):

    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return (1 - self.args[0]**2)**(-S.Half)
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def _eval_apply_subs(self, *args):
        return

    @classmethod
    def canonize(cls, arg):
        arg = sympify(arg)

        if isinstance(arg, C.Number):
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.NegativeInfinity * S.ImaginaryUnit
            elif arg is S.NegativeInfinity:
                return S.Infinity * S.ImaginaryUnit
            elif arg is S.Zero:
                return S.Zero
            elif arg is S.One:
                return S.Pi / 2
            elif arg is S.NegativeOne:
                return -S.Pi / 2
            else:
                cst_table = {
                    S.Half       : 6,
                    -S.Half      : -6,
                    sqrt(2)/2  : 4,
                    -sqrt(2)/2 : -4,
                    1/sqrt(2)  : 4,
                    -1/sqrt(2) : -4,
                    sqrt(3)/2  : 3,
                    -sqrt(3)/2 : -3,
                }

                if arg in cst_table:
                    return S.Pi / cst_table[arg]
                elif arg.is_negative:
                    return -cls(-arg)
        else:
            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return S.ImaginaryUnit * C.asinh(i_coeff)
            else:
                coeff, terms = arg.as_coeff_terms()

                if coeff.is_negative:
                    return -cls(-arg)


    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)

            if len(previous_terms) > 2:
                p = previous_terms[-2]
                return p * (n-2)**2/(k*(k-1)) * x**2
            else:
                k = (n - 1) // 2

                R = C.RisingFactorial(S.Half, k)
                F = C.Factorial(k)

                return R / F * x**n / n

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if C.Order(1,x).contains(arg):
            return arg
        else:
            return self.func(arg)

    def _eval_is_real(self):
	return self.args[0].is_real and (self.args[0]>=-1 and self.args[0]<=1)

class acos(Function):

    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return -(1 - self.args[0]**2)**(-S.Half)
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def _eval_apply_subs(self, *args):
        return

    @classmethod
    def canonize(cls, arg):
        arg = sympify(arg)

        if isinstance(arg, C.Number):
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.Infinity * S.ImaginaryUnit
            elif arg is S.NegativeInfinity:
                return S.NegativeInfinity * S.ImaginaryUnit
            elif arg is S.Zero:
                return S.Pi / 2
            elif arg is S.One:
                return S.Zero
            elif arg is S.NegativeOne:
                return S.Pi
            else:
                cst_table = {
                    S.Half       : S.Pi/3,
                    -S.Half      : 2*S.Pi/3,
                    sqrt(2)/2  : S.Pi/4,
                    -sqrt(2)/2 : 3*S.Pi/4,
                    1/sqrt(2)  : S.Pi/4,
                    -1/sqrt(2) : 3*S.Pi/4,
                    sqrt(3)/2  : S.Pi/6,
                    -sqrt(3)/2 : 5*S.Pi/6,
                }

                if arg in cst_table:
                    return cst_table[arg]


    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n == 0:
            return S.Pi / 2
        elif n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)

            if len(previous_terms) > 2:
                p = previous_terms[-2]
                return p * (n-2)**2/(k*(k-1)) * x**2
            else:
                k = (n - 1) // 2

                R = C.RisingFactorial(S.Half, k)
                F = C.Factorial(k)

                return -R / F * x**n / n

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if C.Order(1,x).contains(arg):
            return arg
        else:
            return self.func(arg)

    def _eval_is_real(self):
	return self.args[0].is_real and (self.args[0]>=-1 and self.args[0]<=1)

class atan(Function):

    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return 1/(1+self.args[0]**2)
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def _eval_apply_subs(self, *args):
        return

    @classmethod
    def canonize(cls, arg):
        arg = sympify(arg)

        if isinstance(arg, C.Number):
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.Pi / 2
            elif arg is S.NegativeInfinity:
                return -S.Pi / 2
            elif arg is S.Zero:
                return S.Zero
            elif arg is S.One:
                return S.Pi / 4
            elif arg is S.NegativeOne:
                return -S.Pi / 4
            else:
                cst_table = {
                    sqrt(3)/3  : 6,
                    -sqrt(3)/3 : -6,
                    1/sqrt(3)  : 6,
                    -1/sqrt(3) : -6,
                    sqrt(3)    : 3,
                    -sqrt(3)   : -3,
                }

                if arg in cst_table:
                    return S.Pi / cst_table[arg]
                elif arg.is_negative:
                    return -cls(-arg)
        else:
            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return S.ImaginaryUnit * C.atanh(i_coeff)
            else:
                coeff, terms = arg.as_coeff_terms()

                if coeff.is_negative:
                    return -cls(-arg)


    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)
            return (-1)**((n-1)//2) * x**n / n

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if C.Order(1,x).contains(arg):
            return arg
        else:
            return self.func(arg)

    def _eval_is_real(self):
        return self.args[0].is_real

class acot(Function):

    nargs = 1

    def fdiff(self, argindex=1):
        if argindex == 1:
            return -1 / (1+self.args[0]**2)
        else:
            raise ArgumentIndexError(self, argindex)

    @classmethod
    def canonize(cls, arg):
        arg = sympify(arg)

        if isinstance(arg, C.Number):
            if arg is S.NaN:
                return S.NaN
            elif arg is S.Infinity:
                return S.Zero
            elif arg is S.NegativeInfinity:
                return S.Zero
            elif arg is S.Zero:
                return S.Pi/ 2
            elif arg is S.One:
                return S.Pi / 4
            elif arg is S.NegativeOne:
                return -S.Pi / 4
            else:
                cst_table = {
                    sqrt(3)/3  : 3,
                    -sqrt(3)/3 : -3,
                    1/sqrt(3)  : 3,
                    -1/sqrt(3) : -3,
                    sqrt(3)    : 6,
                    -sqrt(3)   : -6,
                }

                if arg in cst_table:
                    return S.Pi / cst_table[arg]
                elif arg.is_negative:
                    return -cls(-arg)
        else:
            i_coeff = arg.as_coefficient(S.ImaginaryUnit)

            if i_coeff is not None:
                return -S.ImaginaryUnit * C.acoth(i_coeff)
            else:
                coeff, terms = arg.as_coeff_terms()

                if coeff.is_negative:
                    return -cls(-arg)


    @staticmethod
    @cacheit
    def taylor_term(n, x, *previous_terms):
        if n == 0:
            return S.Pi / 2 # FIX THIS
        elif n < 0 or n % 2 == 0:
            return S.Zero
        else:
            x = sympify(x)
            return (-1)**((n+1)//2) * x**n / n

    def _eval_as_leading_term(self, x):
        arg = self.args[0].as_leading_term(x)

        if C.Order(1,x).contains(arg):
            return arg
        else:
            return self.func(arg)

    def _eval_is_real(self):
        return self.args[0].is_real

class atan2(Function):
    """
    Returns the atan(y/x) taking two arguments y and x. Signs of
    both y and x are considered to determine the appropriate 
    quadrant of atan(y/x). The range is (-pi, pi].
    """
    
    nargs = 2
    
    @classmethod
    def canonize(cls, y, x):
        x, y = sympify(x), sympify(y)
        sign_y = C.sign(y)

        if y.is_zero:
            if x.is_positive:
                return S.Zero
            elif x.is_zero:
                return S.NaN
            elif x.is_negative:
                return S.Pi
        elif x.is_zero:
            if isinstance(sign_y, C.Number):
                return sign_y * S.Pi/2
        else:
            abs_yx = C.abs(y/x)
            if isinstance(sign_y, C.Number) and abs_yx.is_number: 
                phi = C.atan(abs_yx)
                if x.is_positive:
                    return sign_y * phi
                else:
                    return sign_y * (S.Pi - phi)

    def _eval_is_real(self):
        return self.args[0].is_real and self.args[1].is_real
