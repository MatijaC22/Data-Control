from db.database import Base
from sqlalchemy import Column, CheckConstraint, ForeignKeyConstraint, UniqueConstraint, ForeignKey, func, text
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean, VARCHAR, JSON, TEXT, UUID
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import event

from sqlalchemy import func

class DbUsers(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(TEXT, nullable=False)
    surname = Column(TEXT, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True)
    date_of_birth = Column(DateTime)
    image_url = Column(String)#, ForeignKey='images.id')
    nationality = Column(TEXT, nullable=False)
    access_level = Column(Integer, nullable=False, default=2, server_default=text("2"))
    active = Column(Boolean, default=True, server_default=text("true"))

    jobs = relationship('DbJobs', back_populates='users')
    posts = relationship('DbPosts', back_populates='users', cascade='all, delete-orphan')
    notifications = relationship('DbNotifications', back_populates='users', cascade='all, delete-orphan') # here cascade says it will delete all pages under agent_id if we delete that agent_id
    comments = relationship('DbComments', back_populates='users', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<DbUser(id={self.id}, name={self.name}, surname={self.surname}, password={self.password}, email={self.email}, date_of_birth={self.date_of_birth}, image_url={self.image_url}, nationality={self.nationality}, access_level={self.access_level}, active={self.active})>"

    def to_dict(self):
        user_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return user_dict

class DbJobs(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    last_modify = Column(TIMESTAMP(timezone=True))
    
    users = relationship('DbUsers', back_populates='jobs')
    posts = relationship('DbPosts', back_populates='jobs', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<DbJobs(id={self.id}, reference_number={self.reference_number}, user_id={self.user_id}, post_id={self.post_id}, created_at={self.created_at}, last_modify={self.last_modify})>"
    
    def to_dict(self):
        user_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return user_dict

class DbPosts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    # image_id = Column(Integer)#, ForeignKey='images.id')
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    last_modify = Column(TIMESTAMP(timezone=True))

    users = relationship('DbUsers', back_populates='posts')
    jobs = relationship('DbJobs', back_populates='posts')
    comments = relationship('DbComments', back_populates='posts', cascade='all, delete-orphan')
    notifications = relationship('DbNotifications', back_populates='posts', cascade='all, delete-orphan')
    images = relationship('DbImages', back_populates='posts')

    def __repr__(self):
        return f"<DbPosts(id={self.id}, description={self.description}, user_id={self.user_id}, job_id={self.job_id}, created_at={self.created_at}, last_modify={self.last_modify})>"

    def to_dict(self):
        user_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return user_dict

class DbComments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key= True, index = True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    last_modify = Column(TIMESTAMP(timezone=True))
    
    users = relationship('DbUsers', back_populates='comments')
    posts = relationship('DbPosts', back_populates='comments')

    def __repr__(self):
        return f"<DbComments(id={self.id}, text={self.text}, post_id={self.post_id}, created_at={self.created_at}, last_modify={self.last_modify})>"

    def to_dict(self):
        user_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return user_dict

class DbNotifications(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key= True, index = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime, server_default=func.now())
    last_modify = Column(DateTime)
    is_read = Column(Boolean, default=False)
    message = Column(String)

    posts = relationship('DbPosts', back_populates='notifications')
    users = relationship('DbUsers', back_populates='notifications')  

    def __repr__(self):
        return f"<DbNotifications(id={self.id}, user_id={self.user_id}, post_id={self.post_id}, created_at={self.created_at}, last_modify={self.last_modify}, is_read={self.is_read}, message={self.message})>"

    def to_dict(self):
        user_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return user_dict


class DbImages(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'))

    posts = relationship('DbPosts', back_populates='images')
    # table_ref = Column(Integer) # DA LI DOLAZI IZ USERA ILI POSTA
    # image_folder = Column(TEXT, default='', server_default=text("") )
    # table_item_id = Column(Integer)


    # __table_args__ = (
    #     CheckConstraint('table_ref IN (1, 2)', name='check_table_ref_values'),
    # )

    # user = relationship(DbUsers, foreign_keys=[table_item_id], uselist=False, primaryjoin="and_(DbImages.table_ref == 1, DbImages.table_item_id == User.agent_id)")
    # post = relationship(DbPosts, foreign_keys=[table_item_id], primaryjoin="and_(DbImages.table_ref == 2, DbImages.table_item_id == Post.page_id)")

    # __table_args__ = (
    #     UniqueConstraint('table_ref', 'table_item_id', name='uq_table_ref_table_item_id'),
    # )

    def __repr__(self):
        return f"<DbImages(id={self.id}, post_id={self.post_id})>"

    def to_dict(self):
        user_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return user_dict
    