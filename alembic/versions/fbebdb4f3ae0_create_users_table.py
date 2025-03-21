"""create users table

Revision ID: fbebdb4f3ae0
Revises: 3c49788f6acb
Create Date: 2025-03-21 12:32:40.618148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbebdb4f3ae0'
down_revision: Union[str, None] = '3c49788f6acb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True , nullable=False),
        sa.Column('email', sa.String, unique=True , nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at',sa.sql.sqltypes.TIMESTAMP(timezone=True) , nullable=False , server_default=sa.sql.expression.text('now()'))
    )


def downgrade() -> None:
    op.drop_table('users')
