# ai-voice-assistant

build an AI voice assistant with Python. This assistant will have aging capabilities, meaning it will be able to interact with a database, call Python functions, and essentially do anything you want.

- Also integrate with own custom frontend to see how to interact with this in real world

## project demo

- car call center - to schedule a service appointment or an oil change ..etc ... we need to provide VIN details ..etc when we call to this support guy/girl.
- we will be `automating` this using an ai-voice-assistant , where an ai-agent with communicate with you and takes in details of your need and about you if it doesn't have and interact with tools it's been provided and serves as per your request.
- firstly we will build an agent and then we integrate it with frontend.
- also the framework we will be using `Livekit` - which is used by ton of companies including openAI - as this is best in business when it comes to doing ultra low latency transportation of voice. video, audio, data ..etc. to build realtime AI systems.
- make a new account on [liveKit](https://livekit.io/) to get started & it asks you to create an app/project as well mine is `abhi-car-service-center`
- do create a `.env`` file and include the neccessary keys needed to start working on this project. in Livekit go to settings and keys and create key - give it a name (windows_machine) and it gives you - API key , WebSocket URL & SECRET KEY & copy them into .env file. Also the OPENAI API KEY from [OpenAI](https://platform.openai.com/api-keys)
- Also understand livekit architecture before we get started to have an idea of how it's going to work from it's [documentation](https://docs.livekit.io/agents/overview/)
  - `TODO`: understand what's `WebRTC` which is between our clients & livekitCloud & our Backend(Agent) & `WebSocket`.
  - `we will be using REALTIME API (OPEN AI) which allows us to have extremely low latency in the responses.`

### python backend setup

- create a `requirements.txt` file to install the neccessary dependencies by including the libraries we need in there.
- create a virtual environment and then we install those dependencies in requirements.txt file.(recommended)
  - `python -m venv ai`
  - Activate the venv - `source ai/Scripts/activate`
  - Then install the dependencies - `pip install -r ./requirements.txt`
- uvicorn - to run our flask server in this project.
- later we will try to do the same using `FASTAPI` - `TODO`

### Building the voice assistant agent

- let's create some files:
  - `agent.py` - Entry point script
  - `api.py` - specify some of the tools that our agent will be able to use.
  - `db_driver.py` - which will handle managing our database & connecting to that for things like our vehicle information
  - `prompts.py` - which will have prompts that we'll use for our AI agents to operate as we desire.
  - In VS Code, you can check/set the Python interpreter:Press Ctrl+Shift+P (Windows)
  - to run : we do -> `python .\agent.py dev` is how you run this in development mode
  - since we don't have frontend now and to test this livekit provides this [playground](https://agents-playground.livekit.io/) - we can see voice output and our inputs and response from the assistant in the playground once the dev mode started. - cool

### Adding Agent tools & database

- let's start providing tools that agent can use.
- we want to save VIN's or lookup VINs or create a new profile.
- connect the db_driver to api

### designing the agent decision tree

- until above we were able to add tools for the llm to call based on user request but it's doesn't know how to handle or make a decision like if there's no profile it needs to ask us to provide details and if there's one it should go for what it needs to do for us.

### Frontend Integration

- we use `vite` to create our frontend `react` as follows:
  - npm create vite@latest frontend -- --template react
  - refer this docs from [livekit](https://docs.livekit.io/agents/openai/client-apps/) integrating with frontend [react](https://docs.livekit.io/home/quickstarts/react/)
  - then `cd frontend`
  - Do `npm install`
  - then run this npm command as per reference doc `npm install @livekit/components-react @livekit/components-styles livekit-client --save`
  - we will also get rid of public and assets folders
  - copied css styles of app , index , SimpleVoiceAssistant from [twtgithubrepo](https://github.com/techwithtim/LiveKit-AI-Car-Call-Centre/tree/main/frontend/src)
  - to run locally - `npm run dev`
- Now we make new environment file to connect to the liveKitRoom & we need a token as well

### LiveKit Token Authentication & Issuing

we need to write our own server & issue the tokens to our frontend , it gives us more control over the tokens and allowing people to join different rooms , we will do that from our backend.

- if we send a request to getToken , it will generate a random room name for us unless we specify & it will allow us to connect from our frontend

- from frontend let's setup api proxy
- using fastapi - to run the server.py - `uvicorn server:app --host 0.0.0.0 --port 5001 --reload`
