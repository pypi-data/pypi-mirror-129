# -*- coding: utf-8  -*-

def floating_point_numbers_retain_decimal_digit(x, decimal_digit=2):
    dd = decimal_digit
    a = 10 ** dd * x
    a = int(a)
    a /= 10 ** dd
    return a
def floatdd(x, decimal_digit=2):
    return floating_point_numbers_retain_decimal_digit(x, decimal_digit)

def fibo(num=None, found=None, to=None):
    if num != None:
        fib = [1]
        for x in range(0, num):
            try:
                fib[-2]
            except IndexError:
                fib.append(1)
                continue
            fib.append(fib[-1] + fib[-2])
        return fib[num]
    elif found != None:
        fib = [1]
        if type(found) != type(1):
            raise TypeError('\'found\' must be int')
        while True:
            if fib[-1] > found:
                fib.append(False)
                break
            elif fib[-1] == found:
                fib.append(True)
                break
            try:
                fib[-2]
            except IndexError:
                fib.append(1)
                continue
            fib.append(fib[-1] + fib[-2])
        return fib[-1]
    elif to != None:
        fib = [1]
        for x in range(0, to):
            try:
                fib[-2]
            except IndexError:
                fib.append(1)
                continue
            fib.append(fib[-1] + fib[-2])
        return fib

def arithmetic_sequence(result_type, sequence=None, first=None, last=None, number_of_items=None, common_difference=None):
    if result_type == 'all':
        if type(sequence) == type(''):
            lst = []
            for x in sequence:
                lst.append(int(x))
            s = sum(lst)
            cd = int(sequence[1]) - int(sequence[0])
            return {
                'sequence' : sequence,
                'first' : int(sequence[0]),
                'last' : int(sequence[-1]),
                'number of items' : len(sequence),
                'common difference' : cd,
                'sum' : s
                }
        elif type(sequence) == type([]):
            cd = sequence[1] - sequence[0]
            return {
                'sequence' : sequence,
                'first' : sequence[0],
                'last' : sequence[-1],
                'number of items' : len(sequence),
                'common difference' : cd,
                'sum' : sum(sequence)
                }
        else:
            raise TypeError('\'sequence\' must be a list type or a string type')
    elif result_type == 'output':
        if first != None:
            output = [first]
            for x in range(1, number_of_items):
                output.append(output[-1] + common_difference)
        else:
            output = [last]
            for x in range(1, number_of_items):
                output.append(output[-1] - common_difference)
            output = output[::-1]
        return output
    elif result_type == 'first':
        return arithmetic_sequence('output', first, last, number_of_items, common_difference)[0]
    elif result_type == 'last':
        return arithmetic_sequence('output', first, last, number_of_items, common_difference)[-1]
    elif result_type == 'number_of_items' or result_type == 'number of items':
        output = [first]
        while output[-1] < last:
            output.append(output[-1] + common_difference)
        return len(output)
    elif result_type == 'common_difference' or result_type == 'common difference':
        return arithmetic_sequence('output', first, last, number_of_items, common_difference)[1] - arithmetic_sequence('output', first, last, number_of_items, common_difference)[0]
    elif result_type == 'sum':
        return sum(arithmetic_sequence('output', first, last, number_of_items, common_difference))

from math import *
import cmath as c

