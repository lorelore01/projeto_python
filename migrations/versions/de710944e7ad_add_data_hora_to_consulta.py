"""Add data_hora to Consulta

Revision ID: de710944e7ad
Revises: 1f66164747ca
Create Date: 2024-11-03 13:13:33.316592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de710944e7ad'
down_revision = '1f66164747ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consultas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_hora', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consultas', schema=None) as batch_op:
        batch_op.drop_column('data_hora')

    # ### end Alembic commands ###