"""A module for Natural Language Understanding using knowledge graphs"""

from retico.core import abstract
from retico.core.text.common import SpeechRecognitionIU
from retico.core.dialogue.common import DialogueActIU


class KGBasedNLU(abstract.AbstractModule):
    """Currently a dummy NLU Module
    TODO: Incorpoate the knowledge graph
    """

    @staticmethod
    def name():
        return "KG-based NLU Module"

    @staticmethod
    def description():
        return "A Module providing Natural Language Understanding based on knowledge graphs"

    @staticmethod
    def input_ius():
        return [SpeechRecognitionIU]

    @staticmethod
    def output_iu():
        return DialogueActIU

    def __init__(self, incremental=False, **kwargs):
        super().__init__(**kwargs)
        self.incremental = incremental

    def get_current_text(self, input_iu):
        if self.incremental or input_iu.final:
            return input_iu.get_text()

    def process_iu(self, input_iu):
        current_text = self.get_current_text(input_iu)
        if not current_text:
            return None
        print(f"NLU is processing text: '{current_text}'")

        output_iu = self.create_iu(input_iu)
        output_iu.set_act("Description", current_text, 0.9)
        return output_iu