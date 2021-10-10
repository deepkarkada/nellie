from agent.dialogue_manager.Memory import GameMemory, TargetMemory
from agent.dialogue_manager.dm_threshold import DialogueManager
from agent.game_integration.game_updates import GameUpdates
from agent.nlg.nlg import NaturalLanguageGeneration
from agent.nlu.nlu_kg_based import KGBasedNLU
from agent.nlu.segmenter import Segmenter
from retico.core.debug.console_in import ConsoleInput
from retico.core.debug.printer import PrintModule
from retico.modules.google.asr import GoogleASRModule
from retico.core.audio.io import MicrophoneModule


class Agent():

    def __init__(self, game_id=1, game_connection=False):
        # self.microphone_input = MicrophoneModule(5000)
        # self.asr = GoogleASRModule()
        self.game_memory = GameMemory()
        self.target_memory = TargetMemory()
        self.game_connection = game_connection
        self.chatin = ConsoleInput(self)
        self.segmenter = Segmenter(game_memory=self.game_memory, target_memory=self.target_memory)
        self.nlu = KGBasedNLU()
        self.dm = DialogueManager(game_memory=self.game_memory, target_memory=self.target_memory)
        self.nlg = NaturalLanguageGeneration(game_memory=self.game_memory, target_memory=self.target_memory)
        self.printer = PrintModule()

        # Execute the following only if the game is conncted
        if self.game_connection:
            self.game_updates = GameUpdates(game_id)
            self.dm.set_game_link(self.game_updates)

    def setup(self):
        # connect the modules so they can listen to the IUs from the other modules
        # self.microphone_input.subscribe(self.asr)
        # self.asr.subscribe(self.nlu)
        self.chatin.subscribe(self.segmenter)
        self.segmenter.subscribe(self.nlu)
        self.nlu.subscribe(self.dm)
        self.dm.subscribe(self.nlg)
        self.nlg.subscribe(self.printer)

        # Execute the following only if the game is conncted
        if self.game_connection:
            self.game_updates.subscribe(self.dm)

    def start_agent(self):
        # self.microphone_input.run()
        # self.asr.run()
        self.chatin.run()
        self.segmenter.run()
        self.nlu.run()
        self.dm.run()
        self.nlg.run()
        self.printer.run()

        #Execute the following only if the game is conncted
        if self.game_connection:
            self.game_updates.run()

    def stop_agent(self):
        # self.microphone_input.stop()
        # self.asr.stop()
        self.chatin.stop()
        self.segmenter.stop()
        self.nlu.stop()
        self.dm.stop()
        self.nlg.stop()
        self.printer.stop()

        #Execute the following only if the game is conncted
        if self.game_connection:
            self.game_updates.stop()
