"""first version of alembic revision

Revision ID: 717f41821c03
Revises: 
Create Date: 2024-09-04 21:34:59.237602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '717f41821c03'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("test", sa.Column("test", sa.String))
    pass


def downgrade() -> None:
    op.drop_table("test")
    pass
