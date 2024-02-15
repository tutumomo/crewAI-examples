import os
from crewai import Agent
# from langchain.llms import OpenAI
# from langchain.llms import Ollama
from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools

ollama_llm = Ollama(model="mistral") 

Gemini_llm = ChatGoogleGenerativeAI(
    model = "gemini-pro",
    verbose = True,
    temperature = 0.6,
    google_api_key = os.environ["GOOGLE_API_KEY"]
    )

class TripAgents():

  def city_selection_agent(self):
    return Agent(
        role='City Selection Expert',
        goal='Select the best city based on weather, season, and prices. Using traditional chinese to express.',
        backstory=
        'An expert in analyzing travel data to pick ideal destinations',
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
        ],
        # llm = ollama_llm,
        llm = Gemini_llm,
        verbose=True)

  def local_expert(self):
    return Agent(
        role='Local Expert at this city',
        goal='Provide the BEST insights about the selected city. Using traditional chinese to express.',
        backstory="""A knowledgeable local guide with extensive information
        about the city, it's attractions and customs""",
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
        ],
        # llm = ollama_llm,
        llm = Gemini_llm,
        verbose=True)

  def travel_concierge(self):
    return Agent(
        role='Amazing Travel Concierge',
        goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city. Using traditional chinese to express.""",
        backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
        tools=[
            SearchTools.search_internet,
            BrowserTools.scrape_and_summarize_website,
            CalculatorTools.calculate,
        ],
        # llm = ollama_llm,
        llm = Gemini_llm,
        verbose=True)
