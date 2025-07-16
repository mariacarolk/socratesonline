"""Merge migrations

Revision ID: 8ecaefd91d66
Revises: 0ec0f4da905e, 1f6e28eee091, alterar_campo_data_para_vencimento_pagamento, b7314ea8fc32, d2352b3a6166
Create Date: 2025-07-14 17:14:55.669591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ecaefd91d66'
down_revision = ('0ec0f4da905e', '1f6e28eee091', 'alterar_campo_data_para_vencimento_pagamento', 'b7314ea8fc32', 'd2352b3a6166')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
