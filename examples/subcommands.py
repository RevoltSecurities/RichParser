# examples/with_subcommands.py

from richparser import RichParser

def main():
    cli = RichParser(description="CLI with Subcommands Example")

    # Global options
    cli.add_argument("global", "-v", "--verbose", action="store_true", help="Enable verbose mode")
    cli.add_argument("global", "-c", "--config", type=str, help="Path to config file")

    # Subcommand: greet
    greet_parser, _ = cli.add_subcommand("greet", "Greet someone with a message")
    cli.add_subcommand_argument("greet", "greet", "-n", "--name", type=str, required=True, help="Name of the person")
    cli.add_subcommand_argument("greet", "greet", "-m", "--message", type=str, default="Hello", help="Greeting message")

    # Subcommand: calc
    calc_parser, _ = cli.add_subcommand("calc", "Basic calculator")
    cli.add_subcommand_argument("calc", "math", "-a", type=int, required=True, help="Operand A")
    cli.add_subcommand_argument("calc", "math", "-b", type=int, required=True, help="Operand B")
    cli.add_subcommand_argument("calc", "math", "--add", action="store_true", help="Add the operands")
    cli.add_subcommand_argument("calc", "math", "--mul", action="store_true", help="Multiply the operands")

    args = cli.parse_args()

    if hasattr(args, "mode"):
        if args.mode == "greet":
            print(f"{args.message}, {args.name}!")
        elif args.mode == "calc":
            if args.add:
                print(f"[+] {args.a} + {args.b} = {args.a + args.b}")
            elif args.mul:
                print(f"[+] {args.a} * {args.b} = {args.a * args.b}")
            else:
                print("[-] Please specify an operation: --add or --mul")
    else:
        print("[*] No subcommand provided. Use --help for options.")

if __name__ == "__main__":
    main()
