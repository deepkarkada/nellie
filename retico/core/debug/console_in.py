"""
A module that reads chat input from the command line
"""
import threading
import time

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

    def __init__(self, agent, **kwargs):
        super().__init__(**kwargs)
        self.agent = agent

    def process_iu(self, input_iu):
        time.sleep(2)
        text_in = input("User: ")
        if text_in == "!QUIT!":
            self.agent.stop_agent()
        else:
            output_iu = self.create_iu()
            output_iu.payload = text_in
            return output_iu



