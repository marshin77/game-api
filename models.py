"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""


from datetime import date
from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email =ndb.StringProperty()
    wins = ndb.IntegerProperty()
    card1 = ndb.IntegerProperty()
    card2 = ndb.IntegerProperty()
    card3 = ndb.IntegerProperty()
    def to_form(self):
        return UserForm(user_name=self.name, email=self.email,
                        wins= self.wins, card1=self.card1, card2=self.card2,
                        card3=self.card3)

class Game(ndb.Model):
    """Game object"""
    match_wins = ndb.IntegerProperty()
    match_losses = ndb.IntegerProperty()
    game_over = ndb.BooleanProperty(required=True, default=False)
    user = ndb.KeyProperty(required=True, kind='User')
    match = ndb.IntegerProperty()
    
    @classmethod
    def new_game(cls, user):
        """Creates and returns a new game"""
        
        game = Game(user=user, match_wins=0, match=3,
                    match_losses=0, game_over=False)
        game.put()
        return game

    def to_form(self, message):
        """Returns a GameForm representation of the Game"""
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.game_over = self.game_over
        form.message = message
        form.match_wins = self.match_wins
        form.match_losses = self.match_losses
        form.match = self.match
        return form

    def end_game(self):
        """Ends the game - if won is True, the player won. - if won is False,
        the player lost."""
        self.game_over = True
        self.put()
        won = False
        if self.match_wins >= 2:
            won = True
        # Add the game to the score 'board'
        score = Score(user=self.user, date=date.today(), won=won)
        score.put()
        #if the player wins the game add a win to their user data
        user = User.query(User.key==self.user).get()
        if won == True:
            user.wins = user.wins + 1
            user.put()

class Score(ndb.Model):
    """Score object"""
    user = ndb.KeyProperty(required=True, kind='User')
    date = ndb.DateProperty(required=True)
    won = ndb.BooleanProperty(required=True)
    

    def to_form(self):
        return ScoreForm(user_name=self.user.get().name, won=self.won,
                         date=str(self.date))


class GameForm(messages.Message):
    """GameForm for outbound game state information"""
    urlsafe_key = messages.StringField(1, required=True)
    game_over = messages.BooleanField(3, required=True)
    message = messages.StringField(4, required=True)
    user_name = messages.StringField(5, required=True)
    match_wins = messages.IntegerField(6)
    match_losses = messages.IntegerField(7)
    match = messages.IntegerField(8)
    
class GameForms(messages.Message):
    """Return multiple GameForms"""
    items = messages.MessageField(GameForm, 1, repeated=True)

class NewGameForm(messages.Message):
    """Used to create a new game"""
    user_name = messages.StringField(1, required=True)

    



    


class ScoreForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    date = messages.StringField(2, required=True)
    won = messages.BooleanField(3, required=True)
    


class ScoreForms(messages.Message):
    """Return multiple ScoreForms"""
    items = messages.MessageField(ScoreForm, 1, repeated=True)

class UserForm(messages.Message):
    """ScoreForm for outbound Score information"""
    user_name = messages.StringField(1, required=True)
    email = messages.StringField(2)
    wins = messages.IntegerField(3, required=True)
    card1 = messages.IntegerField(4)
    card2 = messages.IntegerField(5)
    card3 = messages.IntegerField(6)

class UserForms(messages.Message):
    """Return multiple UserForms"""
    items = messages.MessageField(UserForm, 1, repeated=True)

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
