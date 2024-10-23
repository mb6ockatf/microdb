"""create convert payments.user_id datatype

Revision ID: aecb4fa89650
Revises: 20d531299d7d
Create Date: 2024-10-23 21:51:19.899282

"""
from typing import Sequence, Union
from alembic import op
from sqlalchemy import Column, Integer

revision: str = 'aecb4fa89650'
down_revision: Union[str, None] = '20d531299d7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    with op.batch_alter_table("payments") as batch_op:
        batch_op.drop_column("user_id")
        batch_op.add_column(Column("user_id", Integer))

def downgrade():
    pass

