from html.parser import HTMLParser
from io import StringIO
from sys import stdout
from typing import IO, Callable, Dict, List, Optional, Tuple

from dinject.inject import Reader

from edition.html import get_css
from edition.metadata import Metadata

TAttribute = Tuple[str, Optional[str]]


class EditionHtmlRenderer(HTMLParser):
    def __init__(
        self,
        metadata: Optional[Metadata] = None,
        toc_writer: Optional[Callable[[IO[str]], None]] = None,
    ) -> None:
        super().__init__()
        self._metadata = metadata
        self._toc_writer = toc_writer
        self._writer: IO[str] = stdout
        self._last_data: str = ""

    def handle_comment(self, data: str) -> None:
        """
        Handles HTML comments encountered in the feed.
        """

        # We intentionally pass comments through since they could be present
        # inside Markdown code blocks. We only escape the brackets to ensure the
        # comments make it through subsequent HTML processing.
        self._writer.write("&lt;!--")
        self._writer.write(data)
        self._writer.write("--&gt;")

    def handle_data(self, data: str) -> None:
        self._writer.write(data)
        self._last_data = data

    def handle_decl(self, decl: str) -> None:
        self._writer.write(f"<!{decl}>")

    def handle_endtag(self, tag: str) -> None:
        self._writer.write(f"</{tag}>")

    def _get_attrs(self, attrs: List[TAttribute]) -> Dict[str, str]:
        wip: Dict[str, str] = {}
        for a in attrs:
            wip[str(a[0])] = str(a[1])
        return wip

    def _get_value(self, key: str) -> str:
        if not self._metadata:
            return ""

        if key == "favicon-href":
            if emoji := self._get_value("favicon-emoji"):
                return f"data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>{emoji}</text></svg>"
            return ""

        if key == "toc":
            if not self._toc_writer:
                raise Exception("no toc writer")
            writer = StringIO()
            self._toc_writer(writer)
            return writer.getvalue().rstrip()

        value = str(self._metadata.get(key, ""))
        if not value:
            print(f'warning: no value for "{key}"')
        return value

    def handle_startendtag(self, tag: str, attrs: List[TAttribute]) -> None:
        edition_attrs = self._get_attrs(attrs)

        if tag == "edition":
            if "value" in edition_attrs:
                value = self._get_value(edition_attrs["value"])
                element = edition_attrs.get("element", None)
                if element:
                    self._writer.write("<")
                    self._writer.write(element)
                    self._writer.write(">")
                    self._writer.write(value)
                    self._writer.write("</")
                    self._writer.write(element)
                    self._writer.write(">")
                else:
                    self._writer.write(value)
                return

        if if_key := edition_attrs.get("edition-if", None):
            if_value = self._get_value(if_key)
            if not if_value:
                # Don't write anything:
                return

        attributes = self.make_attributes(attrs) if attrs else ""
        inner = f"{tag} {attributes}".strip()
        self._writer.write(f"<{inner} />")

    def handle_starttag(self, tag: str, attrs: Optional[List[TAttribute]]) -> None:
        attributes = self.make_attributes(attrs) if attrs else ""
        inner = f"{tag} {attributes}".strip()
        self._writer.write(f"<{inner}>")

    def make_attribute(self, attribute: TAttribute) -> str:
        if attribute[0].startswith("edition-"):
            key_suffix = attribute[0][8:]
            if key_suffix == "if":
                return ""
            metadata_key = str(attribute[1])
            attribute = (
                key_suffix,
                str(self._get_value(metadata_key)),
            )
        return f'{attribute[0]}="{attribute[1]}"'

    def make_attributes(self, attributes: List[TAttribute]) -> str:
        return " ".join([self.make_attribute(a) for a in attributes])

    def _set_default_metadata(self) -> None:
        if not self._metadata:
            return None
        with get_css() as f:
            existing_css = str(self._metadata.get("css", ""))
            new_css = f.read()
            if new_css not in existing_css:
                self._metadata["css"] = existing_css + "\n" + new_css

    def render(self, reader: Reader, writer: IO[str]) -> None:
        self._set_default_metadata()
        self._writer = writer

        if isinstance(reader, str):
            reader = StringIO(reader)

        for line in reader:
            self.feed(line)

        self.close()
