from alembic.config import Config
from alembic import command
import pytest
from sqlalchemy import create_engine, text

# These test are to guarantee that this project is able to migrate to another DB

def available_dbs() -> list[str]:
    return [
    "sqlite", 
    "postgres", 
]

@pytest.fixture
def alembic_runner(db_url):
    def upgrade(revision="head"):
        cfg = Config("alembic.ini")
        cfg.set_main_option("sqlalchemy.url", db_url)
        command.upgrade(cfg, revision)

    def downgrade(revision="base"):
        cfg = Config("alembic.ini")
        cfg.set_main_option("sqlalchemy.url", db_url)
        command.downgrade(cfg, revision)

    return {
        "upgrade": upgrade,
        "downgrade": downgrade,
    }

@pytest.mark.migration
@pytest.mark.parametrize("db_url", available_dbs(), indirect=True)
def test_upgrade_head(db_url, alembic_runner):
    alembic_runner["upgrade"]("head")

@pytest.mark.migration
@pytest.mark.parametrize("db_url", available_dbs(), indirect=True)
def test_upgrade_downgrade_cycle(db_url, alembic_runner):
    alembic_runner["upgrade"]("head")
    alembic_runner["downgrade"]("base")

@pytest.mark.migration
@pytest.mark.parametrize("table", [
    "wallets", 
    "transactions"
])
@pytest.mark.parametrize("db_url", available_dbs(), indirect=True)
def test_table_created(db_url, table, alembic_runner):
    alembic_runner["upgrade"]("head")

    engine = create_engine(db_url)

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT 1 FROM {table} LIMIT 1"))
        assert result is not None
