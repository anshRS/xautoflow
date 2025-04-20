import os
import sys
from pathlib import Path

def setup_project():
    # Create necessary directories
    directories = [
        '.cache',
        'local_kb',
        'app/db/migrations/versions',
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env.template', 'r') as template:
            with open('.env', 'w') as env:
                env.write(template.read())
        print("Created .env file from template")
    
    # Initialize alembic
    os.system('alembic init -t async app/db/migrations')
    print("Initialized Alembic migrations")
    
    # Create initial migration
    os.system('alembic revision --autogenerate -m "Initial migration"')
    print("Created initial migration")
    
    # Apply migrations
    os.system('alembic upgrade head')
    print("Applied migrations")

if __name__ == "__main__":
    setup_project()