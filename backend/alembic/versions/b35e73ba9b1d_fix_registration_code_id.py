"""fix registration code id

Revision ID: b35e73ba9b1d
Revises: 0e827d703847
Create Date: 2026-11-06 15:29:08.967128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b35e73ba9b1d'
down_revision: Union[str, Sequence[str], None] = '0e827d703847'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass