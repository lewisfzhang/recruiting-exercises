# Getting Started

## Source Files
- `order.py` — contains get_shipment(), a function that finds cheapest shipment
- `test.py` — contains all test cases used to test behavior of get_shipment()

Please see docstring and comments for more explanation about code behavior

## Running the Code

To run tests, please run `python3 test.py`
To call get_shipment() function in `order.py`,

    >>> from order import get_shipment
    >>> order = {'apple': 1}
    >>> inventory = [{'name': 'owd', 'inventory': {'apple': 1}}]
    >>> get_shipment(order, inventory)
    [{'owd': {'apple': 1}}]

