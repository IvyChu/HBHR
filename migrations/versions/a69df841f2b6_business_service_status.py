"""business service status

Revision ID: a69df841f2b6
Revises: a0ecd83b0d04
Create Date: 2023-04-05 21:29:36.260950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a69df841f2b6'
down_revision = 'a0ecd83b0d04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('business', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=True))

    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.drop_column('status')

    with op.batch_alter_table('business', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
