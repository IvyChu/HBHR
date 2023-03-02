"""service table

Revision ID: 72d92fbb4c4f
Revises: 71724fb47365
Create Date: 2023-03-01 21:55:59.776828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72d92fbb4c4f'
down_revision = '71724fb47365'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_service'))
    )
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_service_name'), ['name'], unique=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_users_email', type_='unique')
        batch_op.drop_constraint('uq_users_fs_uniquifier', type_='unique')
        batch_op.drop_constraint('uq_users_username', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_user_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_user_fs_uniquifier'), ['fs_uniquifier'])
        batch_op.create_unique_constraint(batch_op.f('uq_user_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_username'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_user_fs_uniquifier'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_user_email'), type_='unique')
        batch_op.create_unique_constraint('uq_users_username', ['username'])
        batch_op.create_unique_constraint('uq_users_fs_uniquifier', ['fs_uniquifier'])
        batch_op.create_unique_constraint('uq_users_email', ['email'])

    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_service_name'))

    op.drop_table('service')
    # ### end Alembic commands ###