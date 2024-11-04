"""first migration

Revision ID: 0389801dfdef
Revises: 
Create Date: 2024-11-01 21:35:08.865839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0389801dfdef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pacientes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=True),
    sa.Column('idade', sa.Integer(), nullable=True),
    sa.Column('cpf', sa.String(length=11), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('pagamento', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('pacientes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_pacientes_cpf'), ['cpf'], unique=True)
        batch_op.create_index(batch_op.f('ix_pacientes_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_pacientes_nome'), ['nome'], unique=False)

    op.create_table('medicos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=False),
    sa.Column('especialidade', sa.String(length=64), nullable=True),
    sa.Column('horarios', sa.String(length=128), nullable=True),
    sa.Column('paciente_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['paciente_id'], ['pacientes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('paciente_id')
    )
    op.create_table('consultas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('paciente_id', sa.Integer(), nullable=True),
    sa.Column('medico_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['medico_id'], ['medicos.id'], ),
    sa.ForeignKeyConstraint(['paciente_id'], ['pacientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('consultas')
    op.drop_table('medicos')
    with op.batch_alter_table('pacientes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_pacientes_nome'))
        batch_op.drop_index(batch_op.f('ix_pacientes_email'))
        batch_op.drop_index(batch_op.f('ix_pacientes_cpf'))

    op.drop_table('pacientes')
    # ### end Alembic commands ###