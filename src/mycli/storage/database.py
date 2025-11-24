"""Database operations for mycli."""

from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as DBSession

from mycli.config import get_config
from mycli.storage.models import Base
from mycli.utils.logger import get_logger

logger = get_logger(__name__)


class Database:
    """Database manager."""
    
    def __init__(self, db_path: Optional[Path] = None) -> None:
        """Initialize database.
        
        Args:
            db_path: Database file path. If None, use default location.
        """
        if db_path is None:
            config = get_config()
            data_dir = config.get_data_dir()
            db_path = data_dir / "mycli.db"
        
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create engine
        db_url = f"sqlite:///{db_path}"
        self.engine = create_engine(db_url, echo=False)
        
        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
        
        # Create tables
        self.create_tables()
        
        logger.info(f"Database initialized at {db_path}")
    
    def create_tables(self) -> None:
        """Create all tables."""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self) -> None:
        """Drop all tables."""
        Base.metadata.drop_all(bind=self.engine)
    
    def get_session(self) -> DBSession:
        """Get database session.
        
        Returns:
            Database session.
        """
        return self.SessionLocal()
    
    def close(self) -> None:
        """Close database connection."""
        self.engine.dispose()


# Global database instance
_db: Optional[Database] = None


def get_database(db_path: Optional[Path] = None) -> Database:
    """Get global database instance.
    
    Args:
        db_path: Optional database file path.
    
    Returns:
        Database instance.
    """
    global _db
    if _db is None:
        _db = Database(db_path)
    return _db
