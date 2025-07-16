"""Criar tabela veiculos_evento

Revision ID: criar_tabela_veiculos_evento
Revises: f77b76e795bd
Create Date: 2024-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'criar_tabela_veiculos_evento'
down_revision = 'f77b76e795bd'
branch_labels = None
depends_on = None


def upgrade():
    # Criar tabela veiculos_evento
    op.create_table('veiculos_evento',
        sa.Column('id_veiculo_evento', sa.Integer(), nullable=False),
        sa.Column('id_evento', sa.Integer(), nullable=False),
        sa.Column('id_veiculo', sa.Integer(), nullable=False),
        sa.Column('id_motorista', sa.Integer(), nullable=False),
        sa.Column('data_inicio', sa.Date(), nullable=False),
        sa.Column('data_devolucao', sa.Date(), nullable=False),
        sa.Column('observacoes', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['id_evento'], ['evento.id_evento']),
        sa.ForeignKeyConstraint(['id_veiculo'], ['veiculo.id_veiculo']),
        sa.ForeignKeyConstraint(['id_motorista'], ['colaborador.id_colaborador']),
        sa.PrimaryKeyConstraint('id_veiculo_evento')
    )


def downgrade():
    # Remover tabela veiculos_evento
    op.drop_table('veiculos_evento') 