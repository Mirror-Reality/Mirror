from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Mirror(Base):
    __tablename__ = "mirrors"

    id = Column(Integer, primary_key=True, index=True)
    ipfs_hash = Column(String, nullable=False)
    owner_address = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)

class MirrorActivity(Base):
    __tablename__ = "mirror_activities"

    id = Column(Integer, primary_key=True, index=True)
    mirror_id = Column(Integer, nullable=False)
    activity_type = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PersonalityTrait(Base):
    __tablename__ = "personality_traits"

    id = Column(Integer, primary_key=True, index=True)
    mirror_id = Column(Integer, nullable=False)
    trait_name = Column(String, nullable=False)
    trait_value = Column(String, nullable=False)
    confidence = Column(String, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TrainingData(Base):
    __tablename__ = "training_data"

    id = Column(Integer, primary_key=True, index=True)
    mirror_id = Column(Integer, nullable=False)
    data_type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_processed = Column(Boolean, default=False) 