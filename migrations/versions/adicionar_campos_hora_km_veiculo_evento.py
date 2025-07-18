"""Adicionar campos hora_inicio, hora_fim, km_inicio e km_fim na tabela veiculos_evento

Revision ID: adicionar_campos_hora_km_veiculo_evento
Revises: criar_tabela_veiculos_evento
Create Date: 2025-01-16 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adicionar_campos_hora_km_veiculo_evento'
down_revision = 'adicionar_qtd_dias_pessoas_despesas'
branch_labels = None
depends_on = None


def upgrade():
    # Adicionar novos campos na tabela veiculos_evento
    op.add_column('veiculos_evento', sa.Column('hora_inicio', sa.Time(), nullable=True))
    op.add_column('veiculos_evento', sa.Column('hora_fim', sa.Time(), nullable=True))
    op.add_column('veiculos_evento', sa.Column('km_inicio', sa.Integer(), nullable=True))
    op.add_column('veiculos_evento', sa.Column('km_fim', sa.Integer(), nullable=True))


def downgrade():
    # Remover campos adicionados
    op.drop_column('veiculos_evento', 'km_fim')
    op.drop_column('veiculos_evento', 'km_inicio')
    op.drop_column('veiculos_evento', 'hora_fim')
    op.drop_column('veiculos_evento', 'hora_inicio') 