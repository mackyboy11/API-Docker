from sqlalchemy.orm import Session

from passlib.context import CryptContext
from database import DBUser, DBRole
from models import UserCreate
from typing import Optional, List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(db: Session, user_id: int) -> Optional[DBUser]:
	"""Get user by ID."""
	return db.query(DBUser).filter(DBUser.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[DBUser]:
	"""Get user by username."""
	return db.query(DBUser).filter(DBUser.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[DBUser]:
	"""Get user by email."""
	return db.query(DBUser).filter(DBUser.email == email).first()


def create_user(db: Session, user: UserCreate) -> DBUser:
	"""Create a new user."""
	hashed_password = pwd_context.hash(user.password)
	db_user = DBUser(
		username=user.username,
		email=user.email,
		full_name=user.full_name,
		hashed_password=hashed_password,
	)

	# Assign default user role if it exists
	user_role = db.query(DBRole).filter(DBRole.name == "user").first()
	if user_role:
		db_user.roles.append(user_role)

	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def authenticate_user(db: Session, username: str, password: str):
	"""Authenticate user with username and password.

	Returns the DBUser on success, or False on failure.
	"""
	user = get_user_by_username(db, username)
	if not user:
		return False
	if not pwd_context.verify(password, user.hashed_password):
		return False
	return user


def get_role_by_name(db: Session, name: str) -> Optional[DBRole]:
	"""Get role by name."""
	return db.query(DBRole).filter(DBRole.name == name).first()


def create_role(db: Session, name: str, description: str = "") -> DBRole:
	"""Create a new role."""
	db_role = DBRole(name=name, description=description)
	db.add(db_role)
	db.commit()
	db.refresh(db_role)
	return db_role


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[DBUser]:
	"""Get all users with pagination."""
	return db.query(DBUser).offset(skip).limit(limit).all()