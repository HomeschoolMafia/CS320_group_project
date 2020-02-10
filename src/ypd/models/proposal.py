from sqlalchemy import Column, Integer, String, ForeignKey

from . import Base

class Proposal:
    def __init__(self, proposal_data, proposal_identity):
        """Model describing the combined data of a project proposal posting.

        Args:
            posting_data (ProposalData): The title of the proposed project
            posting_identity (ProposalIdentity): The comma delimited list of keywords associated with
                            the posting

        Raises:
            ValueError: If proposal_data and proposal_identity correspond to an existing proposal, and
                do not correspond to the same proposal
        """
        if proposal_data.id != proposal_identity.id:
            raise ValueError("Proposal identifier and proposal data do not correspond to the same proposal!")

        self.data = proposal_data
        self.identity = proposal_identity

class ProposalIdentity(Base):
    """Model that allows a user to identify a posting.

        Columns:
            id (int): Primary key that uniquely identifies a Posting_Identity
            title (str): The title of the proposed project
            keywords (str): The comma delimited list of keywords associated with
                            the posting
        """
    __tablename__ = 'proposal_identity'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    keywords = Column(String)

class ProposalData(Base):
    """Model describing the non-identifying data of a project proposal posting.

    Columns:
        id (int): Primary key that uniquely identifies a ProposalIdentity
        description (str): The description of the proposed project
    """
    __tablename__ = 'proposal_data'

    id = Column(Integer, ForeignKey('proposal_identity.id'), primary_key=True)
    desciption = Column(String)
