def command(user_string):
    help_string = 'This program is calculator, so you can just write math equation and press "Enter"'
    if user_string == '/help':
        return help_string
    else:
        return 'Unknown command'


def brackets_indexes(equation):
    br_start = equation.index('(') + 1
    br_end = 0
    open_br_count = 0
    for i in range(equation.index('(') + 1, len(equation)):
        if equation[i] == ')':
            if open_br_count == 0:
                br_end = i
            else:
                open_br_count -= 1
        if equation[i] == '(':
            open_br_count += 1
    return br_start, br_end


def math_indexes(equation, sign):
    eq_start = equation.index(sign) - 1
    eq_end = equation.index(sign) + 2
    return eq_start, eq_end


def math(math_equation):
    global variables
    result: float = 0
    if math_equation[0] in ('+', '-'):
        math_equation = ['0'] + math_equation
    while '(' in math_equation:
        br_start, br_end = brackets_indexes(math_equation)
        math_equation = math_equation[:br_start - 1] + [str(math(math_equation[br_start:br_end]))] + math_equation[
                                                                                                     br_end + 1:]
    while '^' in math_equation and len(math_equation) > 3:
        eq_start, eq_end = math_indexes(math_equation, '^')
        math_equation = math_equation[:eq_start] + [str(math(math_equation[eq_start:eq_end]))] + math_equation[eq_end:]
    while '*' in math_equation and len(math_equation) > 3:
        eq_start, eq_end = math_indexes(math_equation, '*')
        math_equation = math_equation[:eq_start] + [str(math(math_equation[eq_start:eq_end]))] + math_equation[eq_end:]
    while '/' in math_equation and len(math_equation) > 3:
        eq_start, eq_end = math_indexes(math_equation, '/')
        math_equation = math_equation[:eq_start] + [str(math(math_equation[eq_start:eq_end]))] + math_equation[eq_end:]
    its_num_or_var = True
    sign_variation = ['+', '-', '/', '^', '*']
    sign = '+'

    for element in math_equation:
        if its_num_or_var and not element.isalpha():
            try:
                if sign == '+':
                    result += float(element)
                if sign == '-':
                    result -= float(element)
                if sign == '*':
                    result = result * float(element)
                if sign == '/':
                    result = float(result / float(element))
                if sign == '^':
                    result = result ** float(element)
            except ValueError:
                if element.isalnum():
                    print('Invalid identifier')
                else:
                    print('Invalid expression')
                return
            its_num_or_var = False
        elif element.isalpha():
            try:
                if sign == '+':
                    result += variables[element]
                if sign == '-':
                    result -= variables[element]
                if sign == '*':
                    result = result * variables[element]
                if sign == '/':
                    result = float(result / variables[element])
                if sign == '^':
                    result = result ** variables[element]

            except KeyError:
                print('Unknown variable')
                return
            its_num_or_var = False
        else:
            sign = element
            if sign not in sign_variation:
                print('Invalid expression')
                return
            its_num_or_var = True
    return result


def variables_assigment(u_input):
    global variables
    assigment = u_input.split('=')
    variable = assigment[0].replace(' ', '')
    second_variable_check = assigment[1].replace(' ', '').isalpha() or assigment[1].replace(' ', '').isdigit()
    if not variable.isalpha():
        print('Invalid identifier')
    else:
        variables[variable] = math(correct_equation(assigment[1]))



def correct_equation(input_string):
    sign = ['+', '-', '=', '/', '^', '(', ')', '*']
    result_string = ''
    if '(' in input_string and input_string.count('(') != input_string.count(')'):  # проверка на кол-во скобок
        print('Invalid expression')
        return
    for char in input_string:  # добавление дополнительных пробелов вокруг математических знаков
        if char in sign:
            result_string += ' ' + char + ' '
        else:
            result_string += char
    result_list = result_string.split()
    sign = ['+', '-', '=', '/', '^', '*']

    for i in range(len(result_list) - 1):  # слияние математических знаков в один элемент
        if result_list[i][0] in sign and result_list[i + 1] in sign:
            result_list[i + 1] = result_list[i] + result_list[i + 1]
            result_list[i] = ' '
    result_list = [i for i in result_list if i != ' ']
    for i in range(len(result_list)):  # проверка на корректность мат знаков
        if result_list[i].count('+') > 1:
            if result_list[i].count('+') != len(result_list[i]):
                print('Invalid expression')
                return
            else:
                result_list[i] = '+'
        if result_list[i].count('-') > 1:
            if result_list[i].count('-') != len(result_list[i]):
                print('Invalid expression')
                return
            else:
                result_list[i] = '+' if result_list[i].count('-') % 2 == 0 else '-'
        if result_list[i].count('*') > 1 or result_list[i].count('/') > 1 or result_list[i].count('^') > 1:
            print('Invalid expression')
            return
    if result_list[-1] in sign or result_list[0] in ('*', '^', '='):
        print('Invalid expression')
        return
    if result_list[0] in ('+', '-'):
        result_list = ['0'] + [] + result_list

    return result_list


user_input = input()
variables = {}
while user_input != '/exit':
    if user_input:
        if '/' == user_input[0]:
            print(command(user_input))
        else:
            if '=' in user_input:
                variables_assigment(user_input)
            else:
                equation = correct_equation(user_input)
                if equation:
                    result_of_equation = math(equation)
                    if result_of_equation is not None:
                        print(result_of_equation)
    # print(variables)
    user_input = input()

print('Bye!')
