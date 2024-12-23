"""Add convenio column to pacientes

Revision ID: eb8462a755c4
Revises: de710944e7ad
Create Date: 2024-11-06 14:09:51.581533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb8462a755c4'
down_revision = 'de710944e7ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pacientes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('convenio', sa.String(length=64), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pacientes', schema=None) as batch_op:
        batch_op.drop_column('convenio')

    # ### end Alembic commands ###
