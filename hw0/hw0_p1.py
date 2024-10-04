# Helper function to parse a single term
# maybe ok, not sure
def parse_term(term):
    i = 0
    n = len(term)
    sign = 1
    coefficient = 0
    
    # Handle sign of the term
    if term[i] == '-':
        sign = -1
        i += 1
    elif term[i] == '+':
        i += 1

    # Extract coefficient
    while i < n and term[i].isdigit():
        coefficient = coefficient * 10 + int(term[i])
        i += 1

    if coefficient == 0:
        coefficient = 1
    
    coefficient *= sign

    variables = {}

    # Extract variables and exponents
    while i < n:
        var = term[i]
        i += 1

        # Check if exponent exists
        if i < n and term[i] == '^':
            i += 1
            exp = 0
            while i < n and term[i].isdigit():
                exp = exp * 10 + int(term[i])
                i += 1
        else:
            exp = 1

        if var in variables:
            variables[var] += exp
        else:
            variables[var] = exp

    return (coefficient, variables)

# Function to parse the whole polynomial
# i think it is ok here
def parse_polynomial(polynomial):
    #print(polynomial)
    terms = polynomial.replace('-', '+-').split('+')
    parsed_terms = []

    for term in terms:
        term = term.strip()
        if term:
            parsed_terms.append(parse_term(term))

    return parsed_terms

# Function to multiply two terms
def multiply_terms(term1, term2):
    coefficient = term1[0] * term2[0]
    variables = term1[1].copy()

    for var, exp in term2[1].items():
        if var in variables:
            variables[var] += exp
        else:
            variables[var] = exp

    return (coefficient, variables)

# Function to multiply two polynomials
def multiply_polynomials(parsed_polynomials):
    result = parsed_polynomials[0]
    for i in range(1, len(parsed_polynomials)):
        temp = []
        for term1 in result:
            for term2 in parsed_polynomials[i]:
                temp.append(multiply_terms(term1, term2))
        result = temp.copy()
    return result

# Function to combine like terms
def combine_like_terms(terms):
    result_terms = []

    while terms:
        coeff1, vars1 = terms.pop(0)
        for i in range(len(terms) - 1, -1, -1):
            coeff2, vars2 = terms[i]
            if vars1 == vars2:  # If variables and exponents match, combine them
                coeff1 += coeff2
                terms.pop(i)
        if coeff1 != 0:
            result_terms.append((coeff1, vars1))

    return result_terms

# Function to format the polynomial back into a string
def format_polynomial(terms):
    result = []
    for coefficient, variables in terms:
        var_str = ''
        for var, exp in sorted(variables.items()):
            if var == '*':
                continue
            if exp == 1:
                var_str += f'{var}'
            else:
                var_str += f'{var}^{exp}'

        if coefficient == 1:
            if var_str:
                result.append(f'{var_str}')
            else:
                result.append(f'1')
        elif coefficient == -1:
            if var_str:
                result.append(f'-{var_str}')
            else:
                result.append(f'-1')
        else:
            if var_str:
                result.append(f'{coefficient}*{var_str}')
            else:
                result.append(f'{coefficient}')

    return '+'.join(result).replace('+-', '-')

def polynomial_multiplication(poly_str):
    # Split the polynomials by multiplication symbol '*'
    polynomials = []
    for i in range(0, len(poly_str)):
        if poly_str[i] == '(':
            left: int = i
        if poly_str[i] == ')':
            polynomials.append(poly_str[left + 1: i])
    
    # for str in polynomials: print(str)
    
    # ok above
    # Parse each polynomial
    parsed_polynomials = [parse_polynomial(poly.strip()) for poly in polynomials]
    
    # for str in parsed_polynomials: print(str)
    # ok above(maybe)

    # Multiply the parsed polynomials
    result = multiply_polynomials(parsed_polynomials)
    # ok above(maybe)
    
    # print(result)
    # Combine like terms
    combined_result = combine_like_terms(result)
    # print(combined_result)
    # ok above(maybe)
    # Format the result
    return format_polynomial(combined_result)
    
def bonus_point(ans) :
    # replace all the * with empty string
    ans = ans.replace('*', '')
    # replace all the ^ with empty string
    ans = ans.replace('^', '')
    return ans



# Example usage:(5*X+3*Y^5)(3*Y+4*X) output 15*XY + 20*X^2 + 9*Y^6 + 12*XY^5
input_polynomial = input()
output = polynomial_multiplication(input_polynomial)
print(output)
output = bonus_point(output)
print(output)
