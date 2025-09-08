"""marketing completo - tabela escola e categoria promotor

Revision ID: marketing_completo
Revises: criar_tabela_parametros
Create Date: 2024-12-19 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'marketing_completo'
down_revision = 'criar_tabela_parametros'
branch_labels = None
depends_on = None


def upgrade():
    # ### Criar tabela escola ###
    op.create_table('escola',
        sa.Column('id_escola', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=200), nullable=False),
        sa.Column('endereco', sa.String(length=300), nullable=False),
        sa.Column('cidade', sa.String(length=100), nullable=False),
        sa.Column('estado', sa.String(length=2), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('whatsapp', sa.String(length=20), nullable=True),
        sa.Column('nome_contato', sa.String(length=100), nullable=False),
        sa.Column('cargo_contato', sa.String(length=100), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('data_visita', sa.DateTime(), nullable=False),
        sa.Column('id_promotor', sa.Integer(), nullable=False),
        sa.Column('email_enviado', sa.Boolean(), nullable=False, default=False),
        sa.Column('whatsapp_enviado', sa.Boolean(), nullable=False, default=False),
        sa.Column('data_email_enviado', sa.DateTime(), nullable=True),
        sa.Column('data_whatsapp_enviado', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['id_promotor'], ['colaborador.id_colaborador'], ),
        sa.PrimaryKeyConstraint('id_escola')
    )
    
    # ### Adicionar categoria Promotor de vendas ###
    connection = op.get_bind()
    
    # Verificar se a categoria já existe
    result = connection.execute(
        sa.text("SELECT COUNT(*) FROM categoria_colaborador WHERE nome = 'Promotor de vendas'")
    )
    count = result.scalar()
    
    if count == 0:
        # Inserir a nova categoria
        connection.execute(
            sa.text("INSERT INTO categoria_colaborador (nome) VALUES ('Promotor de vendas')")
        )


def downgrade():
    # ### Remover categoria Promotor de vendas ###
    connection = op.get_bind()
    connection.execute(
        sa.text("DELETE FROM categoria_colaborador WHERE nome = 'Promotor de vendas'")
    )
    
    # ### Remover tabela escola ###
    op.drop_table('escola')
