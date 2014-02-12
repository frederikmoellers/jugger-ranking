import abc

class RankingProvider(metaclass = abc.ABCMeta):
    """
    This is an abstract base class for ranking providers. Any class that
    implements this abstract class can be used as a ranking provider for this
    framework.
    """
    # The fields this ranking supplies for each team. By convention, the first 2 fields should be "Rank" and "Team Name".
    _fields = ("Rank", "Team Name")
    # The maximum lengths for the fields (number of characters)
    _field_lengths = (2, 30)
    # The alignment of the fields. True is left-aligned, False is right-aligned.
    _field_alignments = (False, True)

    @abc.abstractmethod
    def add_game(self, game):
        """
        This method should handle a new game result.
        """
        pass

    @abc.abstractmethod
    def add_team(self, team):
        """
        This method should handle the addition of a new team.
        """
        pass

    def fields(self):
        """
        Returns the fields for this ranking, their maximum lengths and their
        alignments.
        Returns:
            A 3-tuple containing tuples of equal length:
            The first tuple contains the field names.
            The second tuple contains the fields' maximum lengths.
            The third tuple contains the fields' alignments (True = left,
            False = right).
        """
        return (self._fields, self._field_lengths, self._field_alignments)

    @abc.abstractmethod
    def get_ranking(self):
        """
        This method should return a ranking of the teams.
        Returns:
            A list of tuples that have lengths equal to those returned by
            fields(). Each tuple has elements corresponding to the fields (the
            first tuple of fields()).
            The list is sorted in descending order.
        """
        pass
