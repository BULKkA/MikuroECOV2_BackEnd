from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, PostStatus, ReactionType

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None

class User(UserBase):
    id: int
    role: UserRole
    email_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserRoleUpdate(BaseModel):
    role: UserRole

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Post schemas
class PostBase(BaseModel):
    title: str
    summary: Optional[str] = None
    body: str
    slug: str
    markdown: bool = False
    media: Optional[List[str]] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    body: Optional[str] = None
    slug: Optional[str] = None
    markdown: Optional[bool] = None
    media: Optional[List[str]] = None
    status: Optional[PostStatus] = None

class Post(PostBase):
    id: int
    author_id: int
    status: PostStatus
    created_at: datetime
    updated_at: Optional[datetime]
    author: User

    class Config:
        from_attributes = True

# Comment schemas
class CommentBase(BaseModel):
    body: str
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    body: Optional[str] = None

class Comment(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    author: User

    class Config:
        from_attributes = True

# Reaction schemas
class ReactionCreate(BaseModel):
    type: ReactionType

class Reaction(BaseModel):
    id: int
    post_id: int
    user_id: int
    type: ReactionType
    created_at: datetime
    user: User

    class Config:
        from_attributes = True

# Captcha schemas
class CaptchaVerify(BaseModel):
    token: str

class CaptchaResponse(BaseModel):
    verified: bool

# Media schemas
class MediaUpload(BaseModel):
    filename: str
    content_type: str
    size: int

class MediaResponse(BaseModel):
    id: str
    url: str