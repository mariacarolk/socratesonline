"""Adicionar campos qtd_dias e qtd_pessoas nas tabelas de despesas

Revision ID: adicionar_qtd_dias_pessoas_despesas
Revises: [ID_ANTERIOR]
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adicionar_qtd_dias_pessoas_despesas'
down_revision = '9b3f1b2a4d3a'
branch_labels = None
depends_on = None


def upgrade():
    # Adicionar campos qtd_dias e qtd_pessoas na tabela despesas_evento
    op.add_column('despesas_evento', sa.Column('qtd_dias', sa.Integer(), nullable=True))
    op.add_column('despesas_evento', sa.Column('qtd_pessoas', sa.Integer(), nullable=True))
    
    # Adicionar campos qtd_dias e qtd_pessoas na tabela despesas_empresa
    op.add_column('despesas_empresa', sa.Column('qtd_dias', sa.Integer(), nullable=True))
    op.add_column('despesas_empresa', sa.Column('qtd_pessoas', sa.Integer(), nullable=True))


def downgrade():
    # Remover campos qtd_dias e qtd_pessoas da tabela despesas_empresa
    op.drop_column('despesas_empresa', 'qtd_pessoas')
    op.drop_column('despesas_empresa', 'qtd_dias')
    
    # Remover campos qtd_dias e qtd_pessoas da tabela despesas_evento
    op.drop_column('despesas_evento', 'qtd_pessoas')
    op.drop_column('despesas_evento', 'qtd_dias') 