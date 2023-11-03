import sys


def install(*, use_emoji=True, show_text=True):
    hook = sys.excepthook

    if not use_emoji and not show_text:
        raise RuntimeError("Need to use emoji or show text.")

    def custom_hook(exctype, excvalue, traceback):
        return_value = hook(exctype, excvalue, traceback)

        try:
            import builtins
            from rich import print
            from urllib.parse import quote

            exception_name = exctype.__name__
            str_exception_type = quote(str(exception_name))
            str_exception_value = quote(str(excvalue))

            google_link_parts = []
            docs_link_parts = []
            if use_emoji:
                google_link_parts.append("🔍")
                docs_link_parts.append("📚")
            if show_text:
                google_link_parts.append("Google this error")
                docs_link_parts.append("Python docs")

            google_link_text = " ".join(google_link_parts)
            docs_link_text = " ".join(docs_link_parts)

            google_search_link = (
                "[link=https://www.google.com/search?q="
                + f"{str_exception_type}+{str_exception_value}]"
                + f"{google_link_text}[/link]"
            )
            links = [google_search_link]

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
