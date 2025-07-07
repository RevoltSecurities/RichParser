# examples/basic_cli.py

from richparser import RichParser

def main():
    parser = RichParser(description="Basic CLI Example without subcommands")

    parser.add_argument("input", "-i", "--input", type=str, help="Input file path")
    parser.add_argument("output", "-o", "--output", type=str, help="Output file path")
    parser.add_argument("config", "-t", "--threads", type=int, default=4, help="Number of threads to use")
    parser.add_argument("flags", "-v", "--verbose", action="store_true", help="Enable verbose mode")

    args = parser.parse_args()

    print(f"[+] Input: {args.input}")
    print(f"[+] Output: {args.output}")
    print(f"[+] Threads: {args.threads}")
    print(f"[+] Verbose: {args.verbose}")

if __name__ == "__main__":
    main()
