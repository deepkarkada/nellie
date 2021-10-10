from retico.core import abstract


class GameStateUpdateIU(abstract.IncrementalUnit):
    """A Game State Update Incremental Unit.

    This IU represents the incoming game state that is requested from the server.

    Attributes:
        state (string): Whether the game is running or not
        time left (int): Time in seconds that is left in the current game
        points (int): The current total score
        pointArray (list): A list of scores accumulated over the past targets
    """

    @staticmethod
    def type():
        return "Game State Update Incremental Unit"

    def __init__(self, creator=None, iuid=0, previous_iu=None, grounded_in=None,
                 payload=None, **kwargs):
        """Initialize the GameStateUpdateIU with the respective attributes"""

        super().__init__(creator=creator, iuid=iuid, previous_iu=previous_iu,
                         grounded_in=grounded_in, payload=payload)
        self.game_state = None
        self.time_left = -1
        self.points = -1
        self.pointArray = []

    def set_values(self, game_state=None, time_left=-1, points=-1, point_array=[]):
        self.game_state = game_state
        self.time_left = time_left
        self.points = points
        self.point_array = point_array
