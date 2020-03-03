"""This module provides the class for dealing with values with uncertainties."""

class UncertainVal:
    """
    This is a class for dealing with values with uncertainties.

    Attributes:
        value (float): The parameter value
        uncertainty (float): The uncertainty on the parameter value
    """
    def __init__(self, value, uncertainty):
        """
        Initializes UncertainVal class with value and uncertainty.
        """
        self.value = value
        self.uncertainty = uncertainty

    def __repr__(self):   
        """
        >>> uval = UncertainVal(0.5, 0.1)
        >>> eval(repr(uval)) == uval
        True
        """
        return f'UncertainVal({self.value!r}, {self.uncertainty!r})'

    def __str__(self):
        """
        Returns value and uncertainty as a formatted string.
        
        >>> uval = UncertainVal(0.5, 0.1)
        >>> str(uval)
        '0.50+-0.10'
        """
        return f'{float(self.value):.2f}+-{float(self.uncertainty):.2f}'

    def __eq__(self, other):
        """Two UncertainVals are equal if their values are equal and their uncertainties are equal"""
        return self.value == other.value and self.uncertainty == other.uncertainty

if __name__ == "__main__":
    import doctest
    doctest.testmod()
