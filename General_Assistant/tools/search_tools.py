"""
這段代碼定義了一個名為 SearchTools 的 Python 類別，其中包含兩個用於進行網路搜尋的方法：search_internet 和 search_news。這些方法通過一個外部 API 實現對互聯網和新聞的搜索。以下是對代碼的逐行解釋：

共通部分：

import json - 引入 Python 的 json 模組，用於處理 JSON 格式的數據。
import os - 引入 os 模組，用於訪問操作系統的功能，例如環境變量。
import requests - 引入 requests 模組，用於發送 HTTP 請求。
from langchain.tools import tool - 從 langchain.tools 模組中引入 tool 裝飾器，用於定義工具方法。
search_internet 方法：

使用 @tool("Search the internet") 裝飾器。
方法接受一個參數 query，表示要搜索的查詢內容。
定義要返回的最高結果數量。
設定 API URL 為 Google SERPer（一種搜索引擎結果頁面解析服務）的搜索接口。
創建一個 payload 包含搜索查詢，並轉換為 JSON 格式。
設定 HTTP 請求頭，包括 API 密鑰和內容類型。
使用 requests 發送 POST 請求並接收響應。
從響應中提取有關搜索結果的數據。
遍歷並處理最多四個搜索結果，格式化為包含標題、鏈接和摘要的字符串。
返回格式化的搜索結果。
search_news 方法：

與 search_internet 方法類似，但專注於搜索新聞。
方法使用不同的 API URL (https://google.serper.dev/news) 進行新聞搜索。
其他操作與
search_internet 方法類似，包括創建 payload、發送請求、處理響應、格式化結果。

總結：

這兩個方法都使用了第三方 API（SERPer API），透過 Google 搜索引擎進行網絡和新聞的搜索。
方法中的錯誤處理（例如 try-except 塊和 next）用於處理潛在的鍵值缺失情況。
返回的結果包括搜索到的項目的標題、鏈接和摘要，格式化為易於閱讀的字符串。
這些工具類別的方法可以在需要自動化搜索互聯網或新聞資訊的應用場景中使用。
整體而言，這段代碼展示了如何利用外部 API 和 Python 編程來實現自動化的網絡搜尋功能，對於需要快速獲取和整理網上資訊的場景特別有用。
"""
import json
import os

import requests
from langchain.tools import tool

class SearchTools():
  @tool("Search the internet")
  def search_internet(query):
    """Useful to search the internet 
    about a a given topic and return relevant results"""
    top_result_to_return = 4
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['organic']
    string = []
    for result in results[:top_result_to_return]:
      try:
        string.append('\n'.join([
            f"Title: {result['title']}", f"Link: {result['link']}",
            f"Snippet: {result['snippet']}", "\n-----------------"
        ]))
      except KeyError:
        next

    return '\n'.join(string)

  @tool("Search news on the internet")
  def search_news(query):
    """Useful to search news about a company, stock or any other
    topic and return relevant results"""""
    top_result_to_return = 4
    url = "https://google.serper.dev/news"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()['news']
    string = []
    for result in results[:top_result_to_return]:
      try:
        string.append('\n'.join([
            f"Title: {result['title']}", f"Link: {result['link']}",
            f"Snippet: {result['snippet']}", "\n-----------------"
        ]))
      except KeyError:
        next

    return '\n'.join(string)
