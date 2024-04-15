class ChomskyNormalForm:

    Vn = []
    Vt = []
    P = {}

    def __init__(self):
        self.Vn = ["S", "A", "B", "C", "D"]
        self.Vt = ["a", "b"]
        self.P = {
            "S": ["aB", "bA", "B"],
            "A": ["b", "aD", "AS", "bAB", "ε"],
            "B": ["a", "bS"],
            "C": ["AB"],
            "D": ["BB"]
        }

    def eliminate_epsilon_productions(self):
        if self.check_for_epsilon_productions():
            eps_keys = []
            for key in self.P.keys():
                if "ε" in self.P[key]:
                    eps_keys.append(key)
                    self.P[key].remove("ε")
            for key in self.P.keys():
                if any([any(value in eps_keys for value in values) for values in self.P[key]]):
                    for keys in eps_keys:
                        for value in self.P[key]:
                            if keys in value:
                                if value == keys:
                                    self.P[key].append("ε")
                                else:
                                    combinations = self.generate_combinations(value, keys)
                                    for combination in combinations:
                                        if combination not in self.P[key]:
                                            self.P[key].append(combination)

    def check_for_epsilon_productions(self):
        return any("ε" in value for value in self.P.values())

    def generate_combinations(self, value, key):
        combinations = []

        def generate_combinations_recursive(current_value, current_index):
            if current_index == len(current_value):
                combinations.append(current_value)
                return
            if current_value[current_index] == key:
                generate_combinations_recursive(current_value[:current_index] + current_value[current_index + 1:],
                                             current_index)
            generate_combinations_recursive(current_value, current_index + 1)
        generate_combinations_recursive(value, 0)
        return combinations

    def eliminate_unit_productions(self):
        if self.check_for_unit_productions():
            for key in self.P.keys():
                for value in self.P[key]:
                    if value in self.Vn and self.P.get(value) is not None:
                        self.P[key].remove(value)

                        for production in self.P[value]:
                            if production not in self.P[key]:
                                self.P[key].append(production)

    def check_for_unit_productions(self):
        return any(any(value == v for v in values) for value in self.Vn for values in self.P.values())

    def remove_inaccessible_symbols(self):
        accessible_symbols = self.check_for_inaccessible_symbols()
        keys_to_remove = []
        iterator = iter(self.P.keys())
        try:
            key = next(iterator)
            while key is not None:
                if key not in accessible_symbols:
                    keys_to_remove.append(key)
                key = next(iterator)
        except StopIteration:
            pass
        for key in keys_to_remove:
            self.P.pop(key)

    def check_for_inaccessible_symbols(self):
        accessible_symbols = [next(iter(self.P.keys()))]
        for values in self.P.values():
            for value in values:
                for non_terminal in self.Vn:
                    if non_terminal in value:
                        if non_terminal not in accessible_symbols:
                            accessible_symbols.append(non_terminal)
        return accessible_symbols

    def remove_unproductive_symbols(self):
        productive_symbols = []
        for i in range(0, len(self.P.keys())):
            for key in self.P.keys():
                for value in self.P[key]:
                    for terminal in self.Vt:
                        if terminal == value:
                            if key not in productive_symbols:
                                productive_symbols.append(key)
                    for productive_symbol in productive_symbols:
                        if productive_symbol in value:
                            if key not in productive_symbols:
                                productive_symbols.append(key)

        if len(self.P.keys()) != len(productive_symbols):
            keys_to_remove = []
            iterator = iter(self.P.keys())
            try:
                key = next(iterator)
                while key is not None:
                    if key not in productive_symbols:
                        keys_to_remove.append(key)
                    key = next(iterator)
            except StopIteration:
                pass
            for key in keys_to_remove:
                self.P.pop(key)

    def chomsky_normal_form(self):
        created_transitions = {}
        temp_copy = self.P.copy()
        index = 1
        for key in self.P.keys():
            for value in self.P[key][:]:
                for terminal in self.Vt:
                    if terminal in value and len(value) > 1:
                        if terminal not in created_transitions.values():
                            created_transitions["X" + str(index)] = terminal
                            self.Vn.append("X" + str(index))
                            temp_copy[key].remove(value)
                            value = value.replace(terminal, "X" + str(index))
                            temp_copy[key].append(value)
                            index += 1
                        else:
                            temp_copy[key].remove(value)
                            key_to_add = [key for key, value in created_transitions.items() if value == terminal][0]
                            value = value.replace(terminal, key_to_add)
                            temp_copy[key].append(value)
                characters = len(value)
                if characters > 2:
                    true_char = 0
                    temp_val = value
                    for created in created_transitions:
                        true_char += value.count(created)
                        temp_val = temp_val.replace(created, "")
                    true_char += len(temp_val)
                    while true_char > 2:
                        trans_chars = self.select_first_two_true_characters(value)
                        created_transitions["X" + str(index)] = trans_chars
                        self.Vn.append("X" + str(index))
                        temp_copy[key].remove(value)
                        value = value.replace(trans_chars, "X" + str(index), 1)
                        temp_copy[key].append(value)
                        index += 1
                        true_char -= 1

        self.P = {**temp_copy, **created_transitions}

    def select_first_two_true_characters(self, value):
        true_characters = ""
        true_count = 0
        in_x = False
        for char in value:
            if char == "X" and not in_x:
                in_x = True
                true_characters += char
            elif char == "X" and in_x:
                true_characters += char
                true_count += 1
            elif char.isdigit() and in_x:
                true_characters += char
            elif in_x:
                true_count += 1
                in_x = False
                if true_count == 2:
                    break
                true_characters += char
                true_count += 1
            else:
                true_characters += char
                true_count += 1

            if true_count == 2:
                break
        return true_characters

    def to_chomsky_normal_form(self):
        self.eliminate_epsilon_productions()
        self.eliminate_unit_productions()
        self.remove_inaccessible_symbols()
        self.remove_unproductive_symbols()
        self.chomsky_normal_form()


chomsky = ChomskyNormalForm()
print(chomsky.P)
print(chomsky.Vn)
chomsky.to_chomsky_normal_form()
print(chomsky.P)
print(chomsky.Vn)
#chomsky.eliminate_epsilon_productions()
# chomsky.eliminate_epsilon_productions()
# print(chomsky.check_for_epsilon_productions())
# print(chomsky.check_for_unit_productions())
# print(chomsky.P)
# chomsky.eliminate_unit_productions()
# chomsky.remove_inaccessible_symbols()
# chomsky.remove_unproductive_symbols()
# chomsky.chomsky_normal_form()
# print(chomsky.P)
# print(chomsky.Vn)
# print(chomsky.select_first_two_true_characters("X11DD"))
