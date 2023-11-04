import argparse
import pathlib
import site
import sys

from rich import print

from error_links import SUPPORTED_SEARCH_ENGINES


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


def install(use_emoji, show_text, search_engine):
    if not use_emoji and not show_text:
        print("[red bold]❗️ One of --use-emoji or --show-text must be True")

    file = get_location()
    file.touch(exist_ok=True)
    contents = file.read_text()

    mark = "# error-links auto-installation:\n"
    new_contents = (
        contents
        + "\n"
        + mark
        + "from error_links import install\n"
        + f"install(use_emoji={use_emoji}, show_text={show_text}, search_engine={search_engine!r})\n"
    )
    file.write_text(new_contents)
    print("🔧 [green]error-links installed successfully")

    if (count := new_contents.count(mark)) > 1:
        print(f"[yellow]⚠️ error-links has {count} installations")


def main():
    parser = argparse.ArgumentParser()

    # type=bool doesn't work in add_argument because `bool("False")` is... True!
    to_bool = lambda v: v if v not in {"True", "False"} else eval(v)

    subparsers = parser.add_subparsers(dest="command")
    install_parser = subparsers.add_parser("install", help="install error links")
    install_parser.add_argument(
        "--use-emoji",
        choices=[True, False],
        help="whether to use emoji in the links",
        default=True,
        type=to_bool,
    )
    install_parser.add_argument(
        "--show-text",
        choices=[True, False],
        type=to_bool,
        help="whether to show the link text",
        default=True,
    )
    install_parser.add_argument(
        "--search-engine",
        choices=SUPPORTED_SEARCH_ENGINES,
        default="google",
        help="search engine to use",
    )
    _ = subparsers.add_parser("where", help="where the installation will take place")

    args = parser.parse_args()
    if args.command == "install":
        install(args.use_emoji, args.show_text, args.search_engine)
    elif args.command == "where":
        where()


if __name__ == "__main__":
    main()


def run():
    main()


if __name__ == "__main__":
    run()
