def ft_count_harvest_recursive():
    x = int(input("Days until harvest: "))
    helper(1, x)


def helper(i, x):
    if i > x:
        print("Harvest time!")
        return
    print("Day", i)
    helper(i + 1, x)
