"""Fix missing indexes for Railway deployment

Revision ID: fix_missing_indexes_railway  
Revises: initial
Create Date: 2025-01-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fix_missing_indexes_railway'
down_revision = 'initial'
branch_labels = None
depends_on = None


def upgrade():
    """Adiciona apenas os campos valor_pago_socrates necessários"""
    
    # Verificar se as tabelas existem antes de tentar alterá-las
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    # Adicionar colunas nas tabelas de despesas se existirem
    if 'despesas_empresa' in tables:
        with op.batch_alter_table('despesas_empresa', schema=None) as batch_op:
            batch_op.add_column(sa.Column('valor_pago_socrates', sa.Float(), nullable=True))

    if 'despesas_evento' in tables:
        with op.batch_alter_table('despesas_evento', schema=None) as batch_op:
            batch_op.add_column(sa.Column('valor_pago_socrates', sa.Float(), nullable=True))

    # Fazer email obrigatório no colaborador se a tabela existir
    if 'colaborador' in tables:
        with op.batch_alter_table('colaborador', schema=None) as batch_op:
            batch_op.alter_column('email',
                   existing_type=sa.VARCHAR(),
                   nullable=False)


def downgrade():
    """Remove as colunas adicionadas se as tabelas existirem"""
    
    # Verificar se as tabelas existem antes de tentar alterá-las
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    tables = inspector.get_table_names()
    
    if 'despesas_evento' in tables:
        with op.batch_alter_table('despesas_evento', schema=None) as batch_op:
            batch_op.drop_column('valor_pago_socrates')

    if 'despesas_empresa' in tables:
        with op.batch_alter_table('despesas_empresa', schema=None) as batch_op:
            batch_op.drop_column('valor_pago_socrates')

    if 'colaborador' in tables:
        with op.batch_alter_table('colaborador', schema=None) as batch_op:
            batch_op.alter_column('email',
                   existing_type=sa.VARCHAR(),
                   nullable=True)
