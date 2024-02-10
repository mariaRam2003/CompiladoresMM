from ShuntingYard.tree_node import TreeNode
import graphviz

EPSILON = '𝜀'


class DirectConstruction:
    def __init__(self, parse_tree: TreeNode, nodes: set):
        self.nodes = nodes
        self.parse_tree = self._normalize_tree(parse_tree)
        self.parse_tree.print_tree()

        self.node_positions = self._set_node_positions()
        self._nullable_nodes = self._nullable()
        self.first_positions = self._firstpos()
        self.last_positions = self._lastpos()
        self.follow_positions = self._followpos()

        self.DFA = self._dfa_builder()

        self.transition_table = self._transition_table()
        self.final_states = self._final_states()


    def _normalize_tree(self, tree: TreeNode):
        """
        This method normalizes the tree by adding a '.' at the root of the tree
        where the left child is the tree and the right child is the '#' symbol
        :param tree: TreeNode
        :return: TreeNode
        """
        concat_node = TreeNode('.')
        concat_node.left = tree
        hashtag_node = TreeNode('#')
        concat_node.right = hashtag_node

        # Adds the nodes to the set of nodes
        self.nodes.add(concat_node)
        self.nodes.add(hashtag_node)

        return concat_node

    def _set_node_positions(self):
        """
        This methods sets a position (or id) to each outer leaf node in the tree
        :return: a dictionary of the form {position: TreeNode}
        """
        index = 0  # This is the position of the node in the tree
        node_positions = {}

        def visit(node: TreeNode):
            if node.left:
                visit(node.left)
            if node.right:
                visit(node.right)

            if not node.right and not node.left:
                nonlocal index
                node_positions[node] = index
                index += 1

        visit(self.parse_tree)
        return node_positions

    def _nullable(self):
        """
        This method returns a dictionary of the form {TreeNode: bool} where the value is True if the node is nullable
        :return:
        """
        nullable = {item: False for item in self.nodes}

        def visit(node: TreeNode):
            if node.left:
                visit(node.left)
            if node.right:
                visit(node.right)

            if not node.right and not node.left:
                if node.value == EPSILON:
                    nullable[node] = True
            else:
                if node.value == '|':
                    nullable[node] = nullable[node.left] or nullable[node.right]
                elif node.value == '.':
                    nullable[node] = nullable[node.left] and nullable[node.right]
                elif node.value in ['?', '*']:
                    nullable[node] = True

        visit(self.parse_tree)
        return nullable

    def _firstpos(self):
        """
        This method returns a dictionary of the form {TreeNode: set()} where the value is the set of first positions
        :return:
        """
        first_positions = {item: set() for item in self.nodes}

        def visit(node: TreeNode):
            if node.left:
                visit(node.left)
            if node.right:
                visit(node.right)

            if not node.right and not node.left:
                if node.value != EPSILON:
                    first_positions[node].add(self.node_positions[node])
            else:
                if node.value == '|':
                    first_positions[node] = first_positions[node.left].union(first_positions[node.right])
                elif node.value == '.':
                    if self._nullable_nodes[node.left]:
                        first_positions[node] = first_positions[node.left].union(first_positions[node.right])
                    else:
                        first_positions[node] = first_positions[node.left]
                elif node.value in ['?', '*']:
                    first_positions[node] = first_positions[node.left]

        visit(self.parse_tree)
        return first_positions

    def _lastpos(self):
        """
        This method returns a dictionary of the form {TreeNode: set()} where the value is the set of last positions
        :return:
        """
        last_positions = {item: set() for item in self.nodes}

        def visit(node: TreeNode):
            if node.left:
                visit(node.left)
            if node.right:
                visit(node.right)

            if not node.right and not node.left:
                if node.value != EPSILON:
                    last_positions[node].add(self.node_positions[node])
            else:
                if node.value == '|':
                    last_positions[node] = last_positions[node.left].union(last_positions[node.right])
                elif node.value == '.':
                    if self._nullable_nodes[node.right]:
                        last_positions[node] = last_positions[node.left].union(last_positions[node.right])
                    else:
                        last_positions[node] = last_positions[node.right]
                elif node.value in ['?', '*']:
                    last_positions[node] = last_positions[node.left]

        visit(self.parse_tree)
        return last_positions

    def _followpos(self):
        """
        This method returns a dictionary of the form {TreeNode: set()} where the value is the set of follow positions
        :return: {TreeNode: set()}
        """
        follow_positions = {item: set() for item in self.nodes}

        def visit(node: TreeNode, follow_positions):
            if node.left:
                visit(node.left, follow_positions)
            if node.right:
                visit(node.right, follow_positions)

            if node.value == '.':  # If the node is a concatenation node
                lastpos = self.last_positions[node.left]
                firstpos = self.first_positions[node.right]

                follow_positions[node] = lastpos.union(firstpos)

            elif node.value == '*':  # If the node is a kleene star node
                lastpos = self.last_positions[node]
                firstpos = self.first_positions[node]

                follow_positions[node] = lastpos.union(firstpos)

        visit(self.parse_tree, follow_positions)
        return follow_positions


    def _transition_table(self):
        """
        Constructs the transition table for the DFA.
        :return: Transition table (nested dictionary)
        """
        self.initial_state = self.first_positions[self.parse_tree]
        alphabet = set()  # Determine the alphabet
        transition_table = {}

        # Populate the transition table based on followpos and alphabet
        for node, followpos_set in self.follow_positions.items():
            state = self.node_positions[node]
            transition_table[state] = {}

            for symbol in alphabet:
                # Determine where this state transitions on this symbol
                next_state = set()
                for pos in followpos_set:
                    if pos.value == symbol:
                        next_state.add(self.node_positions[pos])

                    if next_state:
                        transition_table[state][symbol] = next_state

            return transition_table



    # def _transition_table(self):
    #     """
    #     Constructs the transition table for the DFA.
    #     :return: Transition table (nested dictionary)
    #     """
    #     initial_state = self.first_positions[self.parse_tree]
    #     alphabet = set()  # Determine the alphabet
    #     transition_table = {}
    #
    #     # Populate the transition table based on followpos and alphabet
    #     for node, followpos_set in self.follow_positions.items():
    #         state = self.node_positions[node]
    #         transition_table[state] = {}
    #
    #         for symbol in alphabet:
    #             # Determine where this state transitions on this symbol
    #             next_state = set()
    #             for pos in followpos_set:
    #                 if pos.value == symbol:
    #                     next_state.add(self.node_positions[pos])
    #
    #             if next_state:
    #                 transition_table[state][symbol] = next_state
    #
    #     return transition_table
    #
    # def _final_states(self):
    #     """
    #     Determines the final states of the DFA.
    #     :return: Set of final states
    #     """
    #     final_states = set()
    #
    #     # Find the states containing the position corresponding to '#'
    #     for node, followpos_set in self.follow_positions.items():
    #         state = self.node_positions[node]
    #         for pos in followpos_set:
    #             if pos.value == '#':
    #                 final_states.add(state)
    #
    #     return final_states

    # def draw_dfa(self):
    #     """
    #     Draws a graphical representation of the DFA using Graphviz.
    #     """
        # Generate Graphviz code to represent the DFA
        # Use self.transition_table and self.final_states to create the graph
        #
        # Example: (you'll need to adapt this to your specific data structure)
        # graph = Graph()
        # for state, transitions in self.transition_table.items():
        #     for symbol, next_states in transitions.items():
        #         for next_state in next_states:
        #             graph.edge(str(state), str(next_state), label=symbol)
        # for final_state in self.final_states:
        #     graph.node(str(final_state), shape='doublecircle')
        # graph.render('dfa')