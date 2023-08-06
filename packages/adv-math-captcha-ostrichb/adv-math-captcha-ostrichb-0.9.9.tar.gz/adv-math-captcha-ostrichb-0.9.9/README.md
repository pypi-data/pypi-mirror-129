# ADV-Math-captcha

An advanced mathematical captcha for simple human verification.

## How to use

This is an example to make an verification:
```Python
from adv-math-captcha import Captcha


if __name__ == '__main__':
    formula1 = Captcha(5, 4, 15, 10, 50, 5, 5)
    inp = input("Solve this simple question: {0} = ".format(formula1.formula_str))
    if formula1.verify(float(inp)):
        print("Verify success!")
    else:
        print("Verify failed! The correct answer is {0:.0f}!".format(float(formula1.evaluation)))
```

## Usage

This module only provides one class with only one method. To make a captcha, just use `Captcha(difficulty, term, number_range)`, which is the shortest form. If you wanna use more parameters, use `Captcha(difficulty, term, number_range, factor_range, exponentiation_range, exp_base_range, exp_index_range)`

Details: (All the parameters are integers)
- `difficulty`: Decides the difficulty of the generated expression. Valid value is 1-5 in integer.
  - `1`: Only additions
  - `2`: Additions and subtractions
  - `3`: Operations in `2`, with Mutliplications and divisions (For divisions, the result will always be an integer)
  - `4`: Operations in `3`, with exponentiation calculations
  - `5`: Operations in `4`, with logarithm calculations (The result will always in simple form to insure the result is reducable, for example, 'ln(e^3)', 'log_2 (8)')
- `term`: Determines how many items will appear in an expression. Althogh there is no limits, don't be too much, or it will be hard to get the answer. :) (P.S. an division will be counted as one item. E.g. (6 / 3) )
- `number_range`: Determines the range of the coefficient.
- `factor_range`: Determines the range of division results and dominators. Default value is 10.
- `exponentiation_range`: Determines the range of exponential calculation. Default value is 50.
- `exp_base_range`: Determines the range of base number. Default value is 6.
- `exp_index_range`: Determines the range of index number. Default value is 5.

Once you initialized an captcha object, you can get the expression string from `Captcha.formula_str` variable in class, or make an verification using the `Captcha.verify(user_input)`. A `True` will be returned if the verification is successful, or `False`  if failed.

You can also get the actual value of the expression from `Captcha.evaluation` variable.

# About

If you want to contact me, mail to [mailto](mailto:ostrichb@yandex.com)