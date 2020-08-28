from order import get_shipment

def equals(expected, order, inventory):
    return expected == get_shipment(order, inventory)

def caughtAssertion(order, inventory):
    try:
        get_shipment(order, inventory)
        return False
    except AssertionError:
        return True

def test0():
    """ Example test: Order can be shipped using one warehouse """
    expected = [{'owd': {'apple': 1}}]
    order = {'apple': 1}
    inventory = [{'name': 'owd', 'inventory': {'apple': 1}}]
    return equals(expected, order, inventory)

def test1():
    """ Example test: Order can be shipped using multiple warehouses """
    expected = [{'dm': {'apple': 5}}, {'owd': {'apple': 5}}]
    order = {'apple': 10}
    inventory = [{'name': 'owd', 'inventory': {'apple': 5}}, {'name': 'dm', 'inventory': {'apple': 5}}]
    return equals(expected, order, inventory)

def test2():
    """ Example test: Order cannot be shipped because there is not enough inventory """
    expected = []
    order = {'apple': 1}
    inventory = [{'name': 'owd', 'inventory': {'apple': 0}}]
    return equals(expected, order, inventory)

def test3():
    """ Example test: Order cannot be shipped because there is not enough inventory """
    expected = []
    order = {'apple': 2}
    inventory = [{'name': 'owd', 'inventory': {'apple': 1}}]
    return equals(expected, order, inventory)

def test4():
    """ Empty order """
    expected = []
    order = {}
    inventory = [{'name': 'owd', 'inventory': {'apple': 1}}]
    return equals(expected, order, inventory)

def test5():
    """ Empty inventory """
    expected = []
    order = {'apple': 2}
    inventory = []
    return equals(expected, order, inventory)

def test6():
    """ One warehouse cheaper than two warehouses """
    expected = [{'w3': {'a': 3, 'b': 3}}]
    order = {'a': 3, 'b': 3}
    inventory = [{'name': 'w1', 'inventory': {'a': 5}},
                 {'name': 'w2', 'inventory': {'b': 5}},
                 {'name': 'w3', 'inventory': {'a': 5, 'b': 5}}]
    return equals(expected, order, inventory)

def test7():
    """ Two warehouses cheaper than three warehouses """
    expected = [{'w2': {'a': 4, 'b': 5}}, {'w4': {'b': 3, 'c': 5}}]
    order = {'a': 4, 'b': 8, 'c': 5}
    inventory = [{'name': 'w1', 'inventory': {'a': 5}},
                 {'name': 'w2', 'inventory': {'a': 5, 'b': 5}},
                 {'name': 'w3', 'inventory': {'b': 10}},
                 {'name': 'w4', 'inventory': {'b': 5, 'c': 5}},
                 {'name': 'w5', 'inventory': {'c': 5}}]
    return equals(expected, order, inventory)

def test8():
    """ Shipments with equal warehouses, prefer shipment with 'cheapest' warehouse """
    expected = [{'w1': {'a': 10}}, {'w4': {'b': 10}}]  # prefer [w1, w4] over [w2, w3]
    order = {'a': 10, 'b': 10}
    inventory = [{'name': 'w1', 'inventory': {'a': 10}},
                 {'name': 'w2', 'inventory': {'a': 9, 'b': 1}},
                 {'name': 'w3', 'inventory': {'a': 1, 'b': 9}},
                 {'name': 'w4', 'inventory': {'b': 10}}]
    return equals(expected, order, inventory)

# def test9():
#     """ Invalid order --> throws AssertionError """
#     testA = caughtAssertion({'apple': 'z'}, [])  # item amount in not an integer
#     testB = caughtAssertion({'apple': -1}, [])  # negative item amount
#     testC = caughtAssertion({1: 1}, [])  # item key should be a string
#     return testA and testB and testC
#
# def test10():
#     """ Invalid inventory --> throws AssertionError """
#     testA = caughtAssertion({}, [{'name': 'bad', 'inventory': 1}])  # invalid inventory
#     testB = caughtAssertion({}, [{'inventory': {'apple': 2}}])  # no name
#     testC = caughtAssertion({}, [{'name': 'w1', 'inventory': {'a': 5}}, {'name': 'w1', 'inventory': {'c': 4}}])  # warehouses should have unique name
#     return testA and testB and testC

if __name__ == '__main__':
    tests = [test0, test1, test2, test3, test4, test5, test6, test7, test8] #, test9, test10]
    for idx, test in enumerate(tests):
        print(f"Running test #{idx}... {'Pass' if test() else 'Fail'}")
