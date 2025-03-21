"""add owner_id to posts

Revision ID: 90388f3296c1
Revises: fbebdb4f3ae0
Create Date: 2025-03-21 14:32:32.096540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90388f3296c1'
down_revision: Union[str, None] = 'fbebdb4f3ae0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.add_column("posts", sa.Column("owner_id", sa.Integer , nullable=False))


def downgrade() -> None:
   op.drop_column("posts", "owner_id")
