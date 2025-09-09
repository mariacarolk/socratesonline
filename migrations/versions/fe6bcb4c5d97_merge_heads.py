"""merge heads

Revision ID: fe6bcb4c5d97
Revises: 
Create Date: 2025-09-08 18:38:28.014836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe6bcb4c5d97'
down_revision = ('marketing_completo', 'tornar_data_devolucao_opcional')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
