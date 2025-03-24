"""add file path to posts

Revision ID: 84bd1ba2934b
Revises: 04d79a4cf5e6
Create Date: 2025-03-22 16:20:38.069977

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84bd1ba2934b'
down_revision: Union[str, None] = '04d79a4cf5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("files", sa.String , nullable=True))


def downgrade() -> None:
    op.drop_column("posts", "files")