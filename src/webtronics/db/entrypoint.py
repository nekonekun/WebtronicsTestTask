"""Alembic helper script"""
import os
import sys
from pathlib import Path

from alembic.config import CommandLine, Config

PROJECT_PATH = Path(__file__).parent.parent.resolve()


def main():
    """Alembic entrypoint"""
    alembic = CommandLine()
    alembic.parser.add_argument(
        '--database',
        default=os.getenv('WT_DATABASE_URL'),
        help='Database URL [env var: WT_DATABASE_URL]',
    )

    options = alembic.parser.parse_args()
    if not os.path.isabs(options.config):
        options.config = os.path.join(PROJECT_PATH, options.config)

    config = Config(
        file_=options.config, ini_section=options.name, cmd_opts=options
    )

    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            'script_location', os.path.join(PROJECT_PATH, alembic_location)
        )

    config.set_main_option('sqlalchemy.url', options.database)

    sys.exit(alembic.run_cmd(config, options))
