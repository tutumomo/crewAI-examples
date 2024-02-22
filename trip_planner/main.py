# 執行過程烙是出現
# Invalid Format: Missing 'Action:' after 'Thought: 的錯誤訊息
# 不確定是因為要求他要用中文回復還是有其他 bug 造成的
# 執行程式：poetry run python main.py
from crewai import Crew
from textwrap import dedent
from trip_agents import TripAgents
from trip_tasks import TripTasks

from dotenv import load_dotenv
load_dotenv()

class TripCrew:

  def __init__(self, origin, cities, date_range, interests):
    self.cities = cities
    self.origin = origin
    self.interests = interests
    self.date_range = date_range

  def run(self):
    agents = TripAgents()
    tasks = TripTasks()

    city_selector_agent = agents.city_selection_agent()
    local_expert_agent = agents.local_expert()
    travel_concierge_agent = agents.travel_concierge()

    identify_task = tasks.identify_task(
      city_selector_agent,
      self.origin,
      self.cities,
      self.interests,
      self.date_range
    )
    gather_task = tasks.gather_task(
      local_expert_agent,
      self.origin,
      self.interests,
      self.date_range
    )
    plan_task = tasks.plan_task(
      travel_concierge_agent, 
      self.origin,
      self.interests,
      self.date_range
    )

    crew = Crew(
      agents=[
        city_selector_agent, local_expert_agent, travel_concierge_agent
      ],
      tasks=[identify_task, gather_task, plan_task],
      verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("## Welcome to Trip Planner Crew 歡迎使用本旅遊助手")
  print('--------------------------------------------------')
  location = input(
    dedent("""
      From where will you be traveling from? 出發地點?
    """))
  cities = input(
    dedent("""
      What are the cities options you are interested in visiting? 預計出遊地點?
    """))
  date_range = input(
    dedent("""
      What is the date range you are interested in traveling? 出遊日期?
    """))
  interests = input(
    dedent("""
      What are some of your high level interests and hobbies? 興趣、愛好?
    """))
  
  trip_crew = TripCrew(location, cities, date_range, interests)
  result = trip_crew.run()
  print("\n\n########################")
  print("## 您的旅遊計畫如下")
  print("########################\n")
  print(result)
