"""adding values

Revision ID: ba9aa627328a
Revises: 436d449b2166
Create Date: 2024-11-07 14:12:52.859844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba9aa627328a'
down_revision = '436d449b2166'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consultas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('preco', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consultas', schema=None) as batch_op:
        batch_op.drop_column('preco')

    # ### end Alembic commands ###