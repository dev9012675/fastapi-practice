"""create posts table

Revision ID: 3c49788f6acb
Revises: 
Create Date: 2025-03-21 12:11:01.919771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c49788f6acb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True , nullable=False),
        sa.Column('title', sa.String(30), nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published' , sa.Boolean , server_default= 'TRUE' , nullable=False) ,
        sa.Column('created_at',sa.sql.sqltypes.TIMESTAMP(timezone=True) , nullable=False , server_default=sa.sql.expression.text('now()'))
    )
 

def downgrade() -> None:
    op.drop_table('posts')

