"""add users reference to posts

Revision ID: 04d79a4cf5e6
Revises: 90388f3296c1
Create Date: 2025-03-21 14:42:33.343817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04d79a4cf5e6'
down_revision: Union[str, None] = '90388f3296c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_foreign_key(
    "fk_users_posts",
    "posts",
    "users",
    ["owner_id"],
    ["id"],
    ondelete='CASCADE' ,
    onupdate='CASCADE')


def downgrade() -> None:
    op.drop_constraint("fk_users_posts", 'posts', type_='foreignkey')
