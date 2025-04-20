from app.db.session import Base
from app.models.task import Task

# Import all models here so they are registered with SQLAlchemy
__all__ = ["Base", "Task"] 