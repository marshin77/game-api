# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""

import random

import endpoints
from protorpc import remote, messages


from models import User, Game, Score
from models import StringMessage, NewGameForm, GameForm,\
    ScoreForms, GameForms, UserForm, UserForms
from utils import get_by_urlsafe

NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
GET_GAME_REQUEST = endpoints.ResourceContainer(
        urlsafe_game_key=messages.StringField(1),)

USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))



@endpoints.api(name='guess_a_number', version='v1')
class WarApi(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username"""
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                    'A User with that name already exists!')
        user = User(name=request.user_name, email=request.email, wins=0,
                    card1=random.choice(range(1, 26)), card2=random.choice(range(1, 26)),
                    card3=random.choice(range(1, 26)))
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))
    

    @endpoints.method(request_message=NEW_GAME_REQUEST,
                      response_message=GameForm,
                      path='game',
                      name='new_game',
                      http_method='POST')
    def new_game(self, request):
        """Creates new game"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        
        game = Game.new_game(user.key)


  
        
        return game.to_form('Good luck playing war!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, request):
        """Return the current game state."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game:
            return game.to_form('Time to make a move!')
        else:
            raise endpoints.NotFoundException('Game not found!')

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """Makes a move. Returns a game state with message"""
        AI_draw=random.choice(range(1, 26))
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        user =  User.query(game.user==User.key).get()
        
        if game.game_over:
            return game.to_form('Game already over!')
        
        game.match = game.match - 1
        
        if game.match == 2:
            
            if User.card1 == AI_draw:
                game.match_wins = game.match_wins + 1
                game.put()
                return game.to_form('match tie')

            if User.card1 < AI_draw:
                game.match_losses = game.match_losses + 1
                game.put()
                return game.to_form('match loss')
            else:
                game.match_wins = game.match_wins + 1
                game.put()
                return game.to_form('match win')
            
        if game.match == 1:
            
            if User.card2 == AI_draw:
                game.match_wins = game.match_wins + 1
                game.put()
                return game.to_form('match tie')

            if User.card2 < AI_draw:
                game.match_losses = game.match_losses + 1
                game.put()
                return game.to_form('match loss')
            else:
                game.match_wins = game.match_wins + 1
                game.put()
                return game.to_form('match win')
            
        if game.match == 0:
            
            if User.card3 == AI_draw: 
                game.match_wins = game.match_wins + 1
                game.end_game()
                game.put()
                return game.to_form('match tie')

            if User.card3 < AI_draw:
                game.match_losses = game.match_losses + 1
                game.end_game()
                game.put()
                return game.to_form('match loss')
            else:
                game.match_wins = game.match_wins + 1
                game.end_game()
                game.put()
                return game.to_form('match win')
        
       
    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}/end',
                      name='cancel_game',
                      http_method='PUT')
    def cancel_game(self, request):
        """allows users to cancel a game in progress"""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over:
            return game.to_form('Game already over!')
        else:
            game.end_game(False)
            return game.to_form('game canceled')


    @endpoints.method(response_message=ScoreForms,
                      path='scores',
                      name='get_scores',
                      http_method='GET')
    def get_scores(self, request):
        """Return all scores"""
        return ScoreForms(items=[score.to_form() for score in Score.query()])

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=ScoreForms,
                      path='scores/user/{user_name}',
                      name='get_user_scores',
                      http_method='GET')
    def get_user_scores(self, request):
        """Returns all of an individual User's scores"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        scores = Score.query(Score.user == user.key)
        return ScoreForms(items=[score.to_form() for score in scores])

    @endpoints.method(request_message=USER_REQUEST,
                      response_message=GameForms,
                      path='game/user/{user_name}',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, request):
        """Returns all of an individual User's active games"""
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    'A User with that name does not exist!')
        games = Game.query(Game.user == user.key, Game.game_over == False)
        return GameForms(items=[game.to_form("hi") for game in games])

    
    @endpoints.method(response_message=UserForms,
                      path='ranks',
                      name='get_user_rankings',
                      http_method='GET')
    def get_user_rankings(self, request):
        """Returns users in order by wins"""
        users = User.query().order(-User.wins)
        return UserForms(items=[user.to_form() for user in users])
    
    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=GameForm,
                      path='history/{urlsafe_game_key}',
                      name='get_game_history',
                      http_method='GET')
    def get_game_history(self, request):
        """Return the results of every match with in a game ."""
        game = get_by_urlsafe(request.urlsafe_game_key, Game)
        if game.game_over == True:
            return game.to_form("here are the wins/losses of the matches in that game.")
        else:
            raise endpoints.NotFoundException("Game either in progress or does not exist!")
    

api = endpoints.api_server([WarApi])
