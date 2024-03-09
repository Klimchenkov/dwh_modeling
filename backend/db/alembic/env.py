from logging.config import fileConfig

from sqlalchemy.orm import declarative_base
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import Column, Integer, String

from alembic import context

Base = declarative_base()

_type_lookup = {"integer": Integer, "string": String}

entries = [{
        "clsname": "MyClass",
        "tablename": "my_table",
        "columns": [
            {"name": "col1", "type": "integer", "is_pk": True},
            {"name": "col2", "type": "string"},
            {"name": "col3", "type": "integer"},
            {"name": "col4", "type": "integer"}
        ],
    },
           {
        "clsname": "MoreClass",
        "tablename": "more_table",
        "columns": [
            {"name": "col1", "type": "integer", "is_pk": True},
            {"name": "col2", "type": "string"},
            {"name": "col3", "type": "integer"},
            {"name": "col4", "type": "integer"}
        ],
    }]

def mapping_to_metadata(entry):

    clsdict = {"__tablename__": entry["tablename"]}

    clsdict.update(
        {
            rec["name"]: Column(
                _type_lookup[rec["type"]], primary_key=rec.get("is_pk", False)
            )
            for rec in entry["columns"]
        }
    )
    return type(entry["clsname"], (Base,), clsdict)

for entry in entries:
    mapping_to_metadata(entry)
    
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
