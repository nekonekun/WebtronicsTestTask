"""Initial

Revision ID: 943f3dbe95ab
Revises:
Create Date: 2023-07-07 22:10:04.029884
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '943f3dbe95ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )


def downgrade() -> None:
    op.drop_table('users')
