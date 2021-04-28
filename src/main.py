import sys
from cli.main import main as cli_main
from flsk.main import main as flask_main
import argparse
"""
Entry point. Application can run in two modes - interactive command line mode and web mode using Flask framework."
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="Command line mode", action="store_true")
    parser.add_argument("-s", help="Server mode", action="store_true")
    args = parser.parse_args()
    if args.s:
        flask_main()
    elif args.c:
        cli_main()
    else:
        print(f"Unknown option {sys.argv[1]}")

