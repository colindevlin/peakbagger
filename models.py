from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Boolean, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

engine = create_engine('sqlite:///peak_data.db')
Session = sessionmaker(bind=engine)
db_session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)

    peak_lists = relationship(
        'PeakList',
        secondary='user_peaklist_association',
        back_populates='users'
    )

class PeakList(Base):
    __tablename__ = 'peak_list'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    peaks = relationship('Peak', secondary='peak_peaklist_association', back_populates='peak_lists')
    users = relationship('User', secondary='user_peaklist_association', back_populates='peak_lists')

class Peak(Base):
    __tablename__ = 'peak'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    range = Column(String)

    peak_lists = relationship('PeakList', secondary='peak_peaklist_association', back_populates='peaks')

# Declare association tables after all models
peak_peaklist_association = Table(
    'peak_peaklist_association',
    Base.metadata,
    Column('peak_id', Integer, ForeignKey('peak.id')),
    Column('peaklist_id', Integer, ForeignKey('peak_list.id'))
)

user_peaklist_association = Table(
    'user_peaklist_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('peaklist_id', Integer, ForeignKey('peak_list.id'))
)

# Create tables
Base.metadata.create_all(engine)
