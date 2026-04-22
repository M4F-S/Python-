import sys


if __name__ == "__main__":
    print("=== Inventory System Analysis ===")
    inventory: dict[str, int] = {}

    for token in sys.argv[1:]:
        if ":" not in token:
            print(f"Error - invalid parameter '{token}'")
            continue
        name, _, qty_str = token.partition(":")
        if name == "" or qty_str == "":
            print(f"Error - invalid parameter '{token}'")
            continue
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            qty = int(qty_str)
        except ValueError as e:
            print(f"Quantity error for '{name}': {e}")
            continue
        inventory.update({name: qty})

    print(f"Got inventory: {inventory}")
    if len(inventory) == 0:
        print("Your inventory is empty ;)")
    else:
        item_list = list(inventory.keys())
        print(f"Item list: {item_list}")
        total = sum(inventory.values())
        print(f"Total quantity of the {len(inventory)} items: {total}")

        for name in inventory.keys():
            pct = round(inventory[name] / total * 100, 1)
            print(f"Item {name} represents {pct}%")

        most_name = item_list[0]
        least_name = item_list[0]
        for name in item_list:
            if inventory[name] > inventory[most_name]:
                most_name = name
            if inventory[name] < inventory[least_name]:
                least_name = name
        print(f"Item most abundant: {most_name} with "
              f"quantity {inventory[most_name]}")
        print(f"Item least abundant: {least_name} with "
              f"quantity {inventory[least_name]}")

        inventory.update({"magic_item": 1})
        print(f"Updated inventory: {inventory}")
