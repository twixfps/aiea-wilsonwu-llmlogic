% NBA Knowledge Base

% Teams
team(lakers).
team(celtics).
team(warriors).
team(bulls).
team(heat).

% Conferences
conference(lakers, west).
conference(warriors, west).
conference(celtics, east).
conference(bulls, east).
conference(heat, east).

% Championships
championships(lakers, 17).
championships(celtics, 18).
championships(warriors, 7).
championships(bulls, 6).
championships(heat, 3).

% Rules

% A team is historically winning if it has at least 6 championships.
historically_winning(Team) :-
    championships(Team, Titles),
    Titles >= 6.

% A team belongs to the Eastern Conference.
eastern_team(Team) :-
    conference(Team, east).

% A team belongs to the Western Conference.
western_team(Team) :-
    conference(Team, west).

% A team is a champion franchise if it has at least one championship.
champion_franchise(Team) :-
    championships(Team, Titles),
    Titles > 0.

% A team is highly successful if it has at least 10 championships.
highly_successful(Team) :-
    championships(Team, Titles),
    Titles >= 10.

% A team is a historic Eastern Conference team if it is in the East
% and is historically winning.
historic_east_team(Team) :-
    conference(Team, east),
    historically_winning(Team).