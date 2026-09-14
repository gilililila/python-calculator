from function.add import add
from function.subtract import subtract
from function.multiply import multiply


def main():
    add_result = add(5, 3)
    print(f"The result of addition is: {add_result}")
    sub_result = subtract(5, 3)
    print(f"The result of subtraction is: {sub_result}")
    mul_result = multiply(5, 3)
    print(f"The result of multiplication is: {mul_result}")


if __name__ == "__main__":
    main()
