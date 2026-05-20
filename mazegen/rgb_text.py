
RESET = "\033[0m"


def rgb_text(text: str, r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m{text}{RESET}"


def get_rgb_value(name: str) -> int:
    while True:
        pigment: str = input(f"Enter {name} value (0-255): ").strip()
        if not pigment.isdigit():
            print("Enter a valid integer.")
            continue
        value: int = int(pigment)
        if 0 <= value <= 255:
            return value
        print("Value must be between 0-255.")
