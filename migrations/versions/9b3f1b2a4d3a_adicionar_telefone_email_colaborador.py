"""adicionar telefone e email ao colaborador

Revision ID: 9b3f1b2a4d3a
Revises: d2352b3a6166_merge_heads
Create Date: 2025-08-14
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b3f1b2a4d3a'
down_revision = '5b6590aa6f4e'
branch_labels = None
depends_on = None


def upgrade():
    # PostgreSQL pode fazer ALTER TABLE diretamente
    op.add_column('colaborador', sa.Column('telefone', sa.String(), nullable=True))
    op.add_column('colaborador', sa.Column('email', sa.String(), nullable=True))


def downgrade():
    # PostgreSQL pode fazer DROP COLUMN diretamente
    op.drop_column('colaborador', 'email')
    op.drop_column('colaborador', 'telefone')


