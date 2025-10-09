# migrations/env.py

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add project root to path so Alembic can find settings.py and models.py
# Assuming this script is in a 'migrations' subdirectory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root) 

# Import your project-specific modules
from settings import settings
from models import Base # Assuming you defined Base in models.py

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def get_url():
    """
    Returns the basic database URL stripped of all driver-specific details.
    This is primarily used for 'offline' mode and for setting config.set_main_option.
    """
    # Strips the driver and async marker (e.g., "postgresql+psycopg[async]")
    url_base = settings.DATABASE_URL.split("://", 1)[0].split("+", 1)[0]
    
    # Reconstruct the base URL to prevent stripping too much
    # Example: 'postgresql+psycopg[async]://user...' -> 'postgresql://user...'
    full_url = settings.DATABASE_URL
    if "://" in full_url:
        protocol_part = full_url.split("://", 1)[0].split("+", 1)[0]
        # Find the starting point of the credentials/host part
        host_part = full_url.split("://", 1)[1]
        return f"{protocol_part}://{host_part}"
    return full_url


# CRITICAL FIX 1: Set the database URL on the config object
# Note: get_url() provides the clean URL base.
config.set_main_option("sqlalchemy.url", get_url())


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url() 
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode with manual synchronous driver override."""
    
    # 1. Get the full URL from settings.py (e.g., postgresql+psycopg[async]://...)
    db_url_with_driver = settings.DATABASE_URL
    
    # 2. Define the configuration options
    alembic_config = config.get_section(config.config_ini_section, {})

    # 3. CRITICAL FIX 2: Manually override the URL to use the SYNCHRONOUS psycopg dialect.
    #    This is the simplest, most direct replacement to make the URL synchronous.
    sync_url = db_url_with_driver.replace("[async]", "")
    
    # Example: 'postgresql+psycopg[async]://...' becomes 'postgresql+psycopg://...'
    alembic_config['sqlalchemy.url'] = sync_url

    connectable = engine_from_config(
        alembic_config,
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