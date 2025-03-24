from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable or use SQLite as default
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ai_use_cases.db')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AIUseCaseDB(Base):
    __tablename__ = "ai_use_cases"

    id = Column(String, primary_key=True)
    industry = Column(String, nullable=False)
    business_function = Column(String, nullable=False)
    origine_de_la_source = Column(String, nullable=False)
    lien = Column(String, nullable=False)
    usage_ia = Column(String, nullable=False)
    derniere_mise_a_jour = Column(DateTime, default=datetime.utcnow)
    processus_impacte = Column(String)  # Stored as JSON string
    gains_attendus_realises = Column(String)  # Stored as JSON string
    technologies_ia_utilisees = Column(String)  # Stored as JSON string
    partenaires_impliques = Column(String)  # Stored as JSON string

    def to_dict(self):
        """Convert the database entry to a dictionary."""
        return {
            'id': self.id,
            'industry': self.industry,
            'business_function': self.business_function,
            'origine_de_la_source': self.origine_de_la_source,
            'lien': self.lien,
            'usage_ia': self.usage_ia,
            'derniere_mise_a_jour': self.derniere_mise_a_jour.isoformat(),
            'processus_impacte': json.loads(self.processus_impacte) if self.processus_impacte else [],
            'gains_attendus_realises': json.loads(self.gains_attendus_realises) if self.gains_attendus_realises else [],
            'technologies_ia_utilisees': json.loads(self.technologies_ia_utilisees) if self.technologies_ia_utilisees else [],
            'partenaires_impliques': json.loads(self.partenaires_impliques) if self.partenaires_impliques else []
        }

class DatabaseManager:
    def __init__(self):
        """Initialize the database connection and create tables."""
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

    def save_use_case(self, use_case):
        """Save a single AI use case to the database."""
        try:
            # Convert lists to JSON strings
            db_use_case = AIUseCaseDB(
                id=use_case['id'],
                industry=use_case['industry'],
                business_function=use_case['business_function'],
                origine_de_la_source=use_case['origine_de_la_source'],
                lien=use_case['lien'],
                usage_ia=use_case['usage_ia'],
                processus_impacte=json.dumps(use_case.get('processus_impacte', [])),
                gains_attendus_realises=json.dumps(use_case.get('gains_attendus_realises', [])),
                technologies_ia_utilisees=json.dumps(use_case.get('technologies_ia_utilisees', [])),
                partenaires_impliques=json.dumps(use_case.get('partenaires_impliques', []))
            )
            self.db.add(db_use_case)
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error saving use case: {e}")
            self.db.rollback()
            return False

    def save_use_cases(self, use_cases):
        """Save multiple AI use cases to the database."""
        success_count = 0
        for use_case in use_cases:
            if self.save_use_case(use_case):
                success_count += 1
        return success_count

    def get_use_cases_by_industry(self, industry):
        """Get all AI use cases for a specific industry."""
        use_cases = self.db.query(AIUseCaseDB).filter(AIUseCaseDB.industry == industry).all()
        return [use_case.to_dict() for use_case in use_cases]

    def get_all_industries(self):
        """Get all unique industries from the database."""
        industries = self.db.query(AIUseCaseDB.industry).distinct().all()
        return [industry[0] for industry in industries]

    def __del__(self):
        """Close the database connection when the manager is destroyed."""
        self.db.close() 