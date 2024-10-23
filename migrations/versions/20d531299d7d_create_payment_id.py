"""create payment ID

Revision ID: 20d531299d7d
Revises: b5a0ab3c0e6e
Create Date: 2024-10-23 21:27:28.398208

"""

from typing import Sequence, Union
from alembic import op
from sqlalchemy import Column, Integer
from src.models import Users

revision: str = "20d531299d7d"
down_revision: Union[str, None] = "b5a0ab3c0e6e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("payments") as batch_op:
        batch_op.add_column(Column("ID", Integer, unique=True))


def downgrade():
    with op.batch_alter_table("payments") as batch_op:
        batch_op.drop_column("ID")
