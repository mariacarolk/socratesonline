"""Adicionar tabela tipo_despesa e campos na despesa - manual

Revision ID: add_tipo_despesa_manual
Revises: 846c2ce7fe86
Create Date: 2025-06-01 16:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_tipo_despesa_manual'
down_revision = '846c2ce7fe86'
branch_labels = None
depends_on = None


def upgrade():
    # Criar tabela tipo_despesa
    op.create_table('tipo_despesa',
        sa.Column('id_tipo_despesa', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id_tipo_despesa')
    )
    
    # Adicionar colunas na tabela despesa
    with op.batch_alter_table('despesa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_tipo_despesa', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('valor_medio_despesa', sa.Numeric(precision=10, scale=2), nullable=True))
        batch_op.create_foreign_key('fk_despesa_tipo_despesa', 'tipo_despesa', ['id_tipo_despesa'], ['id_tipo_despesa'])


def downgrade():
    # Remover colunas da tabela despesa
    with op.batch_alter_table('despesa', schema=None) as batch_op:
        batch_op.drop_constraint('fk_despesa_tipo_despesa', type_='foreignkey')
        batch_op.drop_column('valor_medio_despesa')
        batch_op.drop_column('id_tipo_despesa')
    
    # Remover tabela tipo_despesa
    op.drop_table('tipo_despesa') 