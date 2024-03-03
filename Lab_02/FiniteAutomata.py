# Variant 18
import re
import copy
import networkx as nx
import matplotlib.pyplot as plt

class Grammar:

    VN = []
    VT = []
    P = []

    def __init__(self):
        pass


class FiniteAutomaton:

    Q = []
    Sigma = []
    q0 = []
    F = []
    Delta = {}

    def __init__(self):
        self.Q = ["q0", "q1", "q2", "q3"]
        self.Sigma = ["a", "b", "c"]
        self.q0 = "q0"
        self.F = "q3"
        self.Delta = {
            "q0": ["a q0", "a q1"],
            "q1": ["b q2"],
            "q2": ["a q2", "b q3"],
            "q3": ["a q3"]
        }
        # Other test cases
        # self.Q = ["q0", "q1", "q2"]
        # self.Sigma = ["a", "b"]
        # self.q0 = "q0"
        # self.F = "q2"
        # self.Delta = {
        #     "q0": ["a q0", "a q1"],
        #     "q1": ["a q2", "b q1"],
        #     "q2": ["a q2", "b q2"]
        # }
        # self.Q = ["q0", "q1", "q2", "q3", "q4"]
        # self.Sigma = ["a", "b"]
        # self.q0 = "q0"
        # self.F = "q4"
        # self.Delta = {
        #     "q0": ["a q1"],
        #     "q1": ["b q1", "a q2"],
        #     "q2": ["b q2", "b q3"],
        #     "q3": ["b q4", "a q1"],
        #     "q4": []
        # }

    def is_deterministic(self) -> bool:
        for state, transitions in self.Delta.items():
            symbols = []

            for transition in transitions:
                symbols.append(transition[0])
            if len(symbols) != len(set(symbols)):
                return False

        return True

    def grammar_conversion(self) -> Grammar:
        grammar = Grammar()

        grammar.VN = self.Q
        grammar.VT = self.Sigma
        grammar.P = self.Delta

        return grammar

    def NFA_to_DFA(self):
        if self.is_deterministic():
            return
        dfa = FiniteAutomaton()

        transition_chars_pattern = re.compile(r'^(.*?)\s')
        transition_states_pattern = re.compile(r'\s(.*)$')

        transitions = {self.q0: self.group_states(self.Delta[self.q0])}

        finished_states = []
        last_state = ""

        while not(self.has_all_states(transitions)):

            transitions_copy = copy.deepcopy(transitions)
            for value in finished_states:
                del transitions_copy[value]

            for key, values in transitions_copy.items():
                symbols = []
                states = []
                # Getting all the symbols and transition states for the current state
                for value in values:
                    symbols.append(transition_chars_pattern.search(value).group(1))
                    states.append(transition_states_pattern.search(value).group(1))
                # Checking for duplicate symbols in transitions, meaning we have a NFA transition
                if not(len(symbols) == len(set(symbols))):
                    unique_symbols = set(symbols)
                    for element in unique_symbols:
                        # Getting the positions for every symbol and checking if there's more than 1 of it in the array
                        positions = [i for i, value in enumerate(symbols) if value == element]
                        if len(positions) > 1:
                            new_state = ""
                            new_state_trans = []
                            # Creating a new state
                            for position in positions:
                                if states[position] not in new_state:
                                    new_state += states[position]
                                # Getting the transitions from the new state
                                for state1 in self.degroup_states(states[position]):
                                    for elem in self.Delta[state1]:
                                        if elem not in new_state_trans:
                                            new_state_trans.append(elem)

                            if new_state in transitions:
                                break

                            # Adding the new state and its transitions to the dictionary
                            transitions[new_state] = self.group_states(new_state_trans)
                            last_state = new_state

                # Checking the other case, when there's no NFA transitions
                for state in states:
                    if state not in transitions:
                        # Otherwise, we degroup the state and add all the transitions to those states
                        new_state_trans = []
                        new_states = self.degroup_states(state)
                        for new_state in new_states:
                            for trans in self.Delta[new_state]:
                                if trans not in new_state_trans:
                                    new_state_trans.append(trans)
                        new_state_trans = self.group_states(new_state_trans)
                        transitions[state] = new_state_trans
                        last_state = state

                finished_states.append(key)



        finished_states.append(last_state)
        # Changing the attributes of our new DFA
        dfa.Q = finished_states
        dfa.F = []
        # Adding final states
        for state in dfa.Q:
            if self.F in state:
                dfa.F.append(state)
        dfa.Delta = transitions

        return dfa


    def group_states(self, states_arr) -> []:
        transition_chars_pattern = re.compile(r'^(.*?)\s')
        transition_states_pattern = re.compile(r'\s(.*)$')
        # Sorting the array so that the identical elements are adjacent
        states_arr.sort()
        for i in range(len(states_arr) - 1, 0, -1):
            # Searching for identical transition characters and grouping the states together
            if transition_chars_pattern.search(states_arr[i]).group(
                    1) == transition_chars_pattern.search(states_arr[i - 1]).group(1):
                temp = transition_states_pattern.search(states_arr[i]).group(1) + \
                       transition_states_pattern.search(states_arr[i - 1]).group(1)
                states_arr[i - 1] = transition_chars_pattern.search(states_arr[i - 1]) \
                                                 .group(1) + " " + temp
                # Removing the current state, since we injected a new one into the array
                states_arr.pop(i)

        return states_arr

    def degroup_states(self, states) -> []:
        degrouped_states = []
        current_state = ""

        for char in states:
            current_state += char
            if current_state in self.Q:
                degrouped_states.append(current_state)
                current_state = ""

        return degrouped_states

    def has_all_states(self, dictionary):
        transition_states_pattern = re.compile(r'\s(.*)$')

        for key, values in dictionary.items():
            for value in values:
                state = transition_states_pattern.search(value).group(1)

                if state not in dictionary:
                    return False
        return True

    def draw_automaton(self):
        graph = nx.DiGraph()

        # Setting the nodes and edges using our finite automaton's transition dictionary
        for node, edges in self.Delta.items():
            for edge in edges:
                label, target = edge.split(' ', 1)
                # Adding edges and labels
                graph.add_edge(node, target, label=label)
                # Modifying the label for the self loop by adding padding so that it's not drawn inside the node
                if node == target:
                    label = "           " + label
                    graph.add_edge(node, target, label=label)

        pos = nx.planar_layout(graph)
        labels = nx.get_edge_attributes(graph, 'label')
        # Drawing the graph
        nx.draw(graph, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=8)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color='red', font_size=12)
        plt.show()


finite_automaton = FiniteAutomaton()
dfa = finite_automaton.NFA_to_DFA()
print(dfa.Delta)
print(dfa.F)
print(dfa.Q)
print(dfa.is_deterministic())
dfa.draw_automaton()
