'''
A collection of helper functions.
'''


# converts an integer into a roman numeral
def integer_to_roman(number):
    values = [
        1000, 900, 500, 400, 100,
        90, 50, 40, 10,
        9, 5, 4, 1,
    ]
    symbols = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I",
    ]

    roman = ""
    
    i = 0
    while number > 0:
        for _ in range(number // values[i]):
            roman += symbols[i]
            number -= values[i]
        i += 1
    return roman

