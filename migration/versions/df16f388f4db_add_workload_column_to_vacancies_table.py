"""add workload column to Vacancies table

Revision ID: df16f388f4db
Revises: 9aaeabadae08
Create Date: 2024-09-12 09:46:25.121722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df16f388f4db'
down_revision: Union[str, None] = '9aaeabadae08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Vacancies", sa.Column("workload", sa.String, nullable=True))


def downgrade() -> None:
    op.drop_column("Vacancies", "workload")