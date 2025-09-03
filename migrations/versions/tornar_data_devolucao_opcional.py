"""Tornar data_devolucao opcional na tabela veiculos_evento

Revision ID: tornar_data_devolucao_opcional
Revises: adicionar_campos_hora_km_veiculo_evento
Create Date: 2025-01-16 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'tornar_data_devolucao_opcional'
down_revision = 'adicionar_campos_hora_km_veiculo_evento'
branch_labels = None
depends_on = None


def upgrade():
    # Alterar coluna data_devolucao para ser nullable
    op.alter_column('veiculos_evento', 'data_devolucao', nullable=True)


def downgrade():
    # Reverter coluna data_devolucao para ser not nullable
    op.alter_column('veiculos_evento', 'data_devolucao', nullable=False) 