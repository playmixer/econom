"""empty message

Revision ID: 0b57cab0f84c
Revises: 7856469df42a
Create Date: 2021-05-04 12:56:36.614536

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0b57cab0f84c'
down_revision = '7856469df42a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('wallet', 'balance', existing_type=sa.Numeric(10, 2), nullable=False)
    op.alter_column('income', 'money', existing_type=sa.Numeric(10, 2), nullable=False)
    op.alter_column('expense', 'money', existing_type=sa.Numeric(10, 2), nullable=False)


def downgrade():
    op.alter_column('wallet', 'balance', existing_type=sa.Float, nullable=True)
    op.alter_column('income', 'money', existing_type=sa.Float, nullable=False)
    op.alter_column('expense', 'money', existing_type=sa.Float, nullable=False)
