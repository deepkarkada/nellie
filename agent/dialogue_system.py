from retico.core.debug.printer import PrintModule
from retico.modules.google.asr import GoogleASRModule
from retico.core.audio.io import MicrophoneModule

class Agent():

    def __init__(self):
        self.microphone_input = MicrophoneModule(5000)
        self.asr = GoogleASRModule()
        self.printer = PrintModule()

    def setup(self):
        #setup modules where necessary
        self.asr.setup()

        #connect the modules so they can listen to the IUs from the other modules
        self.microphone_input.subscribe(self.asr)
        self.asr.subscribe(self.printer)

    def start_agent(self):
        self.microphone_input.run()
        self.asr.run()
        self.printer.run()

    def stop_agent(self):
        self.microphone_input.stop()
        self.asr.stop()
        self.printer.stop()