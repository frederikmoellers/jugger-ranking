from ranking_providers.fcfjr.graph import Graph
from jugger_types import Game, Team
from ranking_providers import RankingProvider

class FCFJR(RankingProvider):
    """
    Fred's completely fair Jugger ranking.
    From the teams and games, a graph is built. For each team, there's a
    vertice. Between teams that have played against each other there is an
    edge. The weight of the edge is the sum of the jugg differences of all
    games these two teams have played against each other. The direction of the
    edge is so that the weight is positive (A->B if A has scored more juggs in
    all games A vs. B). There are 2 edges, one in each direction, with weight 0
    if the jugg difference sums up to 0.
    The graph is then sorted topologically where circles are treated as super-
    nodes and thus land on the same place. To solve these circles, the games
    between the teams within the circle are checked. The teams are ordered
    according to their "normalized circular jugg difference" (the jugg
    difference over all games that were played between teams within the circle,
    divided by the number of these games). If multiple teams are then still on
    the same place, they are ordered according to their "normalized tie breaker
    jugg difference", the jugg difference over all games that these teams have
    played against a set of common opponents divided by the number of these
    games. This means that only those games are counted that were played
    against common opponents (e.g. if A and B have both played against C then
    those games are counted; if only A has played against D, this game is not
    counted).
    Teams that then are on the same place stay on the same place.
    """
    # TODO: make a picture to explain this
    # TODO: Complexity?

    _fields = ("Place", "Team", "Norm. Circ. Jugg diff.", "T.B. Jugg diff.")
    _field_lengths = (2, 30, 2, 2)
    _field_alignments = (False, True, False, False)

    def __init__(self):
        """
        Instantiates this ranking provider.
        """
        self._team_graph = Graph()

    def add_game(self, game):
        self._team_graph.add_edge(game.winner(), game.loser(), game.jugg_diff())

    def add_team(self, team):
        self._team_graph.add_node(team)

    def get_ranking(self):
        """
        Returns an ordering of the teams.
        Returns:
            A list of tuples.
            The first tuple tells what fields are there and their lengths.
            The secont tuple tells which fields are to be left-aligned (True/False).
            The third and following tuples contain the teams and their data.
        """
        team_list = []
        current_place = 1
        for place in self._team_graph.topological_sort():
            place_list = []
            relevant_teams = set()
            for circle in place:
                relevant_teams |= circle
            place = [[(team.normalized_jugg_diff(relevant_teams), team.name, team) for team in circle] for circle in place]
            for circle in place:
                circle.sort(reverse = True)
            while place:
                place_list.append(set())
                i = 0
                while i < len(place):
                    circle = place[i]
                    jd = circle[0][0]
                    while circle and circle[0][0] == jd:
                        place_list[-1].add(circle.pop(0))
                    if not circle:
                        place.remove(circle)
                    else:
                        i += 1
            for same_place_set in place_list:
                # tie breaker
                if len(same_place_set) > 1:
                    # teams that everyone on this place played against
                    relevant_teams = self._team_graph.nodes()
                    for circ_jugg_diff, name, team in same_place_set:
                        relevant_teams &= team.opponents()
                    # jugg differences against relevant teams
                    rel_jugg_diffs = set()
                    for team_tuple in same_place_set:
                        rel_jugg_diffs.add((team_tuple, team_tuple[2].jugg_diff(relevant_teams)))
                    # pop all teams, highest relevant jugg difference first
                    while rel_jugg_diffs:
                        # current maximum
                        max_rel_jugg_diff = None
                        # teams with maximum jugg difference
                        to_remove = None
                        for team_tuple, rel_jugg_diff in rel_jugg_diffs:
                            # new maximum
                            if max_rel_jugg_diff is None or rel_jugg_diff > max_rel_jugg_diff[0]:
                                max_rel_jugg_diff = (rel_jugg_diff, {team_tuple})
                                to_remove = {(team_tuple, rel_jugg_diff)}
                            # same as maximum
                            elif rel_jugg_diff == max_rel_jugg_diff[0]:
                                max_rel_jugg_diff[1].add(team_tuple)
                                to_remove.add((team_tuple, rel_jugg_diff))
                        # remove teams with maximum jugg difference
                        rel_jugg_diffs -= to_remove
                        # add teams to listing
                        for (circ_jugg_diff, name, team), rel_jugg_diff in to_remove:
                            team_list.append((current_place, team, circ_jugg_diff, rel_jugg_diff))
                        current_place += 1
                else:
                    circ_jugg_diff, name, team = same_place_set.pop()
                    team_list.append((current_place, team, circ_jugg_diff, 0))
                    current_place += 1
        return team_list
