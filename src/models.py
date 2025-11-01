from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum

db = SQLAlchemy()

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"

class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    profile_picture: Mapped[str] = mapped_column(String(255), nullable=True)
    is_private: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    posts: Mapped[list['Post']] = relationship('Post', back_populates='user')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user')
    likes: Mapped[list['Like']] = relationship('Like', back_populates='user')
    followers: Mapped[list['Follower']] = relationship('Follower', foreign_keys='Follower.following_id', back_populates='following')
    following: Mapped[list['Follower']] = relationship('Follower', foreign_keys='Follower.follower_id', back_populates='follower')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "bio": self.bio,
            "profile_picture": self.profile_picture,
            "is_private": self.is_private,
            "created_at": self.created_at.isoformat()
        }

class Post(db.Model):
    __tablename__ = 'post'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped['User'] = relationship('User', back_populates='posts')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='post')
    likes: Mapped[list['Like']] = relationship('Like', back_populates='post')
    media: Mapped[list['Media']] = relationship('Media', back_populates='post')

    def serialize(self):
        return {
            "id": self.id,
            "caption": self.caption,
            "location": self.location,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "user": self.user.serialize() if self.user else None,
            "media": [media.serialize() for media in self.media] if self.media else []
        }

class Media(db.Model):
    __tablename__ = 'media'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post: Mapped['Post'] = relationship('Post', back_populates='media')

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "url": self.url,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat()
        }

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped['User'] = relationship('User', back_populates='comments')
    post: Mapped['Post'] = relationship('Post', back_populates='comments')

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat(),
            "user": self.user.serialize() if self.user else None
        }

class Like(db.Model):
    __tablename__ = 'like'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped['User'] = relationship('User', back_populates='likes')
    post: Mapped['Post'] = relationship('Post', back_populates='likes')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat()
        }

class Follower(db.Model):
    __tablename__ = 'follower'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    follower_user: Mapped['User'] = relationship('User', foreign_keys=[user_from_id], backref='following_relationships')
    following_user: Mapped['User'] = relationship('User', foreign_keys=[user_to_id], backref='follower_relationships')

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
            "created_at": self.created_at.isoformat()
        }