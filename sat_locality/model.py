"""SAT model classes"""


class Variable():
    """
    number: variable identifier
    bearing: [0, 1) bearing clockwise from north
    """
    def __init__(self, number, bearing):
        self.number = number
        self.bearing = bearing
