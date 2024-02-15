"""
測試建立一個說笑話的工具，摸索 tools 工具中。
以為很簡單，結果連要 return 甚麼都不知道，暈倒
因為沒有呼叫跟運算，沒東西要怎麼 return ?
還是要參考 search_tools.py，直接定義一個說笑話的 Agent?

"""
from langchain.tools import tool
from crewai import Agent, Task

class JokeTools():  # class 類別的()裡面是空的

  @tool("Say a funny joke in traditional chinese")
  def say_joke(query):
    """You are a joke teller who is very familiar with traditional Chinese characters and very humorous. 
       You often tell jokes that make people laugh.
    """
    agent = Agent(
        role='joke teller',
        goal=
        'make people laugh',
        backstory=
        "You are a joke teller who is very familiar with traditional Chinese characters and very humorous.",
        allow_delegation=False
    )
    task = Task(
        agent=agent,
        description=
        f'Say a funny joke in traditional chinese'
    )
    joke = task.execute()
    if joke == None:
      return "I'm sorry, I don't know how to tell a joke in traditional Chinese."
    else:
      return joke
