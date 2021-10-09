"""A module takes in text input and returns a list with individual text segments"""

from retico.core import abstract
from retico.core.text.common import SpeechRecognitionIU, TextIU, SegmentedTextIU
from retico.core.dialogue.common import DialogueActIU


class Segmenter(abstract.AbstractModule):
    """Currently a dummy implementation
    TODO: Incorpoate an actual segmentation logic
    """

    @staticmethod
    def name():
        return "Text Segmentation"

    @staticmethod
    def description():
        return "A Module segmenting the incoming text into logical chunks"

    @staticmethod
    def input_ius():
        return [SpeechRecognitionIU, TextIU]

    @staticmethod
    def output_iu():
        return SegmentedTextIU

    def __init__(self, game_memory, target_memory, incremental=False, **kwargs):
        super().__init__(**kwargs)
        self.incremental = incremental
        self.game_memory = game_memory
        self.target_memory = target_memory

    def get_current_text(self, input_iu):
        if self.incremental or type(input_iu) is TextIU or (type(input_iu) is SpeechRecognitionIU and input_iu.final):
            return input_iu.get_text()

    def process_iu(self, input_iu):
        current_text = self.get_current_text(input_iu)
        if not current_text:
            return None
        if type(input_iu) is TextIU or (type(input_iu) is SpeechRecognitionIU and input_iu.final):
            #We received a new text input or a FINAL ASR input and hence consider the current human turn as concluded
            self.target_memory.increment_human_turns()
            self.game_memory.increment_total_human_turns()
        print(f"Segmenter is processing text: '{current_text}'")

        output_iu = self.create_iu(input_iu)
        output_iu.payload = {'Description': [["general", current_text]]}
        return output_iu