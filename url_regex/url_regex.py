import re

from . import tlds

tlds_sort = "|".join([g for g in sorted(tlds.tlds_list)])


class Url:
    def __init__(self, full: str, domain: str, protocol: str = None):
        self.full = full
        self.domain = domain
        self.protocol = protocol

    def __repr__(self):
        return '<Url full={0.full} domain={0.domain} protocol={0.protocol}'.format(self)


class UrlRegex:
    def __init__(self, input: str, strict: bool = True):
        self.strict = strict
        self.input = input

        buildReg = self.build_regex
        self.regex = buildReg
        self.links_found = {}

    @property
    def build_regex(self):
        protocol = f"(?:(?:[a-z]+:)?//){'?' if self.strict else ''}"
        auth = "(?:\\S+(?::\\S*)?@)?"
        host = "(?:(?:[a-z\\u00a1-\\uffff0-9][-_]*)*[a-z\\u00a1-\\uffff0-9]+)"
        domain = "(?:\\.(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)*"
        tld = "(?:\\.{})\\.?".format('(?:[a-z\\u00a1-\\uffff]{2,})' if self.strict else f"(?:{tlds_sort})")
        port = "(?::\\d{2,5})?"
        path = '(?:[/?#][^\\s,.\"]*)?'

        regex = f"(?:({protocol}|www\\.)){auth}(?:(localhost|{host}{domain}{tld}))({port}{path})"
        return regex

    @property
    def debug(self):
        """ Check out how the script handles everything """
        all_groups = []
        find_all = re.search(self.regex, self.input.lower())
        for g in range(20):
            try:
                all_groups.append(find_all.group(g))
            except IndexError:
                break

        output = [
            str(" ".join([g for g in all_groups])),
            str(self.links)
        ]

        print("".join(output))

    @property
    def detect(self):
        """ Checks if string includes one or more links """
        return re.search(self.regex, self.input.lower()) is not None

    @property
    def links(self):
        """ Displays links in a pretty format """
        regex = re.findall(self.regex, self.input.lower())

        for i, g in enumerate(regex):
            self.links_found[i] = Url(
                f"{g[0]}{g[1]}{g[2]}",  # Full domain
                g[1],  # Domain
                g[0] if g[0] else None  # Protocol
            )

        return list(self.links_found.values())
