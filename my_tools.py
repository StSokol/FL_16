

def get_rus_case(number, cases):
    # number and cases in russian ["сайтов","сайт","cайта"] < - 0 сайтов, 1 сайт, 2 сайта

    if 5 < number % 100 < 21:
        return cases[0]
    if 1 < number % 10 < 5:
        return cases[2]
    if number % 10 == 1:
        return cases[1]
    return cases[0]
