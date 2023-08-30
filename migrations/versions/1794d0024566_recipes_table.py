"""recipes table

Revision ID: 1794d0024566
Revises: 4461b70bf17d
Create Date: 2023-08-28 23:21:23.236186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1794d0024566'
down_revision = '4461b70bf17d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('category', sa.String(length=140), nullable=True),
    sa.Column('ingredients', sa.String(length=140), nullable=True),
    sa.Column('steps', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('picture', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_recipe_category'), ['category'], unique=False)
        batch_op.create_index(batch_op.f('ix_recipe_ingredients'), ['ingredients'], unique=False)
        batch_op.create_index(batch_op.f('ix_recipe_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_recipe_timestamp'))
        batch_op.drop_index(batch_op.f('ix_recipe_ingredients'))
        batch_op.drop_index(batch_op.f('ix_recipe_category'))

    op.drop_table('recipe')
    # ### end Alembic commands ###