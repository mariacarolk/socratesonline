"""Fix cascade delete relationships for SQLite

Revision ID: cascade_delete_fix
Revises: add_tipo_despesa_manual
Create Date: 2025-06-08 12:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cascade_delete_fix'
down_revision = 'add_tipo_despesa_manual'
branch_labels = None
depends_on = None

def upgrade():
    # Para SQLite, vamos apenas garantir que os relacionamentos estão corretos
    # O CASCADE DELETE será tratado pelo SQLAlchemy ORM através dos relacionamentos
    pass

def downgrade():
    # Não há necessidade de downgrade para esta migração
    pass 