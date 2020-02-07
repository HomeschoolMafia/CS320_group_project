from sqlalchemy import Column, Integer, String

from . import Base

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
