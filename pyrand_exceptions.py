class UnsetButtonError(Exception):
    # raised when one or more radio buttons are left un-toggled
    pass

class LengthError(Exception):
    # raised when the length is longer than the maximum number possible characters
    pass