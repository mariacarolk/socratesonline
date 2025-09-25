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
    """Adiciona campos valor_pago_socrates sem tentar remover índices inexistentes"""
    
    # Adicionar colunas nas tabelas de despesas
    with op.batch_alter_table('despesas_empresa', schema=None) as batch_op:
        batch_op.add_column(sa.Column('valor_pago_socrates', sa.Float(), nullable=True))

    with op.batch_alter_table('despesas_evento', schema=None) as batch_op:
        batch_op.add_column(sa.Column('valor_pago_socrates', sa.Float(), nullable=True))

    # Fazer email obrigatório no colaborador
    with op.batch_alter_table('colaborador', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # Corrigir foreign keys para veículos (sem dropar índices)
    with op.batch_alter_table('ipva_veiculo', schema=None) as batch_op:
        try:
            batch_op.drop_constraint('uk_ipva_veiculo_ano', type_='unique')
        except:
            pass
        try:
            batch_op.drop_constraint('ipva_veiculo_id_veiculo_fkey', type_='foreignkey')
        except:
            pass
        batch_op.create_foreign_key(None, 'veiculo', ['id_veiculo'], ['id_veiculo'])

    with op.batch_alter_table('licenciamento_veiculo', schema=None) as batch_op:
        try:
            batch_op.drop_constraint('uk_licenciamento_veiculo_ano', type_='unique')
        except:
            pass
        try:
            batch_op.drop_constraint('licenciamento_veiculo_id_veiculo_fkey', type_='foreignkey')
        except:
            pass
        batch_op.create_foreign_key(None, 'veiculo', ['id_veiculo'], ['id_veiculo'])

    with op.batch_alter_table('manutencao_veiculo', schema=None) as batch_op:
        try:
            batch_op.drop_constraint('manutencao_veiculo_id_veiculo_fkey', type_='foreignkey')
        except:
            pass
        batch_op.create_foreign_key(None, 'veiculo', ['id_veiculo'], ['id_veiculo'])

    with op.batch_alter_table('multa_veiculo', schema=None) as batch_op:
        try:
            batch_op.drop_constraint('multa_veiculo_id_veiculo_fkey', type_='foreignkey')
        except:
            pass
        batch_op.create_foreign_key(None, 'veiculo', ['id_veiculo'], ['id_veiculo'])


def downgrade():
    """Remove as colunas adicionadas"""
    
    with op.batch_alter_table('multa_veiculo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('multa_veiculo_id_veiculo_fkey', 'veiculo', ['id_veiculo'], ['id_veiculo'], ondelete='CASCADE')

    with op.batch_alter_table('manutencao_veiculo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('manutencao_veiculo_id_veiculo_fkey', 'veiculo', ['id_veiculo'], ['id_veiculo'], ondelete='CASCADE')

    with op.batch_alter_table('licenciamento_veiculo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('licenciamento_veiculo_id_veiculo_fkey', 'veiculo', ['id_veiculo'], ['id_veiculo'], ondelete='CASCADE')
        batch_op.create_unique_constraint('uk_licenciamento_veiculo_ano', ['id_veiculo', 'ano_exercicio'], postgresql_nulls_not_distinct=False)

    with op.batch_alter_table('ipva_veiculo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('ipva_veiculo_id_veiculo_fkey', 'veiculo', ['id_veiculo'], ['id_veiculo'], ondelete='CASCADE')
        batch_op.create_unique_constraint('uk_ipva_veiculo_ano', ['id_veiculo', 'ano_exercicio'], postgresql_nulls_not_distinct=False)

    with op.batch_alter_table('despesas_evento', schema=None) as batch_op:
        batch_op.drop_column('valor_pago_socrates')

    with op.batch_alter_table('despesas_empresa', schema=None) as batch_op:
        batch_op.drop_column('valor_pago_socrates')

    with op.batch_alter_table('colaborador', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=True)
