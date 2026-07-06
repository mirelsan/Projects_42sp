def ft_plant_age():
    x = int(input("Enter plant age in days: "))
    if x > 60:
        print("Plant is ready to harvest!")
    else:
        print("Plant needs more time to grow")