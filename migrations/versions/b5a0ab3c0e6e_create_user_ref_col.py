"""create user ref col

Revision ID: b5a0ab3c0e6e
Revises:
Create Date: 2024-10-23 17:39:45.742754

"""

from typing import Sequence, Union
from alembic import op
from sqlalchemy import Column, String
from src.models import Users

revision: str = "b5a0ab3c0e6e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(Column("ref_string", String(20), unique=True))


def downgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("ref_string")
