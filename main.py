from calculator import add, divide, multiply, power, subtract


def main():
    add_result = add(5, 3)
    print(f"The result of addition is: {add_result}")
    sub_result = subtract(5, 3)
    print(f"The result of subtraction is: {sub_result}")
    mul_result = multiply(5, 3)
    print(f"The result of multiplication is: {mul_result}")
    div_result = divide(5, 2)
    print(f"The result of division is: {div_result}")
    power_result = power(2, 3)
    print(f"The result of power is: {power_result}")


if __name__ == "__main__":
    main()
