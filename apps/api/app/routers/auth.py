# OpenSchoolOS API — Auth routes (Sprint 005).
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import create_token, get_current_user, hash_password, verify_password
from app.db import get_session
from app.models import UserModel
from app.schemas import TokenOut, UserLogin, UserOut, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, session: Session = Depends(get_session)):
    existing = session.scalar(select(UserModel).where(UserModel.email == payload.email))
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered.")
    user = UserModel(
        id=str(uuid.uuid4()), email=payload.email, full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    token = create_token(user.id)
    return TokenOut(
        access_token=token,
        user=UserOut(id=user.id, email=user.email, full_name=user.full_name),
    )


@router.post("/login", response_model=TokenOut)
def login(payload: UserLogin, session: Session = Depends(get_session)):
    user = session.scalar(select(UserModel).where(UserModel.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    if not user.is_active or user.deleted_at is not None:
        raise HTTPException(status_code=403, detail="Account deactivated.")
    token = create_token(user.id)
    return TokenOut(
        access_token=token,
        user=UserOut(id=user.id, email=user.email, full_name=user.full_name),
    )


@router.get("/me", response_model=UserOut)
def me(user: UserModel = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated.")
    return UserOut(id=user.id, email=user.email, full_name=user.full_name)
