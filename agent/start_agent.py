from agent.dialogue_system import Agent

GAME_ID = 3
GAME_CONNECTION = False

nellie = Agent(GAME_ID, GAME_CONNECTION)
nellie.setup()
nellie.start_agent()