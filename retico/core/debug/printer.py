"""
A module that simply transcribes incoming text
"""
from retico.core import abstract, text


class PrintModule(abstract.AbstractModule):
    """
    A Moduel that prints SpeechRecognitionIUs.
    """

    @staticmethod
    def output_iu():
        pass

    @staticmethod
    def name():
        return "Print ASR Results"

    @staticmethod
    def description():
        return (
            "A module that uses SpeechRecognition IUs and prints them"
        )

    @staticmethod
    def input_ius():
        return [text.common.SpeechRecognitionIU, text.common.TextIU]

    def __init__(self, forward_after_final=False, **kwargs):
        super().__init__(**kwargs)
        self.forward_after_final = forward_after_final

    def process_iu(self, input_iu):
        if isinstance(input_iu, text.common.SpeechRecognitionIU):
            if self.forward_after_final and not input_iu.final:
                return
        asr_result = input_iu.get_text()
        print("Nellie: " + str(asr_result))
