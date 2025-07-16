"""merge heads

Revision ID: b7314ea8fc32
Revises: adicionar_comprovante, f77b76e795bd
Create Date: 2025-07-09 12:35:58.024937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7314ea8fc32'
down_revision = ('adicionar_comprovante', 'f77b76e795bd')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