def math(mode='+', a=0, b=0):
    if a == 'pi':
        a = pi
    if b == 'pi':
        b = pi
    # pi
    if a == 'e':
        a = e
    if b == 'e':
        b = e
    # e
    if a == 'tau':
        a = tau
    if b == 'tau':
        b = tau
    # tau
    if a == 'inf':
        a = float('inf')
    if b == 'inf':
        b = float('inf')
    # inf
    if a == '-inf':
        a = float('-inf')
    if b == '-inf':
        b = float('-inf')
    # -inf
    if a == 'nan' or a == 'NaN':
        a = nan
    if b == 'nan' or b == 'NaN':
        b = nan
    # nan
    if mode == '+':
        result = a + b
    elif mode == '-':
        result = a - b
    elif mode == '*':
        result = a * b
    elif mode == '/':
        result = a / b
    elif mode == '//':
        result = a // b
    elif mode == '...':
        result = a % b
    elif mode == '%':
        result = a % b
    # Operations
    elif mode == '>':
        if a > b:
            result = True
        else:
            result = False
    elif mode == '<':
        if a < b:
            result = True
        else:
            result = False
    elif mode == '==':
        if a == b:
            result = True
        else:
            result = False
    elif mode == '!=':
        if a != b:
            result = True
        else:
            result = False
    elif mode == '>=':
        if a >= b:
            result = True
        else:
            result = False
    elif mode == '<=':
        if a <= b:
            result = True
        else:
            result = False
        # Compare
    elif mode == '!':
        x = 1
        for y in range(1, a + 1):
            x = x * y
        result = x
    elif mode == '^':
        result = a ** b
    elif mode == 'square root':
        result = sqrt(a)
    elif mode == 'sqrt()':
        result = sqrt(a)
    # Power
    elif mode == 'exp()':
        result = exp(a)
    elif mode == 'exp1()':
        result = exp1(a)
    # Power And Logarithmic Functions
    elif mode == 'cos()':
        result = cos(a)
    elif mode == 'tan()':
        result = tan(a)
    elif mode == 'sin()':
        result = sin(a)
    elif mode == 'acos()':
        result = acos(a)
    elif mode == 'atan()':
        result = atan(a)
    elif mode == 'asin()':
        result = asin(a)
    elif mode == 'dist()':
        result = dist(a)
    elif mode == 'hypot()':
        result = hypot(a)
    # Trigonometric Function
    elif mode == 'cosh()':
        result = cosh(a)
    elif mode == 'tanh()':
        result = tanh(a)
    elif mode == 'sinh()':
        result = sinh(a)
    elif mode == 'acosh()':
        result = acosh(a)
    elif mode == 'atanh()':
        result = atanh(a)
    elif mode == 'asinh()':
        result = asinh(a)
    # Hyperbolic Functions
    elif mode == 'Degrees()':
        result = degrees(a)
    elif mode == 'degrees()':
        result = degrees(a)
    elif mode == 'Radians()':
        result = radians(a)
    elif mode == 'radians()':
        result = radians(a)
    # Angular Conversion
    elif mode == 'abs()':
        result = abs(a)
        # Else
    elif mode == 'Int / Float':
        if type(a) == type(1):
            result = float(a)
        elif type(a) == type(1.5):
            result = int(a)
        else:
            raise TypeError(''' 'Int / Float' object's argument must be int or float ''')
    elif mode == 'int / float':
        if type(a) == type(1):
            result = float(a)
        elif type(a) == type(1.5):
            result = int(a)
        else:
            raise TypeError(''' 'Int / Float' object's argument must be int or float ''')
    elif mode == 'Type':
        result = type(a)
    elif mode == 'type':
        result = type(a)
    # Type
    else:
        raise AttributeError(''' 'run' object has no attribute '%s' ''' % mode)
    return result

def cmath(mode, a, b):
    if a == 'pi':
        a = c.pi
    if b == 'pi':
        b = c.pi
    # pi
    if a == 'e':
        a = c.e
    if b == 'e':
        b = c.e
    # e
    if a == 'tau':
        a = c.tau
    if b == 'tau':
        b = c.tau
    # tau
    if a == 'inf':
        a = float('inf')
    if b == 'inf':
        b = float('inf')
    # inf
    if a == '-inf':
        a = float('-inf')
    if b == '-inf':
        b = float('-inf')
    # -inf
    if a == 'nan' or a == 'NaN':
        a = c.nan
    if b == 'nan' or b == 'NaN':
        b = c.nan
    # nan
    if mode == 'cos()':
            return c.cos(a)
    elif mode == 'tan()':
            return c.tan(a)
    elif mode == 'sin()':
            return c.sin(a)
    elif mode == 'acos()':
            return c.cos(a)
    elif mode == 'atan()':
            return c.tan(a)
    elif mode == 'asin()':
            return c.sin(a)
        # Trigonometric Function
    elif mode == 'cosh()':
            return c.cos(a)
    elif mode == 'tanh()':
            return c.tan(a)
    elif mode == 'sinh()':
            return c.sin(a)
    elif mode == 'acosh()':
            return c.cos(a)
    elif mode == 'atanh()':
            return c.tan(a)
    elif mode == 'asinh()':
            return c.sin(a)
        # Hyperbolic Functions
    else:
            raise AttributeError(''' 'crun' object has no attribute '%s' ''' % mode)

