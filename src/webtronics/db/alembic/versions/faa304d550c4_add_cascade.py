"""Add cascade

Revision ID: faa304d550c4
Revises: af4d214f3013
Create Date: 2023-07-10 10:50:48.276399
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'faa304d550c4'
down_revision = 'af4d214f3013'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'posts', 'author_id', existing_type=sa.INTEGER(), nullable=False
    )
    op.drop_constraint('posts_author_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(
        None, 'posts', 'users', ['author_id'], ['id'], ondelete='CASCADE'
    )
    op.drop_constraint(
        'reactions_post_id_fkey', 'reactions', type_='foreignkey'
    )
    op.drop_constraint(
        'reactions_user_id_fkey', 'reactions', type_='foreignkey'
    )
    op.create_foreign_key(
        None, 'reactions', 'users', ['user_id'], ['id'], ondelete='CASCADE'
    )
    op.create_foreign_key(
        None, 'reactions', 'posts', ['post_id'], ['id'], ondelete='CASCADE'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        'reactions_user_id_fkey', 'reactions', type_='foreignkey'
    )
    op.drop_constraint(
        'reactions_post_id_fkey', 'reactions', type_='foreignkey'
    )
    op.create_foreign_key(
        'reactions_user_id_fkey', 'reactions', 'users', ['user_id'], ['id']
    )
    op.create_foreign_key(
        'reactions_post_id_fkey', 'reactions', 'posts', ['post_id'], ['id']
    )
    op.drop_constraint('posts_author_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(
        'posts_author_id_fkey', 'posts', 'users', ['author_id'], ['id']
    )
    op.alter_column(
        'posts', 'author_id', existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###
