class Game:
    """
    A game.
    """
    # current game sequence number
    _current_sequence = 1
    # TODO: Optimize for runtime (replace calculations by constants)

    def __init__(self, team1, team2, score1, score2):
        """
        Instantiates a new game.
        The order of the teams is not important as long as it matches the
        order of the score values.
        Parameters:
            team1 - The first team.
            team2 - The second team.
            score1 - The score of the first team.
            score2 - The score of the second team.
        """
        self.team1 = team1
        self.team2 = team2
        self.score1 = score1
        self.score2 = score2
        self.num = Game._current_sequence
        Game._current_sequence += 1
        team1.add_game(self)
        team2.add_game(self)

    def __str__(self):
        """
        Returns:
        A string representation of the game in the form:
        Team 1 vs. Team 2 - 1:0
        """
        return self.team1.name + " vs. " + self.team2.name + " - " + str(self.score1) + ":" + str(self.score2)

    def __repr__(self):
        """
        Returns:
            str(self)
        """
        return str(self)

    def is_winner(self, team):
        """
        Returns True if the specified team won this game.
        Parameters:
            team - The team to check.
        Returns:
            True if the team specified by the parameter won this game. False
            otherwise.
        """
        # TODO: Raise TeamNotFound exception if the team didn't play this game.
        if self.team1 == team and self.score1 > self.score2:
            return True
        if self.team2 == team and self.score2 > self.score1:
            return True
        return False

    def jugg_diff(self, team = None):
        """
        Returns the jugg difference of this game for the specified team.
        Parameters:
            team - The team to compute the jugg difference for.
        Returns:
            The jugg difference for the specified team or the absolute jugg
            difference if no team was given.
        """
        # TODO: Raise TeamNotFound exception if the team didn't play this game.
        if team == None:
            return abs(self.score1 - self.score2)
        elif team == self.team1:
            return self.score1 - self.score2
        else:
            return self.score2 - self.score1

    def loser(self):
        """
        Returns:
            The losing team.
        """
        if self.score1 > self.score2:
            return self.team2
        else:
            return self.team1

    def opponent(self, team):
        """
        Parameters:
            team - The team whose opponent should be returned.
        Returns:
            The opponent of the team given as a parameter.
        """
        # TODO: Raise TeamNotFound exception if the team didn't play this game.
        if self.team1 == team:
            return self.team2
        else:
            return self.team1

    def winner(self):
        """
        Returns:
            The winning team.
        """
        if self.score1 > self.score2:
            return self.team1
        else:
            return self.team2

class Team:
    """
    A team.
    """
    # TODO: Replace calculations by variables (Game.__init__ etc. should update them)
    def __init__(self, name):
        """
        Instantiates a new team.
        Parameters:
            name - The name of the team.
            games - An optional list of games to add to this team.
        """
        # the name of the team
        self.name = name
        # a list of Game instances
        self._games = []
        # the overall jugg difference
        self._total_jugg_difference = 0
        # the number of games this team has won
        self._wins = 0

    def __str__(self):
        """
        Returns the team's name.
        """
        return self.name

    def __repr__(self):
        """
        See team.__str__(self)
        """
        return str(self)
    
    def add_game(self, game):
        """
        Adds a game for this team. This should need to be called by the user.
        Game.__init__ calls this for both teams.
        Parameters:
            game - The game to add.
        """
        self._games.append(game)
        self._total_jugg_difference += game.jugg_diff(self)
        if game.is_winner(self):
            self._wins += 1

    def jugg_diff(self, relevant_teams = None):
        """
        Returns the jugg difference for this team.
        If relevant_teams is given, only the games against teams in this
        iterable are counted for the jugg difference.
        Parameters:
            relevant_teams - The teams that should be counted when computing
                             the jugg difference. The type can be arbitrary as
                             long as membership can be checked (if team in
                             relevant_teams)
        Returns:
            The jugg difference over all games against relevant teams (or all).
        """
        if len(self._games) == 0:
            return 0
        if relevant_teams is None:
            return self._total_jugg_difference
        diff = 0
        for game in self._games:
            if game.opponent(self) in relevant_teams:
                diff += game.jugg_diff(self)
        return diff

    def normalized_jugg_diff(self, relevant_teams = None):
        """
        Returns the "normalized" jugg difference. It is computed as the jugg
        difference divided by the number of (relevant) games.
        The rest is similar to Team.jugg_diff.
        Parameters:
            relevant_teams - Same as in Team.jugg_diff
        Returns:
            The jugg difference divided by the number of (relevant) games.
        """
        if len(self._games) == 0:
            return 0
        if relevant_teams is None:
            return self.jugg_diff() / len(self._games)
        else:
            num_games = 0
            for game in self._games:
                if game.opponent(self) in relevant_teams:
                    num_games += 1
            if num_games == 0:
                return 0
            return self.jugg_diff(relevant_teams) / num_games

    def opponents(self):
        """
        Returns:
            A set of all opponents (Teams) this team has played against.
        """
        return {game.opponent(self) for game in self._games}

    def wins(self):
        """
        Returns:
            The number of games this team has won.
        """
        return self._wins
