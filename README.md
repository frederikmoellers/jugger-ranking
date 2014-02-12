jugger-ranking
==============

A program to rank jugger teams based on the games they played.
At the moment it only has one ranking system (Fred's Completely Fair Jugger
Ranking) and has no real interface yet.
It can be used as follows:

    $ cd backend
    $ python3
    >>> import ranking_providers.fcfjr
    >>> from jugger_types import Team, Game
    >>> f = ranking_providers.fcfjr.FCFJR()
    >>> t1 = Team("PaderBears")
    >>> t2 = Team("Trollfaust")
    >>> g = Game(t1, t2, 5, 2)
    >>> f.add_team(t1)
    >>> f.add_team(t2)
    >>> f.add_game(g)
    >>> f.fields()
    (('Place', 'Team', 'Norm. Circ. Jugg diff.', 'T.B. Jugg diff.'), (2, 30, 2, 2), (False, True, False, False))
    >>> f.get_ranking()
    [(1, PaderBears, 0, 0), (2, Trollfaust, 0, 0)]

Documentation for the functions is in the code.
