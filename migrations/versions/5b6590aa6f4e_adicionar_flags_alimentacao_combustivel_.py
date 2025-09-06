"""adicionar_flags_alimentacao_combustivel_apenas

Revision ID: 5b6590aa6f4e
Revises: 75998c3b99a8
Create Date: 2025-07-15 14:35:28.851345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b6590aa6f4e'
down_revision = '75998c3b99a8'
branch_labels = None
depends_on = None


def upgrade():
    # Adicionar colunas apenas se elas não existirem
    try:
        op.add_column('despesa', sa.Column('flag_alimentacao', sa.Boolean(), nullable=False, server_default='false'))
    except Exception:
        pass  # Coluna já existe
    
    try:
        op.add_column('despesa', sa.Column('flag_combustivel', sa.Boolean(), nullable=False, server_default='false'))
    except Exception:
        pass  # Coluna já existe


def downgrade():
    # Remover colunas se existirem
    try:
        op.drop_column('despesa', 'flag_combustivel')
    except Exception:
        pass
    
    try:
        op.drop_column('despesa', 'flag_alimentacao')
    except Exception:
        pass
