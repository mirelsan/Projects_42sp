import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        raw = input("Enter new coordinates as floats in format 'x,y,z': ")
        parts = raw.split(",")
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        try:
            return float(parts[0]), float(parts[1]), float(parts[2])
        except ValueError as e:
            print(f"Error on parameter: {e}")


def distance(p1: tuple[float, float, float],
             p2: tuple[float, float, float]) -> float:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return math.sqrt(dx**2 + dy**2 + dz**2)


def main() -> None:
    print("=== Game Coordinate System ===")
    print("\nGet a first set of coordinates")
    pos1 = get_player_pos()
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")
    d_center = distance((0.0, 0.0, 0.0), pos1)
    print(f"Distance to center: {round(d_center, 4)}")

    print("\nGet a second set of coordinates")
    pos2 = get_player_pos()
    d_between = distance(pos1, pos2)
    print(f"Distance between the 2 sets of coordinates: {round(d_between, 4)}")


if __name__ == "__main__":
    main()
