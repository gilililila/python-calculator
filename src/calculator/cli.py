import os
import sys

from calculator import add, divide, multiply, power, subtract

OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "**": power,
}

# ANSI 颜色
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    DIM    = "\033[2m"
    CYAN   = "\033[36m"
    BCYAN  = "\033[96m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    MAGENTA= "\033[95m"
    BLUE   = "\033[94m"

def _supports_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("TERM") != "dumb"

def _c(text: str, *codes: str) -> str:
    if not _supports_color():
        return text
    return "".join(codes) + text + C.RESET


def display_menu():
    """Display the calculator menu — the badass edition."""
    banner = r"""
   ██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗
   ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║
   ██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║
   ██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║
   ██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║
   ╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                ⚔  C A L C U L A T O R  ⚔
"""

    op_line = (
        f"   {_c('+', C.BOLD, C.BCYAN)}  add      "
        f"{_c('-', C.BOLD, C.BCYAN)}  sub      "
        f"{_c('*', C.BOLD, C.BCYAN)}  mul      "
        f"{_c('/', C.BOLD, C.BCYAN)}  div      "
        f"{_c('**', C.BOLD, C.MAGENTA)} power"
    )

    hint = _c("  [ q / quit ]  to leave the arena", C.DIM)
    line = _c("  " + "═" * 62, C.BLUE)

    print(_c(banner, C.BOLD, C.CYAN))
    print(line)
    print(op_line)
    print(hint)
    print(line)

def get_number(prompt):
    """Prompt user for a number and return it."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    """Main REPL loop for the calculator."""
    display_menu()

    while True:
        operation = input("Enter operation (+, -, *, /, **, or quit): ").strip()

        if operation.lower() in ("quit", "q"):
            print("Goodbye!")
            break

        if operation not in OPERATIONS:
            print(f"Unknown operation: '{operation}'. Please try again.")
            continue

        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")

        try:
            result = OPERATIONS[operation](a, b)
            print(f"\n  {a} {operation} {b} = {result}\n")
        except (ValueError, TypeError) as e:
            print(f"\n  Error: {e}\n")


if __name__ == "__main__":
    main()
