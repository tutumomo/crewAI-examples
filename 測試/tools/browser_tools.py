"""
這個 tools 不單單是定義了 tools，是在 tools 裡面就定義了 agent、task，並執行了 task.excute()。
這段代碼定義了一個名為 BrowserTools 的 Python 類別，其中包含一個方法 scrape_and_summarize_website，用於從網站抓取內容並進行摘要。以下是對代碼的逐行解釋：

import json - 引入 Python 的 json 模組，用於處理 JSON 格式的數據。
import os - 引入 os 模組，用於訪問操作系統功能，比如環境變量。
import requests - 引入 requests 模組，用於發送 HTTP 請求。
from crewai import Agent, Task - 從 crewai 模組中引入 Agent 和 Task 類別，這些可能是用於處理自動化任務或人工智能相關功能的類別。
from langchain.tools import tool - 從 langchain.tools 模組中引入 tool 裝飾器，用於定義工具方法。
from unstructured.partition.html import partition_html - 引入用於處理 HTML 內容的 partition_html 函數。
BrowserTools 類別定義了 scrape_and_summarize_website 方法：

使用 @tool("Scrape website content") 裝飾器。
方法接受一個參數 website，表示要抓取內容的網站 URL。
構建一個用於向 browserless API 發送請求的 URL，其中包含從環境變量獲取的 API 密鑰。
創建一個 payload，其中包含要抓取的網站 URL，並將其轉換為 JSON 格式。
設定 HTTP 請求頭。
使用 requests 發送 POST 請求到 browserless API，獲取網站的 HTML 內容。
使用 partition_html 函數處理獲取的 HTML 文本，將其分割為多個元素。
進行文本處理，將元素轉換為字符串並分割成大小為 8000 字符的塊。
對每個文本塊進行摘要處理：
創建一個 Agent 並設置其角色、目標和背景故事。
創建一個 Task，
其中包括 Agent 和對文本塊進行摘要的描述。

執行 Task 來產生摘要。

將所有摘要收集到一個列表中。

最後，將所有摘要連接成一個字符串並返回。

這個方法的主要功能是使用 browserless API 從給定的網站抓取 HTML 內容，然後將這些內容分割、處理並通過 AI 代理（如 Agent 和 Task）生成摘要。這個過程可能用於自動化地從網站收集並簡化信息，特別是在需要快速獲得網站主要內容摘要的情況下。整個過程都以程式化的方式進行，顯示了現代技術在資訊處理和自動化方面的應用。
"""
import json
import os

import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html

class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(website):
    """Useful to scrape and summarize a website content"""
    url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
    payload = json.dumps({"url": website})
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    elements = partition_html(text=response.text)
    content = "\n\n".join([str(el) for el in elements])
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    summaries = []
    for chunk in content:
      agent = Agent(
          role='Principal Researcher',
          goal=
          'Do amazing research and summaries based on the content you are working with',
          backstory=
          "You're a Principal Researcher at a big company and you need to do research about a given topic.",
          allow_delegation=False)
      task = Task(
          agent=agent,
          description=
          f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
      )
      summary = task.execute()
      summaries.append(summary)
    return "\n\n".join(summaries)
