"""A module that manages the dialogue flow based on the NLU input"""

from retico.core import abstract
from retico.core.dialogue.common import DialogueActIU

THRESHOLD_IDENTIFIED = 0.3
THRESHOLD_SKIP = 5

class DialogueManager(abstract.AbstractModule):
    """Currently a dummy DM Module
    TODO: Incorpoate any kind of meaningful DM
    """

    @staticmethod
    def name():
        return "Custom Dialogue Manager"

    @staticmethod
    def description():
        return "A Module managing the dialogue in the agent"

    @staticmethod
    def input_ius():
        return [DialogueActIU]

    @staticmethod
    def output_iu():
        return DialogueActIU

    def read_country_ids(self):
        self.country_to_ids = {}
        self.ids_to_country = {}
        with open("../data/agent/countrynames_id.txt") as f:
            for line in f:
                (key, val) = line.split("\t")
                val = val.replace("\n","")
                self.country_to_ids[val] = key
                self.ids_to_country[key] = val

    def __init__(self, incremental=True, **kwargs):
        super().__init__(**kwargs)
        self.incremental = incremental
        self.read_country_ids()

    def get_current_dialogue_act(self, input_iu):
        return input_iu.act, input_iu.concepts, input_iu.confidence

    def process_iu(self, input_iu):
        act, concepts, confidence = self.get_current_dialogue_act(input_iu)
        if not act:
            return None

        if act == "TargetDescription":
            """This is input from the Description NLU"""
            pred_entities = concepts["pred_entities"]
            country_max_conf = max(pred_entities, key=pred_entities.get)
            max_conf = pred_entities[country_max_conf]

            print("DM is processing a DA of type " + str(act) + " with max confidence country for " + str(country_max_conf) + " (" + str(max_conf) + ")")

            if max_conf > THRESHOLD_IDENTIFIED:
                output_iu = self.create_iu(input_iu)
                output_iu.set_act("TargetIdentified", self.country_to_ids[country_max_conf])
                return output_iu