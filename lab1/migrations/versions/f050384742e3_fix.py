"""fix

Revision ID: f050384742e3
Revises: c0838ee54b7f
Create Date: 2025-04-13 00:16:53.438707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'f050384742e3'
down_revision: Union[str, None] = 'c0838ee54b7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('budget', 'category_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('budget', sa.Column('category_id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
