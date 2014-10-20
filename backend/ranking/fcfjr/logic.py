from django.core.files import File
from graph import Graph
from juggerranking.models import Game, Team
from pygraphviz import AGraph
from ranking.models import RankedTeam, RankingPicture
import tempfile

def asciiname(team):
    """
    Convert a team name to ascii
    """
    return team.name.encode('ascii', 'ignore')

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
def recalculate(user):
    # remove old ranking
    RankedTeam.objects.filter(team__user = user).delete()
    for pic in RankingPicture.objects.all():
        pic.image.delete()
        pic.delete()

    team_graph = Graph()
    gvfull = AGraph(directed = True)
    for team in user.teams.all():
        gvfull.add_node(asciiname(team), label = team.name)
        team_graph.add_node(team)
    for game in Game.objects.filter(team_1__user = user, team_2__user = user):
        team_graph.add_edge(game.winner(), game.loser(), game.jugg_diff())
    for source, dest, weight in team_graph.edges():
        gvfull.add_edge(asciiname(source), asciiname(dest), label = str(weight))
    with tempfile.NamedTemporaryFile(suffix = ".png") as tmp:
        gvfull.draw(tmp, "png", "dot")
        pic = RankingPicture(user = user, image = File(tmp), title = "Full Team Graph")
        pic.save()

    current_place = 1
    gvcircles = AGraph(directed = True)
    gvtiebreaker = AGraph(directed = True)
    for place in team_graph.topological_sort():
        place_list = []
        relevant_teams = set()
        for circle in place:
            relevant_teams |= circle
            if len(circle) == 1:
                continue
            for team in circle:
                gvcircles.add_node(asciiname(team), label = team.name)
            for source, dest, weight in team_graph.edges():
                if source in circle and dest in circle:
                    gvcircles.add_edge(asciiname(source), asciiname(dest), label = str(weight))
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
                relevant_teams = team_graph.nodes()
                for circ_jugg_diff, name, team in same_place_set:
                    opponents = set()
                    for game in team.games():
                        if game.team_1 == team:
                            opponents.add(game.team_2)
                        else:
                            opponents.add(game.team_1)
                    relevant_teams &= opponents
                if len(relevant_teams) > 0:
                    for team in relevant_teams:
                        gvtiebreaker.add_node("b-" + asciiname(team), label = team.name)
                    for void, void, team in same_place_set:
                        gvtiebreaker.add_node("a-" + asciiname(team), label = team.name)
                        for game in team.games():
                            if game.team_1 == team and game.team_2 in relevant_teams:
                                if game.winner() == team:
                                    gvtiebreaker.add_edge("a-" + asciiname(team), "b-" + asciiname(game.team_2), label = game.jugg_diff())
                                else:
                                    gvtiebreaker.add_edge("b-" + asciiname(game.team_2), "a-" + asciiname(team), label = game.jugg_diff())
                            elif game.team_2 == team and game.team_1 in relevant_teams:
                                if game.winner() == team:
                                    gvtiebreaker.add_edge("a-" + asciiname(team), "b-" + asciiname(game.team_1), label = game.jugg_diff())
                                else:
                                    gvtiebreaker.add_edge("b-" + asciiname(game.team_1), "a-" + asciiname(team), label = game.jugg_diff())
                # jugg differences against relevant teams
                rel_jugg_diffs = set()
                for team_tuple in same_place_set:
                    rel_jugg_diffs.add((team_tuple, team_tuple[2].normalized_jugg_diff(relevant_teams)))
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
                        RankedTeam.objects.create(place = current_place, team = team)
                    current_place += 1
            else:
                circ_jugg_diff, name, team = same_place_set.pop()
                RankedTeam.objects.create(place = current_place, team = team)
                current_place += 1
    with tempfile.NamedTemporaryFile(suffix = ".png") as tmp:
        gvcircles.draw(tmp, "png", "dot")
        pic = RankingPicture(user = user, image = File(tmp), title = "Circles")
        pic.save()
    with tempfile.NamedTemporaryFile(suffix = ".png") as tmp:
        gvtiebreaker.draw(tmp, "png", "dot")
        pic = RankingPicture(user = user, image = File(tmp), title = "Tie Breaker")
        pic.save()
