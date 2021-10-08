"""
A module that reads chat input from the command line
"""
import threading

from retico.core.text.common import SpeechRecognitionIU, TextIU

from retico.core import abstract, text


class ConsoleInput(abstract.AbstractProducingModule):
    """A module that reads chat input from the command line"""

    @staticmethod
    def name():
        return "Command Line Chat"

    @staticmethod
    def description():
        return "A producting module that reads input from the command line."

    @staticmethod
    def output_iu():
        return TextIU

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process_iu(self, input_iu):
        input("User: ")
        output_iu = self.create_iu()
        output_iu.payload = "Test"
        return output_iu



