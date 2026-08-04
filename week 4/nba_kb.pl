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

% Rule:
% A team is considered a historically successful franchise
% if it has won at least 6 NBA championships.
historically_winning(Team) :-
    championships(Team, Titles),
    Titles >= 6.