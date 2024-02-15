"""
這裡要仿照 crewAI-examples 提供範例的做法。
agents、tasks 都寫成外部的檔案，並從這裡讀取。
tools 則放在資料夾中，從這裡讀取。


"""
# 載入 crewai 的模組
from crewai import Agent, Crew, Task

from tasks import MarketingAnalysisTasks
from agents import MarketingAnalysisAgents