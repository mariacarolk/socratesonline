"""Adicionar tabelas equipe_evento, elenco_evento, fornecedor_evento e campo id_fornecedor

Revision ID: f77b76e795bd
Revises: fix_relationships_logic
Create Date: 2025-06-11 15:52:07.990482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f77b76e795bd'
down_revision = 'fix_relationships_logic'
branch_labels = None
depends_on = None


def upgrade():
    # Criar tabela equipe_evento
    op.create_table('equipe_evento',
        sa.Column('id_equipe_evento', sa.Integer(), nullable=False),
        sa.Column('id_evento', sa.Integer(), nullable=False),
        sa.Column('id_colaborador', sa.Integer(), nullable=False),
        sa.Column('funcao', sa.String(), nullable=True),
        sa.Column('observacoes', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['id_colaborador'], ['colaborador.id_colaborador'], ),
        sa.ForeignKeyConstraint(['id_evento'], ['evento.id_evento'], ),
        sa.PrimaryKeyConstraint('id_equipe_evento')
    )
    
    # Criar tabela elenco_evento
    op.create_table('elenco_evento',
        sa.Column('id_elenco_evento', sa.Integer(), nullable=False),
        sa.Column('id_evento', sa.Integer(), nullable=False),
        sa.Column('id_elenco', sa.Integer(), nullable=False),
        sa.Column('observacoes', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['id_elenco'], ['elenco.id_elenco'], ),
        sa.ForeignKeyConstraint(['id_evento'], ['evento.id_evento'], ),
        sa.PrimaryKeyConstraint('id_elenco_evento')
    )
    
    # Criar tabela fornecedor_evento
    op.create_table('fornecedor_evento',
        sa.Column('id_fornecedor_evento', sa.Integer(), nullable=False),
        sa.Column('id_evento', sa.Integer(), nullable=False),
        sa.Column('id_fornecedor', sa.Integer(), nullable=False),
        sa.Column('observacoes', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['id_evento'], ['evento.id_evento'], ),
        sa.ForeignKeyConstraint(['id_fornecedor'], ['fornecedor.id_fornecedor'], ),
        sa.PrimaryKeyConstraint('id_fornecedor_evento')
    )
    
    # Adicionar campo id_fornecedor na tabela despesa_evento
    op.add_column('despesa_evento', sa.Column('id_fornecedor', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'despesa_evento', 'fornecedor', ['id_fornecedor'], ['id_fornecedor'])


def downgrade():
    # Remover campo id_fornecedor da tabela despesa_evento
    op.drop_constraint(None, 'despesa_evento', type_='foreignkey')
    op.drop_column('despesa_evento', 'id_fornecedor')
    
    # Remover tabelas criadas
    op.drop_table('fornecedor_evento')
    op.drop_table('elenco_evento') 
    op.drop_table('equipe_evento')
