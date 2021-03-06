from typing import Dict, List, NewType, TypedDict

Items = NewType('Items', Dict[str, int])
Shipment = NewType('Shipment', Dict[str, Items])
class WareHouse(TypedDict):
    name: str
    inventory: Items

"""
ASSUMPTIONS:
    0. Clarification on inputs from engineer at Deliverr (Joshua Kastendick)
        - You can assume that the inputs passed to you are of the correct type (but could be empty).
        - Item quantities are non-negative; they can be 0 or positive, but not negative.
    1. Shipping from one warehouse is cheaper than multiple warehouses
    2. Number of items shipped from each warehouse does not affect the cost
    3. For shipments with same number of warehouses, return shipment that has the first cheaper warehouse not in the other shipments
        In other words, a greedy algorithm that ships as much inventory as possible from cheaper warehouses
        (ie. for inventory [w1, w2, w3, w4, w5], prefer shipment [w1, w4] over [w2, w3] and [w1, w2, w5] over [w1, w3, w4])
"""
def get_shipment(order: Items, inventory: List[WareHouse]) -> List[Shipment]:
    """
    Assumes order and inventory are of the correct type
    :param order: map of items being ordered + how many are ordered
    :param inventory: list of warehouse name and their respective item inventory amounts
    :return: cheapest shipment if it exists, else NO_SHIPMENT
    """
    NO_ITEMS, NO_SHIPMENT = {}, [] # predefined constants

    def dfs(this_order: Items, warehouse_idx: int):
        """
        DFS to traverse order/warehouse state space, using greedy method to complete shipments one warehouse at a time
        :param this_order: the current order to fulfill, must be non-empty
        :param warehouse_idx: idx of warehouse to first attempt to fill in inventory list
        :return: cheapest shipment, if shipment exists (otherwise no shipment)
        """
        assert this_order != NO_ITEMS, "predefined condition of parameter 'this_order'"
        if warehouse_idx == len(inventory): return NO_SHIPMENT # base case: no more warehouses

        warehouse = inventory[warehouse_idx] # the current warehouse
        foundItems = {} # greedy, grab max items from this warehouse to include in shipment
        next_order = {} # remaining items to ship after grabbing all possible from this warehouse
        for item, count in this_order.items():
            if item in warehouse['inventory']:
                stock = warehouse['inventory'][item] # item's available stock in this warehouse
                if count > stock:
                    next_order[item] = count - stock
                foundItems[item] = min(count, stock)
            else:
                next_order[item] = count

        include = [{warehouse['name']: foundItems}] # shipment that includes items from this warehouse
        if next_order == NO_ITEMS: return include # edge case, greedy: ship entire order from this warehouse (cheaper than any warehouse after)

        exclude = dfs(this_order, warehouse_idx + 1) # shipment that excludes items from this warehouse
        if foundItems == NO_ITEMS: return exclude # edge case, no items in order can be shipped from this warehouse

        shipment = dfs(next_order, warehouse_idx + 1) # shipment based on remaining items to ship with the rest of the warehouses (of higher cost)
        if shipment == NO_SHIPMENT: return exclude # edge case, if no shipment possible that includes this warehouse and remaining items

        include += shipment # append shipments from remaining (higher cost) warehouses to shipment from this warehouse
        if exclude == NO_SHIPMENT: return include # edge case, if no shipment possible without using this warehouse

        return min(include, exclude, key=len) # return the shipment with less warehouses (if equal, prefer shipment that includes this warehouse)

    order = {k:v for k,v in order.items() if v>0} # ignore items with non-positive amount
    if order == NO_ITEMS: return NO_SHIPMENT # edge case, empty order

    output = dfs(order, 0)
    output.sort(key = lambda shipment: next(iter(shipment)))  # sort shipment list by warehouse name
    return output
