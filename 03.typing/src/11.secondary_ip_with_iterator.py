import re
from collections.abc import Iterator
from textwrap import dedent


def get_ip(config: str) -> Iterator[tuple[str, str, bool]]:
    pattern = re.compile(
        pattern=r"ip address (?P<address>\S+) (?P<netmask>\S+)(?P<secondary> secondary)?",
    )
    for m in pattern.finditer(config):
        yield (
            m.group("address"),
            m.group("netmask"),
            bool(m.group("secondary")),
        )


if __name__ == "__main__":
    config = dedent(
        """
        interface GigabitEthernet0/1
         description test
         ip address 192.168.0.1 255.255.255.0
         ip address 192.168.1.1 255.255.255.0 secondary
         load-interval 30
        """,
    )

    for ip in get_ip(config):
        print(ip)
