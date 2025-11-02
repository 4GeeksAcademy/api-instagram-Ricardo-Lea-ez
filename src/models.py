from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    profile_picture: Mapped[str] = mapped_column(String(255), nullable=True)
    website: Mapped[str] = mapped_column(String(255), nullable=True)
    is_private: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    posts: Mapped[list['Post']] = relationship('Post', back_populates='user')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user')
    likes: Mapped[list['Like']] = relationship('Like', back_populates='user')
    stories: Mapped[list['Story']] = relationship('Story', back_populates='user')
    
    # Follow relationships
    followers: Mapped[list['Follow']] = relationship(
        'Follow', 
        foreign_keys='Follow.following_id', 
        back_populates='following'
    )
    following: Mapped[list['Follow']] = relationship(
        'Follow', 
        foreign_keys='Follow.follower_id', 
        back_populates='follower'
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "bio": self.bio,
            "profile_picture": self.profile_picture,
            "website": self.website,
            "is_private": self.is_private,
            "created_at": self.created_at.isoformat(),
            "posts_count": len(self.posts),
            "followers_count": len(self.followers),
            "following_count": len(self.following)
        }

class Post(db.Model):
    __tablename__ = 'post'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped['User'] = relationship('User', back_populates='posts')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='post')
    likes: Mapped[list['Like']] = relationship('Like', back_populates='post')

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "location": self.location,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "likes_count": len(self.likes),
            "comments_count": len(self.comments),
            "user": self.user.serialize() if self.user else None
        }

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped['User'] = relationship('User', back_populates='comments')
    post: Mapped['Post'] = relationship('Post', back_populates='comments')

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
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

class Follow(db.Model):
    __tablename__ = 'follow'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    follower: Mapped['User'] = relationship('User', foreign_keys=[follower_id], back_populates='following')
    following: Mapped['User'] = relationship('User', foreign_keys=[following_id], back_populates='followers')

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "following_id": self.following_id,
            "created_at": self.created_at.isoformat()
        }

class Story(db.Model):
    __tablename__ = 'story'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    media_url: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    
    # Relationships
    user: Mapped['User'] = relationship('User', back_populates='stories')

    def serialize(self):
        return {
            "id": self.id,
            "media_url": self.media_url,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "user": self.user.serialize() if self.user else None
        }from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    profile_picture: Mapped[str] = mapped_column(String(255), nullable=True)
    website: Mapped[str] = mapped_column(String(255), nullable=True)
    is_private: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    posts: Mapped[list['Post']] = relationship('Post', back_populates='user')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user')
    likes: Mapped[list['Like']] = relationship('Like', back_populates='user')
    stories: Mapped[list['Story']] = relationship('Story', back_populates='user')
    
    # Follow relationships
    followers: Mapped[list['Follow']] = relationship(
        'Follow', 
        foreign_keys='Follow.following_id', 
        back_populates='following'
    )
    following: Mapped[list['Follow']] = relationship(
        'Follow', 
        foreign_keys='Follow.follower_id', 
        back_populates='follower'
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "bio": self.bio,
            "profile_picture": self.profile_picture,
            "website": self.website,
            "is_private": self.is_private,
            "created_at": self.created_at.isoformat(),
            "posts_count": len(self.posts),
            "followers_count": len(self.followers),
            "following_count": len(self.following)
        }

class Post(db.Model):
    __tablename__ = 'post'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped['User'] = relationship('User', back_populates='posts')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='post')
    likes: Mapped[list['Like']] = relationship('Like', back_populates='post')

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "location": self.location,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "likes_count": len(self.likes),
            "comments_count": len(self.comments),
            "user": self.user.serialize() if self.user else None
        }

class Comment(db.Model):
    __tablename__ = 'comment'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped['User'] = relationship('User', back_populates='comments')
    post: Mapped['Post'] = relationship('Post', back_populates='comments')

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
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

class Follow(db.Model):
    __tablename__ = 'follow'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    follower: Mapped['User'] = relationship('User', foreign_keys=[follower_id], back_populates='following')
    following: Mapped['User'] = relationship('User', foreign_keys=[following_id], back_populates='followers')

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "following_id": self.following_id,
            "created_at": self.created_at.isoformat()
        }

class Story(db.Model):
    __tablename__ = 'story'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    media_url: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    
    # Relationships
    user: Mapped['User'] = relationship('User', back_populates='stories')

    def serialize(self):
        return {
            "id": self.id,
            "media_url": self.media_url,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "user": self.user.serialize() if self.user else None
        }