class GameMemory:
    """
    The Game Memory holds all the information that need to be stored over the course of one game. These are both
    related to the information from the game interface (i.e., game time and score) as well as information related
    to the interaction.
    TODO: Think about whether this needs to be made thread-safe since it is accessed in multiple threads
    """

    def __init__(self):
        self.remaining_game_time = -1
        self.current_score = 0
        self.point_array = []
        self.game_state = "Init"
        self.total_guesses = 0
        self.total_human_turns = 0
        self.total_agent_turns = 0

    def set_remaining_game_time(self, time):
        self.remaining_game_time = time

    def get_remaining_game_time(self):
        return self.remaining_game_time

    def set_current_score(self, score):
        self.current_score = score

    def get_current_score(self):
        return self.current_score

    def set_point_array(self, point_array):
        self.point_array = point_array

    def get_point_array(self):
        return self.point_array

    def set_game_state(self, game_state):
        self.game_state = game_state

    def get_game_state(self):
        return self.game_state

    def increment_total_guesses(self):
        self.total_guesses += 1

    def get_total_guesses(self):
        return self.total_guesses

    def increment_total_human_turns(self):
        self.total_human_turns += 1

    def get_total_human_turs(self):
        return self.total_human_turns

    def increment_total_agent_turns(self):
        self.total_agent_turns += 1

    def get_total_agent_turs(self):
        return self.total_agent_turns

    def get_total_turn(self):
        return self.total_agent_turns + self.total_human_turns


class TargetMemory:
    """
    The Target Memory holds all the information that are related to the current target. It is wiped whenever
    a new target comes in.
    TODO: Think about whether this needs to be made thread-safe since it is accessed in multiple threads
    """

    def __init__(self):
        self.time_spent = 0
        self.human_turns = 0
        self.agent_turns = 0

    def set_time_spent(self, time):
        self.time_spent = time

    def get_time_spent(self):
        return self.time_spent

    def increment_human_turns(self):
        self.human_turns += 1

    def get_human_turns(self):
        return self.human_turns

    def increment_agent_turns(self):
        self.agent_turns += 1

    def get_agent_turns(self):
        return self.agent_turns

    def get_total_turns(self):
        return self.agent_turns + self.human_turns

    def wipe_memory(self):
        self.time_spent = 0
        self.human_turns = 0
        self.agent_turns = 0
