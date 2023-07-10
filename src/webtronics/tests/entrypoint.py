import sys

import pytest


def main():
    sys.exit(
        pytest.main(
            [
                '-x',
                './',
                '--cov=webtronics',
                '-o',
                'log-cli=true',
                '--asyncio-mode=auto',
            ]
        )
    )
