# creating the AI agent (The voice assistant) which will connect to LiveKit
from __future__ import annotations
import os
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai
from dotenv import load_dotenv
from api import AssistantFunc
from prompts import INSTRUCTIONS, WELCOME_MESSAGE, LOOKUP_VIN_MESSAGE


# to access various keys that we need from .env file.
load_dotenv()


# define async function and call that entry point and takes in context
async def entrypoint(ctx: JobContext):
    # connect to livekit
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()

    # define the model we want to use
    model = openai.realtime.RealtimeModel(
        instructions=INSTRUCTIONS,  # what we want to act as(system promt like)
        voice="shimmer",
        temperature=0.8,
        modalities=["audio", "text"],  # what type of medium we want to work with
    )

    assistant_fnc = AssistantFunc()
    assistant = MultimodalAgent(model=model, fnc_ctx=assistant_fnc)
    # assistant will join the room
    await assistant.start(ctx.room)
    # The Room object is the main interface that the worker should interact with.
    # When the entrypoint is called, the worker has not connected to the Room yet. Certain properties of Room would not be available before calling JobContext.connect()
    # tell the ai assistant to do something - to talk to the user or greet them
    session = model.sessions[0]  # grab the first session we have
    # make a new conversation item(adding a new chat message into kind of the context or the current session)
    session.conversation.item.create(
        llm.ChatMessage(role="assistant", content=WELCOME_MESSAGE)
    )
    # tell the assistant to do is respond to that message.
    session.response.create()  # it will read the above conversation and respond to it(speak out to us)

    @session.on("user_speech_committed")
    def on_user_speech_committed(msg: llm.ChatMessage):
        if isinstance(msg.content, list):
            # sometimes msgs comes in as a list so we join them as below
            msg.content = "\n".join(
                "[image]" if isinstance(x, llm.ChatImage) else x for x in msg
            )

        if assistant_fnc.has_car():  # check if we have a car
            handle_query(msg)
        else:
            find_profile(msg)

    def find_profile(msg: llm.ChatMessage):
        session.conversation.item.create(
            llm.ChatMessage(role="system", content=LOOKUP_VIN_MESSAGE(msg))
        )
        session.response.create()

    def handle_query(msg: llm.ChatMessage):
        session.conversation.item.create(
            llm.ChatMessage(role="user", content=msg.content)
        )
        session.response.create()


# call the entry point
if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint)
    )  # runs the entrypoint function asynchronously for us.
    # and automatically connects to livekit cloud as we provided values in environment variables , which will be looked by livekit in order to make the connection
