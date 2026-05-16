from sqlalchemy import Column, Integer, String, DateTime, Table, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from database import Base   
from sqlalchemy.orm import relationship

# ----------------------------------------------------
# ARA TABLOLAR (Many-to-Many)
# ----------------------------------------------------

post_likes = Table(
    'post_likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('post_id', Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
)

user_follows = Table(
    'user_follows',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
)

# ----------------------------------------------------
# MODELLER
# ----------------------------------------------------

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    mail = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)

    # İlişkiler
    posts = relationship('Post', back_populates='owner')
    liked_posts = relationship('Post', secondary=post_likes, back_populates='liked_posts_by_users')
    
    # DÜZELTME: primaryjoin ve secondaryjoin kısımlarına explicit olarak Users.id eklendi
    following = relationship(
        'Users', 
        secondary=user_follows, 
        primaryjoin="Users.id==user_follows.c.follower_id", 
        secondaryjoin="Users.id==user_follows.c.followed_id", 
        back_populates='followers'
    )

    followers = relationship(
        'Users',
        secondary=user_follows,
        primaryjoin="Users.id==user_follows.c.followed_id",
        secondaryjoin="Users.id==user_follows.c.follower_id",
        back_populates='following'
    )
    
    # DÜZELTME: foreign_keys listesine doğrudan Notification sınıfının değişkeni verildi
    notifications = relationship('Notification', back_populates='receiver', cascade='all, delete-orphan', foreign_keys="[Notification.receiver_id]")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_published = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    estimated_read_time = Column(Integer, nullable=True)

    # İlişkiler
    owner = relationship('Users', back_populates='posts')
    comments = relationship("Comments", back_populates="post", cascade='all, delete-orphan')
    images = relationship("PostImages", back_populates="post", cascade="all, delete-orphan")
    liked_posts_by_users = relationship('Users', secondary=post_likes, back_populates='liked_posts')


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    receiver_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)
    sender_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=True)

    # İlişkiler
    # DÜZELTME: String veya liste bazlı eşleşme netleştirildi
    receiver = relationship('Users', back_populates='notifications', foreign_keys=[receiver_id])
    post = relationship('Post', foreign_keys=[post_id])


class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)

    user = relationship('Users')


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    text = Column(String, nullable=True)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    image_path = Column(String, nullable=True)

    owner = relationship('Users')
    post = relationship('Post', back_populates='comments')


class Read(Base):
    __tablename__ = 'read_posts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PostImages(Base):
    __tablename__ = 'post_images'
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    images_path = Column(String, nullable=False)
    
    post = relationship('Post', back_populates='images')