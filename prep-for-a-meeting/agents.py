from textwrap import dedent
from crewai import Agent

# 設定4個 LLM
# crewai 使用 Ollama 的方法：windows 只需要打開 ubuntu 視窗即可，不需要執行 litellm；Mac 則甚至不需要啟動任何程式，只要有安裝好 Ollama 即可調用。
# 與 autogen 不同，autogen 要調用 Ollama 需要執行 litellm，多一道步驟，比較麻煩
gpt35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
gpt4 = ChatOpenAI(model_name="gpt-4", temperature=0.7),
ollama = Ollama(model="openhermes_assistant")  # 這是用 modelfile 建立的
gemini = ChatGoogleGenerativeAI(model="gemini-pro",
                             verbose = True,
                             temperature = 0.6,
                             google_api_key = os.environ["GOOGLE_API_KEY"]
                             )

from tools.ExaSearchTool import ExaSearchTool

class MeetingPreparationAgents():
	def research_agent(self):
		return Agent(
			role='Research Specialist',
			goal='Conduct thorough research on people and companies involved in the meeting',
			tools=ExaSearchTool.tools(),
			backstory=dedent("""\
					As a Research Specialist, your mission is to uncover detailed information
					about the individuals and entities participating in the meeting. Your insights
					will lay the groundwork for strategic meeting preparation."""),
			verbose=True
		)

	def industry_analysis_agent(self):
		return Agent(
			role='Industry Analyst',
			goal='Analyze the current industry trends, challenges, and opportunities',
			tools=ExaSearchTool.tools(),
			backstory=dedent("""\
					As an Industry Analyst, your analysis will identify key trends,
					challenges facing the industry, and potential opportunities that
					could be leveraged during the meeting for strategic advantage."""),
			verbose=True
		)

	def meeting_strategy_agent(self):
		return Agent(
			role='Meeting Strategy Advisor',
			goal='Develop talking points, questions, and strategic angles for the meeting',
			tools=ExaSearchTool.tools(),
			backstory=dedent("""\
					As a Strategy Advisor, your expertise will guide the development of
					talking points, insightful questions, and strategic angles
					to ensure the meeting's objectives are achieved."""),
			verbose=True
		)

	def summary_and_briefing_agent(self):
		return Agent(
			role='Briefing Coordinator',
			goal='Compile all gathered information into a concise, informative briefing document',
			tools=ExaSearchTool.tools(),
			backstory=dedent("""\
					As the Briefing Coordinator, your role is to consolidate the research,
					analysis, and strategic insights."""),
			verbose=True
		)
