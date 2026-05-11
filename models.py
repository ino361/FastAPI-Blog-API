from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from database import Base   
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title =Column(String, index=True, nullable=True)
    content= Column(Text, nullable=True)
    created_at= Column(DateTime(timezone=True), server_default = func.now())
    is_published= Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    owner = relationship('Users')
    comments = relationship("Comments", back_populates="post", cascade='all, delete-orphan')
    images = relationship("PostImages", back_populates="post", cascade="all, delete-orphan")

class Admin(Base):

    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, index=True )
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Users(Base):
    __tablename__ = 'users'

    id =Column(Integer,primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    mail = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True , index=True, autoincrement=True, nullable=False)
    text = Column(String, nullable=True)
    is_published =Column(Boolean, default=True)
    created_at =Column(DateTime(timezone=True), server_default = func.now())
    owner_id = Column(Integer, ForeignKey('users.id', ondelete = 'CASCADE'), nullable=False )
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    image_path =Column(String, nullable=True)


    owner =relationship('Users')
    post = relationship('Post', back_populates='comments')


class Read(Base):
    __tablename__ = 'read_posts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PostImages(Base):
    __tablename__ = 'post_images'
    id = Column(Integer,primary_key=True, index=True)
    post_id = Column(Integer,ForeignKey('posts.id', ondelete='CASCADE'),nullable=False)
    images_path = Column(String, nullable=False)
    post = relationship('Post', back_populates='images')