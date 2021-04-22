import sys
from command_line_main import main as cmd_main
from flask_main import main as flsk_main

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print(f"USAGE: {sys.argv[0]} <mode> <...>")
        print("Modes: \n"
              "-c Command line mode\n"
              "-w WWW mode\n")
        sys.exit()
    if sys.argv[1] == "-c":
        cmd_main()
    elif sys.argv[1] == "-w":
        flsk_main()
    else:
        print(f"Unknown option {sys.argv[1]}")

