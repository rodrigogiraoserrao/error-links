import sys


SUPPORTED_SEARCH_ENGINES = {"google", "duckduckgo"}
SEARCH_ENGINE_QUERY_LINK = "[link=https://www.{search_engine}.com/search?q={exctype}+{excvalue}]{link_text}[/link]"


def install(*, use_emoji=True, show_text=True, search_engine="google"):
    hook = sys.excepthook

    if not use_emoji and not show_text:
        raise RuntimeError("Need to use emoji or show text.")

    search_engine = search_engine.casefold()
    if search_engine not in SUPPORTED_SEARCH_ENGINES:
        raise RuntimeError(
            f"Search engine {search_engine!r} not supported."
            + f"Use {' or '.join(SUPPORTED_SEARCH_ENGINES)}"
        )

    def custom_hook(exctype, excvalue, traceback):
        return_value = hook(exctype, excvalue, traceback)

        try:
            import builtins
            from rich import print
            from urllib.parse import quote

            exception_name = exctype.__name__
            str_exception_type = quote(str(exception_name))
            str_exception_value = quote(str(excvalue))

            search_link_parts = []
            docs_link_parts = []
            if use_emoji:
                search_link_parts.append("🔍")
                docs_link_parts.append("📚")
            if show_text:
                search_link_parts.append(
                    "Search this error"
                    if search_engine != "google"
                    else "Google this error"
                )
                docs_link_parts.append("Python docs")

            search_link_text = " ".join(search_link_parts)
            docs_link_text = " ".join(docs_link_parts)

            search_link = SEARCH_ENGINE_QUERY_LINK.format(
                search_engine=search_engine,
                exctype=str_exception_type,
                excvalue=str_exception_value,
                link_text=search_link_text,
            )
            links = [search_link]

            # Check if this is a built-in exception.
            import builtins

            if exception_name in dir(builtins):
                python_search_link = (
                    "[link=https://docs.python.org/3/library/exceptions.html#"
                    + f"{str_exception_type}]{docs_link_text}[/link]"
                )
                links.append(python_search_link)

            print(" | ".join(links))
        except Exception:  # If _anything_ happens, we do nothing.
            pass

        return return_value

    sys.excepthook = custom_hook
