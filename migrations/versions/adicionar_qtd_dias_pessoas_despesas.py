"""Adicionar campos qtd_dias e qtd_pessoas nas tabelas de despesas

Revision ID: adicionar_qtd_dias_pessoas_despesas
Revises: [ID_ANTERIOR]
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adicionar_qtd_dias_pessoas_despesas'
down_revision = '5b6590aa6f4e'
branch_labels = None
depends_on = None


def upgrade():
    # Adicionar campos qtd_dias e qtd_pessoas na tabela despesas_evento
    with op.batch_alter_table('despesas_evento', schema=None) as batch_op:
        batch_op.add_column(sa.Column('qtd_dias', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('qtd_pessoas', sa.Integer(), nullable=True))
    
    # Adicionar campos qtd_dias e qtd_pessoas na tabela despesas_empresa
    with op.batch_alter_table('despesas_empresa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('qtd_dias', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('qtd_pessoas', sa.Integer(), nullable=True))


def downgrade():
    # Remover campos qtd_dias e qtd_pessoas da tabela despesas_empresa
    with op.batch_alter_table('despesas_empresa', schema=None) as batch_op:
        batch_op.drop_column('qtd_pessoas')
        batch_op.drop_column('qtd_dias')
    
    # Remover campos qtd_dias e qtd_pessoas da tabela despesas_evento
    with op.batch_alter_table('despesas_evento', schema=None) as batch_op:
        batch_op.drop_column('qtd_pessoas')
        batch_op.drop_column('qtd_dias') 