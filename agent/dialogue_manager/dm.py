"""A module that manages the dialogue flow based on the NLU input"""

from retico.core import abstract
from retico.core.dialogue.common import DialogueActIU


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

    def __init__(self, incremental=True, **kwargs):
        super().__init__(**kwargs)
        self.incremental = incremental

    def get_current_dialogue_act(self, input_iu):
        return input_iu.act, input_iu.concepts, input_iu.confidence

    def process_iu(self, input_iu):
        act, concepts, confidence = self.get_current_dialogue_act(input_iu)
        if not act:
            return None
        print("DM is processing a DA of type " + str(act) + " with the following values - Concept: " + str(concepts) + "; Confidence: " + str(confidence))

        output_iu = self.create_iu(input_iu)
        output_iu.set_act("TargetIdentified", "UK")
        return output_iu