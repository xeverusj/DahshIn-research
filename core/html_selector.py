"""
core/html_selector.py — Inhouse HTML parsing with CSS selector support.

Implements a Parsel-compatible API using lxml and cssselect directly —
the same underlying libraries that Scrapling itself uses, with no
external scraping framework dependency.

Supported:
  Selector(html_string)          — parse HTML
  .css('selector')               — CSS selection → SelectorList of Selector objects
  .css('selector::text')         — text content of each match
  .css('selector::attr(name)')   — attribute value of each match
  .css('*::text')                — all text nodes in subtree
  .find_all('tag')               — iterate all elements with tag
  .get(default=None)             — first result or default
  .getall()                      — all results as list of strings
  .html                          — outer HTML of element (property)
"""

import re

try:
    import lxml.html
    import lxml.etree
    _LXML_AVAILABLE = True
except ImportError:
    _LXML_AVAILABLE = False


class SelectorList(list):
    """List of results with Parsel-compatible .get() / .getall() helpers."""

    def get(self, default=None):
        """Return first item or default if empty."""
        return self[0] if self else default

    def getall(self):
        """Return all items as a plain list."""
        return list(self)


class Selector:
    """
    Thin CSS-selector wrapper around lxml.html.

    Mirrors the Scrapling / Parsel Selector API so scrapers can be written
    once and remain portable whether lxml is available or not.
    """

    # Compile once — match e.g. "div.card::text"  or  "a::attr(href)"
    _RE_TEXT = re.compile(r'^(.*?)::text$', re.DOTALL)
    _RE_ATTR = re.compile(r'^(.*?)::attr\(([^)]+)\)$', re.DOTALL)

    def __init__(self, source):
        """
        Accept either an HTML string or a raw lxml element.
        If lxml is not installed the object is inert (all queries return empty).
        """
        self._el = None
        if not _LXML_AVAILABLE:
            return
        if isinstance(source, str):
            try:
                self._el = lxml.html.fromstring(source)
            except Exception:
                pass
        elif source is not None:
            # Already an lxml element — wrap directly
            self._el = source

    # ── Public API ────────────────────────────────────────────────────────────

    @property
    def html(self) -> str:
        """Outer HTML of the wrapped element, or empty string."""
        if self._el is None:
            return ''
        try:
            return lxml.html.tostring(self._el, encoding='unicode')
        except Exception:
            return ''

    def css(self, query: str) -> SelectorList:
        """
        Run a CSS selector query with optional ::text / ::attr() pseudo-elements.

        Returns a SelectorList of:
          - strings  when ::text or ::attr() is used
          - Selector objects  otherwise (each wrapping a matched element)
        """
        if self._el is None:
            return SelectorList()

        text_m = self._RE_TEXT.match(query)
        attr_m = self._RE_ATTR.match(query)

        if text_m:
            base = text_m.group(1).strip()
            elements = self._select(base)
            results = []
            for el in elements:
                t = self._text(el)
                if t:
                    results.append(t)
            return SelectorList(results)

        if attr_m:
            base = attr_m.group(1).strip()
            attr_name = attr_m.group(2).strip()
            elements = self._select(base)
            results = []
            for el in elements:
                val = el.get(attr_name, '')
                if val:
                    results.append(val)
            return SelectorList(results)

        # Plain selector — return Selector wrappers
        elements = self._select(query)
        return SelectorList([Selector(el) for el in elements])

    def find_all(self, tag: str) -> SelectorList:
        """
        Iterate all descendant elements with the given tag name.
        Equivalent to lxml element.iter(tag).
        """
        if self._el is None:
            return SelectorList()
        try:
            return SelectorList([Selector(el) for el in self._el.iter(tag)])
        except Exception:
            return SelectorList()

    def get(self, default=None):
        """Return outer HTML of this element, or default."""
        h = self.html
        return h if h else default

    def getall(self) -> list:
        """Return [outer_html] for this single element (list for API compat)."""
        h = self.html
        return [h] if h else []

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _select(self, selector: str) -> list:
        """Run a CSS selector and return a list of lxml elements."""
        if self._el is None:
            return []
        # Empty / wildcard — return all descendants
        if not selector or selector.strip() == '*':
            try:
                return list(self._el.iter())
            except Exception:
                return []
        try:
            return self._el.cssselect(selector)
        except Exception:
            return []

    @staticmethod
    def _text(element) -> str:
        """Return all text content of an lxml element, stripped."""
        try:
            return (element.text_content() or '').strip()
        except Exception:
            return ''
