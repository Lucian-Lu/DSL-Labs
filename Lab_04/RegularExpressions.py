import random
# Variant 3


def generate_words_from_regex(nr, limit):
    string = ""
    counter = 0
    if nr == 1:
        string += "O"
        rand = random.random()
        while rand <= 0.25:
            rand = random.random()
        while rand > 0.25 and counter < limit:
            counter += 1
            if rand < 0.5:
                string += "P"
            elif rand < 0.75:
                string += "Q"
            else:
                string += "R"
            rand = random.random()

        string += "2"
        rand = random.random()
        if rand > 0.5:
            string += "3"
        else:
            string += "4"
        return string
    elif nr == 2:
        rand = random.random()
        while rand > 0.33 and counter < limit:
            counter += 1
            string += "A"
            rand = random.random()
        string += "B"
        rand = random.random()
        if rand <= 0.3333:
            string += "C"
        elif rand <= 0.6666:
            string += "D"
        else:
            string += "E"
        string += "E"
        rand = random.random()
        if rand <= 0.3333:
            string += "GG"
        elif rand <= 0.6666:
            string += "HH"
        else:
            string += "ii"
        return string
    elif nr == 3:
        string += "J"
        rand = random.random()
        while rand > 0.3333 and counter < limit:
            counter += 1
            string += "J"
            rand = random.random()
        string += "K"
        rand = random.random()
        counter = 0
        while rand > 0.25 and counter < limit:
            counter += 1
            if rand < 0.5:
                string += "L"
            elif rand < 0.75:
                string += "M"
            else:
                string += "N"
            rand = random.random()
        rand = random.random()
        if rand > 0.5:
            string += "O"
        rand = random.random()
        if rand > 0.5:
            string += "PPP"
        else:
            string += "QQQ"
        return string


def parse_regular_expression(regex):
    string = ""
    i = 0
    while i < len(regex):
        current = ""
        if regex[i] == '(':
            while i < len(regex) and regex[i] != ')':
                current += regex[i]
                i += 1
            if i < len(regex):
                current += regex[i]
            else:
                return "Error: ')' is missing"
            if not(i == len(regex)):
                i += 1

            if i == len(regex):
                symbols = [ch for ch in current if ch not in "()|"]
                rand = random.randint(0, len(symbols)-1)
                string += symbols[rand]

            elif regex[i] == "*":
                symbols = [ch for ch in current if ch not in "()|"]
                rng = random.random()
                while rng > 0.25:
                    rand = random.randint(0, len(symbols)-1)
                    string += symbols[rand]
                    rng = random.random()
                i += 1

            elif regex[i] == "?":
                symbols = [ch for ch in current if ch not in "()|"]
                rng = random.random()
                if rng > 0.5:
                    rand = random.randint(0, len(symbols)-1)
                    string += symbols[rand]
                i += 1
            elif regex[i] == "+":
                symbols = [ch for ch in current if ch not in "()|"]
                rng = random.random()
                while rng <= 0.25:
                    rng = random.random()
                while rng > 0.25:
                    rand = random.randint(0, len(symbols)-1)
                    string += symbols[rand]
                    rng = random.random()
                i += 1
            elif regex[i] == "^":
                symbols = [ch for ch in current if ch not in "()|"]
                rand = random.randint(0, len(symbols)-1)
                string += symbols[rand] * int(regex[i+1])
                i += 2

            elif regex[i] not in "*+?^":
                symbols = [ch for ch in current if ch not in "()|"]
                rand = random.randint(0, len(symbols) - 1)
                string += symbols[rand]

            else:
                print('Error at character' + regex[i])
                return "Error"

        elif regex[i] not in "*+?^":
            if i+1 < len(regex):
                if regex[i+1] not in "*+?^":
                    string += regex[i]
                    i += 1
                elif regex[i+1] == "*":
                    rand = random.random()
                    while rand > 0.333:
                        string += regex[i]
                        rand = random.random()
                    i += 1
                elif regex[i+1] == "+":
                    rand = random.random()
                    while rand <= 0.333:
                        rand = random.random()
                    while rand > 0.333:
                        string += regex[i]
                        rand = random.random()
                    i += 1
                elif regex[i+1] == "?":
                    rand = random.random()
                    if rand > 0.5:
                        string += regex[i]
                    i += 1
                elif regex[i+1] == "^":
                    string += regex[i] * regex[i+2]
                    i += 2
                else:
                    print('Error at character' + regex[i])
                    return "Error"
            else:
                string += regex[i]
                i += 1
        elif regex[i] in "*+?^":
            i += 1
            continue
        else:
            print('Error at character' + regex[i])
            return "Invalid expression"

    return string


# O(P|Q|R)+2(3|4)
# A*B(C|D|E)E(G|H|i)^2
# J+K(L|M|N)*O?(P|Q)^3
print(generate_words_from_regex(1, 5))
print(parse_regular_expression("O(P|Q|R)+2(3|4)"))
