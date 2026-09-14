from function.add import add
from function.subtract import subtract


def main():
    add_result = add(5, 3)
    print(f"The result of addition is: {add_result}")
    sub_result = subtract(5, 3)
    print(f"The result of subtraction is: {sub_result}")


if __name__ == "__main__":
    main()
