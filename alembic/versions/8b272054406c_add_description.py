"""add description

Revision ID: 8b272054406c
Revises: a743f2b65419
Create Date: 2025-03-15 20:03:30.106140

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b272054406c'
down_revision: Union[str, None] = 'a743f2b65419'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('description', sa.String(), nullable=True, default=''))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'description')
    # ### end Alembic commands ###
