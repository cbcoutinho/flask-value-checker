"""
parsing nodes,
that contain their respective values
"""


class Node:
    pass


class VariableNode(Node):
    def __init__(self, variable):
        self.variable = variable


class StringNode(Node):
    def __init__(self, value):
        self.value = value


class NumberNode(Node):
    def __init__(self, value):
        self.value = value
