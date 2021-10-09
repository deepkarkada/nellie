"""A module that takes a DialogueAct as an input and transforms it into a text output to say for the agent"""
from retico.core.text.common import TextIU, GeneratedTextIU

from retico.core import abstract
from retico.core.dialogue.common import DialogueActIU

response_dictionary = {
    "TargetIdentified": "Got It",
    "Skip": "Let's skip this one"
}

class NaturalLanguageGeneration(abstract.AbstractModule):
    """Currently a dummy NLG Module
    TODO: Incorpoate a real lookup table
    """

    @staticmethod
    def name():
        return "Natural Language Generation"

    @staticmethod
    def description():
        return "A Module that turns response DAs into text"

    @staticmethod
    def input_ius():
        return [DialogueActIU]

    @staticmethod
    def output_iu():
        return GeneratedTextIU

    def __init__(self, game_memory, target_memory, incremental=False, **kwargs):
        super().__init__(**kwargs)
        self.incremental = incremental
        self.game_memory = game_memory
        self.target_memory = target_memory

    def get_current_dialogue_act(self, input_iu):
        return input_iu.act, input_iu.concepts, input_iu.confidence

    def process_iu(self, input_iu):
        act, concepts, confidence = self.get_current_dialogue_act(input_iu)
        if not act:
            return None
        print("NLG is processing a DA of type " + str(act) + " with the following values - Concept: " + str(concepts) + "; Confidence: " + str(confidence))

        output_iu = self.create_iu(input_iu)
        output_iu.payload = response_dictionary[act]
        output_iu.dispatch = True

        #Increment the agent turns before sending the IU
        self.target_memory.increment_agent_turns()
        self.game_memory.increment_total_agent_turns()
        return output_iu