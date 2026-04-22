def ft_count_harvest_recursive():
    n = int(input("Days until harvest: "))

    def _print_day(current, stop):
        if current > stop:
            print("Harvest time!")
            return
        print(f"Day {current}")
        _print_day(current + 1, stop)

    _print_day(1, n)
