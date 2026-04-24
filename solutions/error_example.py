"""Solution with runtime error."""


def solve(input_data):
    """This solution raises an error."""
    # This will raise an error when 'c' key doesn't exist
    return input_data["a"] + input_data["c"]
