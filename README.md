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
