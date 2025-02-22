# AshishCustomTripPlanner Crew

Welcome to the AshishCustomTripPlanner Crew project, powered by [crewAI](https://crewai.com). 
<br>I have taken the [Surpise Trip](https://github.com/crewAIInc/crewAI-examples/tree/main/surprise_trip) project from [CrewAI Examples](https://github.com/crewAIInc/crewAI-examples.git). 

I have modified this project to use Deepseek LLM using - <br>
   1) Deepseek API from Deepseek
   2) Deepseek NIM API from nvidia.

Rest of exammple is same as the origial suprise trip. 

Also I have used the Serper API for google search.

To run this project you will need -
   1) Serper API
   2) Deepseek API
   3) NIM Deepseek API.
   4) Optionally OpenRouter Deepseek API if you like to use.
      
In case you want to use only one LLM, then you can use either of it. I have used OpenRouter LLM as an optional. You may skip it. 

## Installation

You can use installation instruction on the [CrewAI Installation](https://docs.crewai.com/installation) webpage. 

I have used conda based environment to run crewAI. The detail instructions are given on my blog for your reference. 

### Customizing

**Configure Environment**: Edit `.env.example`  and rename file to `.env` and update below environment variables by providing API keys.

- SERPER_API_KEY=
- DEEPSEEK_API_KEY=
- NIM_DEEPSEEK_API_KEY=
- OPENROUTER_DEEPSEEK_API_KEY=

**Configure Agents and Taks**:
- Modify `src/ashish_custom_trip_planner/config/agents.yaml` to define your agents
- Modify `src/ashish_custom_trip_planner/config/tasks.yaml` to define your tasks
- Modify `src/ashish_custom_trip_planner/crew.py` to add your own logic, tools and specific args
- Modify `src/ashish_custom_trip_planner/main.py` to add custom inputs for your agents and tasks
- Check `src/ashish_custom_trip_planner/config/agents.yaml` to update your agents and `src/ashish_custom_trip_planner/config/tasks.yaml` to update your tasks.

## Understanding Your Crew

The ashish-custom-trip-planner Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the ashish-custom-trip-planner Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Output
A successful output from one of sucessful runs is shown in "Output-Run-1.txt" file in root folder. 

## Support

For support, questions, or feedback regarding the AshishCustomTripPlanner Crew or crewAI.
- Visit CrewAI  [documentation](https://docs.crewai.com)
- Reach out to CrewAI through  [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join CrewAI Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with CrewAI docs](https://chatg.pt/DWjSBZn)

## License
This project is released under the MIT License.
