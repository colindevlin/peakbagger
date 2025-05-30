from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Boolean
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('sqlite:///peak_data.db')

Session = sessionmaker(bind=engine)
db_session = Session()

Base = declarative_base()

class Peak(Base):
    __tablename__ = 'peak'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    range = Column(String)

    lists = relationship("PeakList", secondary="peak_list_association", back_populates="peaks")

class PeakList(Base):
    __tablename__ = 'peak_list'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    peaks = relationship("Peak", secondary="peak_list_association", back_populates="lists")

class PeakListAssociation(Base):
    __tablename__ = 'peak_list_association'
    peak_id = Column(Integer, ForeignKey('peak.id'), primary_key=True)
    list_id = Column(Integer, ForeignKey('peak_list.id'), primary_key=True)


Base.metadata.create_all(engine)