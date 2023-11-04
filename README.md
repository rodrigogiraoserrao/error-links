# `error-links`

`error-links` adds Google and Python documentation links to the bottom of exceptions.

![](https://raw.githubusercontent.com/rodrigogiraoserrao/error-links/main/error_links.png)

In most terminals, you will need to hold <kbd>Cmd</kbd> or <kbd>Ctrl</kbd> to allow _clicking_ the link.

This works really well alongside [Rich's traceback handler](https://rich.readthedocs.io/en/stable/traceback.html#traceback-handler), which is what enabled the highlighting and coloured output in the screenshot above.


## Usage

To use this package, simply install it with `python -m pip install error_links`.
Then, install the error links with

```py
from error_links import install
install()
```

You can control whether to show the emoji or the text with the `install` keyword arguments `use_emoji` and `show_text`, respectively.
For example, `install(show_text=False)` will use only the emoji for the link.

You can switch from Google to DuckDuckGo by specifying `search_engine="duckduckgo"`.
More search engines _may_ be supported in the future if you make a PR or [request it](https://github.com/rodrigogiraoserrao/error-links/issues/new).


## Install automatically

You can use the command `error-links install` to install error links automatically.
This will modify the file `sitecustomize.py` in your directory `site-packages`.

To see where the installation was made, you can use the command `error-links where`.

If you want error links in the REPL automatically as well, you can [read this article on how to run custom Python code on REPL startup](https://mathspp.com/blog/til/customise-the-repl-on-start-up).
