# define our tools we will provide to model

from livekit.agents import llm


class AssistantFunc(llm.FunctionContext):
    """sample func"""

    def __init__(self):
        super().__init__()