def meaning(mode=''):
    if mode == '+':
        message = 'Find the sum of A and B, indicating A plus B'
    elif mode == '-':
        message = 'Find the difference between A and B, which means A minus B'
    elif mode == '*':
        message = 'Find the product of A and B, representing A times B'
    elif mode == '/':
        message = 'The quotient of A and B, which means A divided by B'
    elif mode == '//':
        message = 'Find the integer part of a divided by B'
    elif mode == '...':
        message = 'Find the remainder of a divided by B'
    elif mode == '%':
        message = 'Find the remainder of a divided by B'
        # Operations
    elif mode == '>':
        message = 'Find whether A is greater than B. if yes, return True; If not, False is returned'
    elif mode == '<':
        message = 'Find whether A is less than B. If yes, return true; If not, false is returned'
    elif mode == '==':
        message = 'Find whether A is equal to B. If yes, return true; If not, false is returned'
    elif mode == '>=':
        message = 'Find whether A is greater than or equal to B. If yes, return true; If not, false is returned'
    elif mode == '<=':
        message = 'Find whether A is less than or equal to B. If yes, return true; If not, false is returned'
    elif mode == '!=':
        message = 'Find whether A is not equal to B. If yes, return true; If not, false is returned'
        # Compare
    elif mode == '!':
        message = 'Find the factorial of A'
    if mode == '^':
        message = 'Seeking the b-th of a'
    if mode == 'sqrt()':
        message = 'Find the square root of A'
        # Power
    elif mode == 'cos()':
        message = 'Return the cosine of x radians'
    elif mode == 'sin()':
        message = 'Return the sine of x radians'
    elif mode == 'tan()':
        message = 'Return the tangent of x radians'
    elif mode == 'acos()':
        message = 'Return the arc cosine of A, in radians'
    elif mode == 'asin()':
        message = 'Return the arc sine of A, in radians'
    elif mode == 'atan()':
        message = 'Return the arc tangent of A, in radians'
    elif mode == 'dist()':
        message = 'Return the Euclidean distance between two points A and B, \n each given as a sequence (or iterable) of coordinates. \n The two points must have the same dimension'
    elif mode == 'hypot()':
        message = '''Return the Euclidean norm,
sqrt(sum(A**2 for A in coordinates)).
This is the length of the vector from the origin to the point given by the coordinates.
For a two dimensional point (A, B),
this is equivalent to computing the hypotenuse of a right triangle using the Pythagorean theorem, sqrt(A*A + B*B)'''
        # Trigonometric Function
    elif mode == 'acosh()':
        message = 'Return the inverse hyperbolic cosine of A'
    elif mode == 'asinh()':
        message = 'Return the inverse hyperbolic sine of A'
    elif mode == 'atanh()':
        message = 'Return the inverse hyperbolic tangent of A'
    elif mode == 'cosh()':
        message = 'Return the hyperbolic cosine of A'
    elif mode == 'sinh()':
        message = 'Return the hyperbolic sine of A'
    elif mode == 'tanh()':
        message = 'Return the hyperbolic tangent of A'
        # Hyperbolic Functions
    elif mode == 'exp()':
        message = 'Return e raised to the power A, where e = 2.718281… is the base of natural logarithms. \n This is usually more accurate than math.e ** A or pow(math.e, A)'
    elif mode == 'expm1()':
        message = '''Return e raised to the power A, minus 1.
Here e is the base of natural logarithms.
For small floats A, the subtraction in exp(A) - 1 can result in a significant loss of precision;
the expm1() function provides a way to compute this quantity to full precision:

>>> from math import exp, expm1
>>> exp(1e-5) - 1  # gives result accurate to 11 places
1.0000050000069649e-05
>>> expm1(1e-5)    # result accurate to full precision
1.0000050000166668e-05'''
        # Power And Logarithmic Functions
    elif mode == 'Degrees()':
        message = 'Convert angle A from radians to degrees'
    elif mode == 'degrees()':
        message = 'Convert angle A from radians to degrees'
    elif mode == 'Radians()':
        message = 'Convert angle A from degrees to radians'
    elif mode == 'radians()':
        message = 'Convert angle A from degrees to radians'
        # Angular Conversion
    elif mode == 'abs()':
        message = 'Return the absolute value of a'
        # Else
    elif mode == 'Int / Float':
        message = 'Force integer A to be converted to decimal, or convert decimal A to integer ( Note: if the decimal part of A is 0, A will be converted to decimal x.0 )'
    elif mode == 'int / float':
        message = 'Force integer A to be converted to decimal, or convert decimal A to integer ( Note: if the decimal part of A is 0, A will be converted to decimal x.0 )'
    elif mode == 'Type':
        message = 'Returns the type of A, integer returns Int, decimal returns Float \n ( Note: if decimal part is 0, Int is returned )'
    elif mode == 'type':
        message = 'Returns the type of A, integer returns Int, decimal returns Float \n ( Note: if decimal part is 0, Int is returned )'
        # Type
    else:
            raise AttributeError(''' 'meaning' object has no attribute '%s' ''' % mode)

def list():
    a = '''
+, -, *, /, //, ..., %,
^, sqrt(), sqare root,
exp(), exp1(),
cos(), tan(), sin(),
acos(), atan(), asin(),
cosh(), tanh(), sinh(),
acosh(), atanh(), asinh(),
abs(),
Int / Float, Type
'''
    return a
