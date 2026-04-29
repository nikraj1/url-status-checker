import requests
import argparse
import time

# Optional color support
try:
    from colorama import Fore, Style, init
    init()
    COLOR = True
except:
    COLOR = False


def print_colored(text, color):
    if COLOR:
        print(color + text + Style.RESET_ALL)
    else:
        print(text)


def check_url(url, timeout=5):
    try:
        start = time.time()
        response = requests.get(url, timeout=timeout)
        elapsed = round((time.time() - start) * 1000, 2)  # ms

        return {
            "url": url,
            "status": response.status_code,
            "time": elapsed
        }

    except requests.exceptions.RequestException:
        return {
            "url": url,
            "status": "ERROR",
            "time": None
        }


def load_urls(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        print("Error reading file")
        return []


def main():
    parser = argparse.ArgumentParser(description="URL Status Checker")
    parser.add_argument("--url", help="Single URL to check")
    parser.add_argument("--file", help="File containing list of URLs")
    parser.add_argument("--timeout", type=int, default=5, help="Request timeout (seconds)")
    parser.add_argument("--output", help="Save results to file")

    args = parser.parse_args()

    urls = []

    if args.url:
        urls.append(args.url)

    if args.file:
        urls.extend(load_urls(args.file))

    if not urls:
        print("Please provide --url or --file")
        return

    results = []

    print("\nChecking URLs...\n")

    for url in urls:
        result = check_url(url, args.timeout)
        results.append(result)

        if result["status"] == "ERROR":
            print_colored(f"{url} -> ERROR", Fore.RED)
        elif result["status"] == 200:
            print_colored(f"{url} -> {result['status']} ({result['time']} ms)", Fore.GREEN)
        else:
            print_colored(f"{url} -> {result['status']} ({result['time']} ms)", Fore.YELLOW)

    if args.output:
        with open(args.output, "w") as f:
            for r in results:
                f.write(f"{r['url']},{r['status']},{r['time']}\n")

        print_colored(f"\nResults saved to {args.output}", Fore.CYAN)


if __name__ == "__main__":
    main()