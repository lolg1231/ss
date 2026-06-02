"""
Xbox Autoclaimer - Main Entry Point
"""
import sys
import argparse
import os

def main():
    parser = argparse.ArgumentParser(
        description="Xbox Gamertag Autoclaimer"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in CLI mode instead of GUI"
    )
    
    args = parser.parse_args()
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    if args.cli:
        from claimer import XboxAutoclaimer
        print("\\n" + "="*60)
        print("  🎮 Xbox Autoclaimer - CLI Mode")
        print("="*60 + "\\n")
        
        claimer = XboxAutoclaimer()
        
        try:
            claimer.run()
        except KeyboardInterrupt:
            print("\\n[*] Interrupted by user")
            claimer.stop()
    else:
        try:
            from gui import main as gui_main
            gui_main()
        except ImportError:
            print("[-] GUI not available. Install tkinter or run with --cli")
            sys.exit(1)


if __name__ == "__main__":
    main()
