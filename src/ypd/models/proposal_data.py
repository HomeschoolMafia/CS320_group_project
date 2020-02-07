from sqlalchemy import Column, Integer, String, ForeignKey

from . import Base

class ProposalData(Base):
    """Model describing the non-identifying data of a project proposal posting.

    Columns:
        id (int): Primary key that uniquely identifies a ProposalIdentity
        description (str): The description of the proposed project
    """
    __tablename__ = 'proposal_data'

    id = Column(Integer, ForeignKey('proposal_identity.id'), primary_key=True)
    desciption = Column(String)
