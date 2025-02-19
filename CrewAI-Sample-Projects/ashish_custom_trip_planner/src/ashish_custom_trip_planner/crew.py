from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from surprise_travel.tools.custom_tool import MyCustomTool

# Check our tools documentation for more information on how to use them
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Activity(BaseModel):
    name: str = Field(..., description="Name of the activity")
    location: str = Field(..., description="Location of the activity")
    description: str = Field(..., description="Description of the activity")
    date: str = Field(..., description="Date of the activity")
    cousine: str = Field(..., description="Cousine of the restaurant")
    why_its_suitable: str = Field(..., description="Why it's suitable for the traveler")
    reviews: Optional[List[str]] = Field(..., description="List of reviews")
    rating: Optional[float] = Field(..., description="Rating of the activity")

class DayPlan(BaseModel):
	date: str = Field(..., description="Date of the day")
	activities: List[Activity] = Field(..., description="List of activities")
	restaurants: List[str] = Field(..., description="List of restaurants")
	flight: Optional[str] = Field(None, description="Flight information")

class Itinerary(BaseModel):
	name: str = Field(..., description="Name of the itinerary, something funny")
	day_plans: List[DayPlan] = Field(..., description="List of day plans")
	hotel: str = Field(..., description="Hotel information")

@CrewBase
class AshishCustomTripPlanner():
	"""AshishCustomTripPlanner crew"""

	# print(os.getenv("DEEPSEEK_API_KEY"))
	# print(os.getenv("NIM_DEEPSEEK_API_KEY"))
	# print(os.getenv("OPENROUTER_DEEPSEEK_API_KEY"))
	# Setup Deepseek environemnet 
	deepseek_llm = LLM(
				model="deepseek/deepseek-chat",
				# api_key="DEEPSEEK_API_KEY",
				api_key=os.getenv("DEEPSEEK_API_KEY"),
				base_url="https://api.deepseek.com",
		#        temperature=1.0,
	)
	nvdia_deepseek_llm = LLM (
				# model="nvidia_nim/meta/llama3-70b-instruct",
				model="deepseek-ai/deepseek-r1",
				temperature=0.7,
				base_url = "https://integrate.api.nvidia.com/v1",
				api_key = os.getenv("NIM_DEEPSEEK_API_KEY")
	)

	openrouter_deepseek_llm = LLM (
				# model="nvidia_nim/meta/llama3-70b-instruct",
				model="deepseek/deepseek-r1:free",
				temperature=0.7,
				base_url="https://openrouter.ai/api/v1",
				api_key=os.getenv("OPENROUTER_DEEPSEEK_API_KEY"),
	) 


	deepseek_llm_reasoner = LLM(
				model="deepseek/deepseek-reasoner",
				# api_key="DEEPSEEK_API_KEY",
				api_key=os.getenv("DEEPSEEK_API_KEY"),
				base_url="https://api.deepseek.com",
		#        temperature=1.0,
	)
	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'


	# we are going to create three agents 
	#1) personalized_activity_planner agentt which will based on the date and desttination create a high level activities plan
	#2) restaurant_scout agent - which based on the location and activities will create list of restaurants 
	#3) itinerary_compiler agent - which will provvide the final internary fror given number of days 

	@agent
	def personalized_activity_planner(self) -> Agent:
		return Agent(
			config=self.agents_config['personalized_activity_planner'],
			tools=[SerperDevTool(), ScrapeWebsiteTool()], # Example of custom tool, loaded at the beginning of file
			verbose=True,
			allow_delegation=False,
			llm=self.nvdia_deepseek_llm,
		)

	@agent
	def restaurant_scout(self) -> Agent:
		return Agent(
			config=self.agents_config['restaurant_scout'],
			tools=[SerperDevTool(), ScrapeWebsiteTool()],
			verbose=True,
			allow_delegation=False,
			llm=self.nvdia_deepseek_llm,
		)

	@agent
	def itinerary_compiler(self) -> Agent:
		return Agent(
			config=self.agents_config['itinerary_compiler'],
			tools=[SerperDevTool()],
			verbose=True,
			allow_delegation=False,
			llm=self.deepseek_llm,
		)


	# Similar to agents, we are going to create task for each agent.
	# 
	@task
	def personalized_activity_planning_task(self) -> Task:
		return Task(
			config=self.tasks_config['personalized_activity_planning_task'],
			agent=self.personalized_activity_planner()
		)

	@task
	def restaurant_scenic_location_scout_task(self) -> Task:
		return Task(
			config=self.tasks_config['restaurant_scenic_location_scout_task'],
			agent=self.restaurant_scout()
		)

	@task
	def itinerary_compilation_task(self) -> Task:
		return Task(
			config=self.tasks_config['itinerary_compilation_task'],
			agent=self.itinerary_compiler(),
			output_json=Itinerary
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AshishCustomTripPlanner crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # manager_llm=self.deepseek_llm,
            # function_calling_llm=self.deepseek_llm,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
