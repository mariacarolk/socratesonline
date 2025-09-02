"""adicionar telefone e email ao colaborador

Revision ID: 9b3f1b2a4d3a
Revises: d2352b3a6166_merge_heads
Create Date: 2025-08-14
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b3f1b2a4d3a'
down_revision = 'adicionar_campo_media_km_litro_veiculo'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('colaborador') as batch_op:
        batch_op.add_column(sa.Column('telefone', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table('colaborador') as batch_op:
        batch_op.drop_column('email')
        batch_op.drop_column('telefone')


