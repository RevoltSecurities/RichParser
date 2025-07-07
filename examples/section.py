# examples/sectioned_cli.py

from richparser import RichParser

def main():
    cli = RichParser(description="CLI with Help Sections Example")

    cli.add_argument("input", "-u", "--url", type=str, help="Target URL to scan")
    cli.add_argument("config", "-t", "--timeout", type=int, default=5, help="Request timeout in seconds")
    cli.add_argument("flags", "-v", "--verbose", action="store_true", help="Enable verbose output")

    args = cli.parse_args()
    print("[+] Running scan on:", args.url)
    print("[+] Timeout:", args.timeout)
    print("[+] Verbose:", args.verbose)

if __name__ == "__main__":
    main()
