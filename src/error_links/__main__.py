import argparse
import pathlib
import site
import sys

from rich import print


def get_location():
    sitepackages = site.getsitepackages()
    if not sitepackages:
        print("[red bold]❗️ Failed to locate site-packages directory.[/]")
        sys.exit(0)

    location = pathlib.Path(sitepackages[0]) / "sitecustomize.py"
    return location


def where():
    location = get_location()
    print(f"📁 Installation location is [blue]{location}[/]")


def install(use_emoji, show_text):
    file = get_location()
    file.touch(exist_ok=True)
    contents = file.read_text()

    mark = "# error-links auto-installation:\n"
    new_contents = (
        contents
        + "\n"
        + mark
        + "from error_links import install\n"
        + f"install(use_emoji={use_emoji}, show_text={show_text})\n"
    )
    file.write_text(new_contents)
    print("🔧 [green]error-links installed successfully")

    if (count := new_contents.count(mark)) > 1:
        print(f"[yellow]⚠️ error-links has {count} installations")


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")
    install_parser = subparsers.add_parser("install", help="Install error links")
    install_parser.add_argument(
        "--use-emoji", choices=[True, False], type=bool, default=True
    )
    install_parser.add_argument(
        "--show-text", choices=[True, False], type=bool, default=True
    )
    _ = subparsers.add_parser("where", help="Where the installation will take place")

    args = parser.parse_args()
    if args.command == "install":
        install(args.use_emoji, args.show_text)
    elif args.command == "where":
        where()


if __name__ == "__main__":
    main()


def run():
    main()


if __name__ == "__main__":
    run()
