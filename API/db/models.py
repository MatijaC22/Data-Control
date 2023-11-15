from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean, VARCHAR, JSON, TEXT, UUID
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import ForeignKeyConstraint, UniqueConstraint, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from sqlalchemy import func

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(TEXT, nullable=False)
    surname = Column(TEXT, nullable=False)
    password = Column(String)
    email = Column(String, unique=True)
    date_of_birth = Column(DateTime)
    image_url = Column(String)
    nationality = Column(TEXT, nullable=False)
    access_level = Column(Integer, nullable=False)
    active = Column(Boolean)

    def __repr__(self):
        return f"<DbUser(id={self.id}, name={self.name}, surname={self.surname}, password={self.password}, email={self.email}, date_of_birth={self.date_of_birth}, image_url={self.image_url}, nationality={self.nationality}, access_level={self.access_level}, active={self.active})>"

    def to_dict(self):
        user_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return user_dict
    
class DbAgents(Base):
    __tablename__ = 'agents'
    agent_id = Column(Integer, primary_key=True, index=True)
    agent_uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    agent_name = Column(TEXT, unique=True, nullable=False)
    launch_secret = Column(VARCHAR(length=50), unique=True, nullable=False)
    rate = Column(Integer, default=30, nullable=False)
    max_concurrent = Column(Integer, default=1)
    max_delay = Column(Integer, nullable=False)
    fields_order = Column(JSON)
    output_type = Column(VARCHAR(length=50))
    active = Column(Boolean)

    # Relationship with DbPages
    pages = relationship('DbPages', back_populates='agent', cascade='all, delete-orphan') # here cascade says it will delete all pages under agent_id if we delete that agent_id

    # Relationship with DbJobs
    jobs = relationship('DbJobs', back_populates='agent', cascade='all, delete-orphan')

    # Add a UniqueConstraint for the combination of agent_uuid, launch_secret, and agent_name in DbAgents
    __table_args__ = (UniqueConstraint('agent_uuid', 'launch_secret', 'agent_name', name='uq_agents_uuid_secret_name'),)


class DbPages(Base):
    __tablename__ = 'pages'
    page_id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey('agents.agent_id'))
    url = Column(VARCHAR(length=500), unique=True, nullable=False)
    created_at = Column(VARCHAR(length=50), server_default=func.now())
    launched_on = Column(DateTime)
    finalized_at = Column(DateTime)
    last_seen_on = Column(DateTime)
    data = Column(JSON)
    scrape_done = Column(Boolean, nullable=False, default=False)
    mission = Column(VARCHAR(length=255))
    priority = Column(Integer, default=1)

    # Relationship with DbAgents
    agent = relationship('DbAgents', back_populates='pages')

    # # Relationship with DbAgents
    # job = relationship('DbJobs', back_populates='pages')
    

    # Relationship with DbPageJobMatrix
    page_job_matrix = relationship('DbPageJobMatrix', back_populates='pages', cascade='all, delete-orphan')

class DbPageJobMatrix(Base):
    __tablename__ = 'page_job_matrix'
    page_id = Column(Integer, ForeignKey('pages.page_id'), primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.job_id'), primary_key=True)

    # Relationship with DbPages
    pages = relationship('DbPages', back_populates='page_job_matrix')

    # Relationship with DbJobs
    jobs = relationship('DbJobs', back_populates='page_job_matrix')

    # Add a ForeignKeyConstraint for the combination of page_id and job_id in DbPageJobMatrix
    __table_args__ = (
            ForeignKeyConstraint(['page_id'], ['pages.page_id'], name='fk_page_id'),
            ForeignKeyConstraint(['job_id'], ['jobs.job_id'], name='fk_job_id')
        )

class DbJobs(Base):
    __tablename__ = 'jobs'
    job_id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey('agents.agent_id'))
    job_uuid = Column(UUID(as_uuid=True), nullable=False)
    launched_at = Column(DateTime, nullable=False)  # HERE SHOULD BE GOOD TO ADD ON CREATED TO NE NOW() TIMEDATE
    finished_on = Column(DateTime)
    results = Column(JSON)

    # Relationship with DbAgents
    agent = relationship('DbAgents', back_populates='jobs')

    # Relationship with DbPageJobMatrix
    page_job_matrix = relationship('DbPageJobMatrix', back_populates='jobs', cascade='all, delete-orphan')



    
