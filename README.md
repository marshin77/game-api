# game-api

1. game instructions for (3 card war) 2 player game, player vs ai:
	a. run create_user endpiont send it a unique user name and an email address(optinal)
	b. run create_game endpiont send it your user name recive a urlsafe_game_key
	c. run make_move endpiont send it your urlsafe_game_key recive results of your match
	d. repeat 3 times win majority of matches win game.

2. descriptions of each endpoint:

	a. cancel game: 
		Path: 'game/{urlsafe_game_key}/end'
		Method: PUT
		Parameters: urlsafe_game_key
		Returns: GameForm with current game state.
		Description: allows users to cancel a game in progress, counts as a loss

	b. create_user: 
		Path: 'user'
		Method: POST
		Parameters: username, email(optinal)
		Returns: string message.
		Description: creates a user with a unique name.

	c. get_game:	
		Path: 'game/{urlsafe_game_key}'
		Method: GET
		Parameters: urlsafe_game_key
		Returns: GameForm with current game state.
		Description: Returns the current state of a game.

	d.get_scores:	
		Path: 'scores'
		Method: GET
		Parameters: none
		Returns: ScoreForms with the score of all games.
		Description: Return all matches and their results/date played/player name

	e.get_user_games:	
		Path: 'game/user/{user_name}'
		Method: GET
		Parameters: user name
		Returns: GameForms from a users active games.
		Description: Returns all of an individual User's active games

	f.get_user_rankings:	
		Path: 'ranks'
		Method: GET
		Parameters: none
		Returns: UserForms with the number of wins a user has.
		Description: Returns users and their # of wins in order by wins

	g.get_user_scores:	
		Path: 'scores/user/{user_name}'
		Method: GET
		Parameters: user name
		Returns: ScoreForms of a user.
		Description: Returns all of an individual User's match results/date played/player name

	h.make_move: 
		Path: 'game/{urlsafe_game_key}'
		Method: PUT
		Parameters: urlsafe_game_key
		Returns: GameForm with current game state and a message about the out come of that match.
		Description: compairs the "cards"(prng 1-25) the players drew decides winner by higher "card"
	(prng#) 

	i.new_game:	
		Path: 'game'
		Method: POST
		Parameters: NewGameForm
		Returns: Gameform.
		Description: Creates new game, requires a user name.

	i.get_game_history:	
		Path: 'history/{urlsafe_game_key}'
		Method: GET
		Parameters: urlsafe_game_key
		Returns: Gameform with the wins/losses of every match in a given game.
		Description: Return the results of every match with in a game 
		
3. explanation of score keeping:
	players are given 3 "cards" players compair each "card" one at a time, the player with higher "card" wins, if "cards" are equal both sides recive a "win".
	after three draws(matches) the player with the most match wins will win the game.
	players are ranked by number of wins
