"""A module that receives and sends updates from the game server via http requests"""
import time

import requests

from agent.game_integration.common import GameStateUpdateIU
from retico.core.text.common import TextIU, GeneratedTextIU

from retico.core import abstract
from retico.core.dialogue.common import DialogueActIU

class GameUpdates(abstract.AbstractProducingModule):
    """Module for receiving and sending updates from the game server"""

    @staticmethod
    def name():
        return "Game Updates"

    @staticmethod
    def description():
        return "A Module that receives and sends game updates"

    @staticmethod
    def output_iu():
        return GameStateUpdateIU

    def __init__(self, game_id=1, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id

    def select_country(self, country_id):
        r = requests.get(url="http://localhost:8001/game/" + str(self.game_id), params={"selection": country_id})

    def process_iu(self, input_iu):
        time.sleep(0.5)
        r = requests.get(url="http://localhost:8001/game/" + str(self.game_id), params={})
        data = r.json()

        output_iu = self.create_iu(input_iu)
        output_iu.set_values(game_state=data["state"], time_left=data["time_left"], points=data["points"], point_array=data["pointArray"])
        return output_iu