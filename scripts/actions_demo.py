import argparse
import platform
import sys
import time


def main() -> int:
    parser = argparse.ArgumentParser(description="Tiny script used by Actions demo workflow")
    parser.add_argument("--sleep", default="5", help="Seconds to sleep")
    parser.add_argument("--message", default="", help="Message to print")
    parser.add_argument("--matrix-os", default="", help="Matrix OS label")
    parser.add_argument("--python", dest="python_version", default="", help="Matrix Python version")
    args = parser.parse_args()

    try:
        sleep_seconds = float(args.sleep)
    except ValueError:
        print(f"Invalid --sleep value: {args.sleep}", file=sys.stderr)
        return 2

    print("actions_demo.py running")
    print(f"message: {args.message}")
    print(f"matrix.os: {args.matrix_os}")
    print(f"matrix.python: {args.python_version}")
    print(f"runner.platform: {platform.platform()}")

    time.sleep(max(0.0, sleep_seconds))
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
