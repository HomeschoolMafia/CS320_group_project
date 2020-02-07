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
