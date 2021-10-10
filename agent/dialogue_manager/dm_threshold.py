"""A module that manages the dialogue flow based on the NLU input"""
from agent.game_integration.common import GameStateUpdateIU
from retico.core import abstract
from retico.core.dialogue.common import DialogueActIU

THRESHOLD_IDENTIFIED = 0.3
THRESHOLD_SKIP = 5

class DialogueManager(abstract.AbstractModule):
    """Threshold-based Dialogue Manager.
    This is a simple baseline DM that can only produce two Output-DAs:
    (i) TargetIdentified: If the threshold of one of the countries exceeds the THRESHOLD_IDENTIFIER, the agent
    says "Got it"
    (ii) Skip: If the human took at least THRESHOLD_SKIP turns, the agents says "Let's skip"
    """

    @staticmethod
    def name():
        return "Threshold-based Dialogue Manager"

    @staticmethod
    def description():
        return "A Module managing the dialogue in the agent"

    @staticmethod
    def input_ius():
        return [DialogueActIU, GameStateUpdateIU]

    @staticmethod
    def output_iu():
        return [DialogueActIU]

    def read_country_ids(self):
        with open("../data/agent/countrynames_id.txt") as f:
            for line in f:
                (key, val) = line.split("\t")
                val = val.replace("\n","")
                self.country_to_ids[val] = key
                self.ids_to_country[key] = val

    def __init__(self, game_memory, target_memory, incremental=True, **kwargs):
        super().__init__(**kwargs)
        self.ids_to_country = {}
        self.country_to_ids = {}
        self.incremental = incremental
        self.game_memory = game_memory
        self.target_memory = target_memory
        self.read_country_ids()

    def get_current_dialogue_act(self, input_iu):
        return input_iu.act, input_iu.concepts, input_iu.confidence

    def process_iu(self, input_iu):
        if type(input_iu) is DialogueActIU:
            act, concepts, confidence = self.get_current_dialogue_act(input_iu)

            if not act:
                return None

            if act == "TargetDescription":
                """This is input from the Description NLU"""
                pred_entities = concepts["pred_entities"]
                country_max_conf = max(pred_entities, key=pred_entities.get)
                max_conf = pred_entities[country_max_conf]

                print("DM is processing a DA of type " + str(act) + " with max confidence country for " + str(country_max_conf) + " (" + str(max_conf) + ")")

                if max_conf >= THRESHOLD_IDENTIFIED:
                    output_iu = self.create_iu(input_iu)
                    output_iu.set_act("TargetIdentified", self.country_to_ids[country_max_conf])
                    return output_iu

            if self.target_memory.get_human_turns() >= THRESHOLD_SKIP:
                output_iu = self.create_iu(input_iu)
                output_iu.set_act("Skip")
                return output_iu
        elif type(input_iu) is GameStateUpdateIU:
            print("DM is processing a game state update; game state is " + str(input_iu.game_state) + "; we have " + str(
                input_iu.time_left) + " seconds left in the game and currently scored " + str(input_iu.points) + " points.")
            self.game_memory.set_current_score(input_iu.points)
            self.game_memory.set_remaining_game_time(input_iu.time_left)
            self.game_memory.set_point_array(input_iu.point_array)
            self.game_memory.set_game_state(input_iu.game_state)

