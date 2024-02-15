"""
這段代碼定義了一個名為 SECTools 的 Python 類別，該類別包含了兩個方法用於搜尋和分析美國證券交易委員會（SEC）提交的報告，特別是 10-Q 和 10-K 表格。以下是對代碼的逐行解釋：

通用部分
import os - 引入 os 模組，用於訪問操作系統的功能，例如環境變量。
import requests - 引入 requests 模組，用於發送 HTTP 請求。
from langchain.tools import tool - 從 langchain.tools 模組中引入 tool 裝飾器，用於定義工具方法。
from langchain.text_splitter import CharacterTextSplitter - 引入用於文本分割的工具。
from langchain.embeddings import OpenAIEmbeddings - 引入用於生成文本嵌入的 OpenAI 嵌入模型。
from langchain_community.vectorstores import FAISS - 引
入用于建立向量存储的 FAISS 库，以便进行高效的相似性搜索。
7. from sec_api import QueryApi - 引入用于查询 SEC 数据的 API 模块。

from unstructured.partition.html import partition_html - 引入用于处理 HTML 文档的函数。
search_10q 方法
使用 @tool("Search 10-Q form") 裣饰器。
接收一个由股票代码和查询问题组成的字符串，用管道符（|）分隔。
使用 SEC API（通过环境变量中的 API 密钥）构造查询，以获取指定股票的最新 10-Q 表格。
如果找不到相应的文件，返回一个错误信息。
否则，从返回的文件中提取链接，并使用 __embedding_search 方法来搜索和提取相关的回答。
search_10k 方法
类似于 search_10q，但用于搜索 10-K 表格（年度报告）。
__embedding_search 私有方法
下载并处理指定 URL 的 HTML 内容。
使用 partition_html 函数将 HTML 内容分割成多个元素。
使用 CharacterTextSplitter 将文本划分为更小的部分，以便处理。
使用 OpenAIEmbeddings 生成文本的嵌入表示。
使用 FAISS 库建立向量存储，并通过嵌入相似性搜索相关答案。
返回前四个最相关的文档内容作为答案。
__download_form_html 私有方法
用于从给定的 URL 下载 HTML 内容。
设置 HTTP 请求头以模拟常见的浏览器行为，以确保成功获取页面内容。
总结：

这个类通过 SEC API 搜索特定股票的 10-Q 和 10-K 报告，解析报告内容，并使用文本嵌入和向量相似性搜索来回答关于报告内容的特定问题。
这是一个自动化工具，适用于金融分析师或投资者，用于快速获取和理解公司的财务报告。
"""
import os

import requests

from langchain.tools import tool
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from sec_api import QueryApi
from unstructured.partition.html import partition_html

class SECTools():
  @tool("Search 10-Q form")
  def search_10q(data):
    """
    Useful to search information from the latest 10-Q form for a
    given stock.
    The input to this tool should be a pipe (|) separated text of
    length two, representing the stock ticker you are interested and what
    question you have from it.
		For example, `AAPL|what was last quarter's revenue`.
    """
    stock, ask = data.split("|")
    queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
    query = {
      "query": {
        "query_string": {
          "query": f"ticker:{stock} AND formType:\"10-Q\""
        }
      },
      "from": "0",
      "size": "1",
      "sort": [{ "filedAt": { "order": "desc" }}]
    }

    fillings = queryApi.get_filings(query)['filings']
    if len(fillings) == 0:
      return "Sorry, I couldn't find any filling for this stock, check if the ticker is correct."
    link = fillings[0]['linkToFilingDetails']
    answer = SECTools.__embedding_search(link, ask)
    return answer

  @tool("Search 10-K form")
  def search_10k(data):
    """
    Useful to search information from the latest 10-K form for a
    given stock.
    The input to this tool should be a pipe (|) separated text of
    length two, representing the stock ticker you are interested, what
    question you have from it.
    For example, `AAPL|what was last year's revenue`.
    """
    stock, ask = data.split("|")
    queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
    query = {
      "query": {
        "query_string": {
          "query": f"ticker:{stock} AND formType:\"10-K\""
        }
      },
      "from": "0",
      "size": "1",
      "sort": [{ "filedAt": { "order": "desc" }}]
    }

    fillings = queryApi.get_filings(query)['filings']
    if len(fillings) == 0:
      return "Sorry, I couldn't find any filling for this stock, check if the ticker is correct."
    link = fillings[0]['linkToFilingDetails']
    answer = SECTools.__embedding_search(link, ask)
    return answer

  def __embedding_search(url, ask):
    text = SECTools.__download_form_html(url)
    elements = partition_html(text=text)
    content = "\n".join([str(el) for el in elements])
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap  = 150,
        length_function = len,
        is_separator_regex = False,
    )
    docs = text_splitter.create_documents([content])
    retriever = FAISS.from_documents(
      docs, OpenAIEmbeddings()
    ).as_retriever()
    answers = retriever.get_relevant_documents(ask, top_k=4)
    answers = "\n\n".join([a.page_content for a in answers])
    return answers

  def __download_form_html(url):
    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
      'Cache-Control': 'max-age=0',
      'Dnt': '1',
      'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
      'Sec-Ch-Ua-Mobile': '?0',
      'Sec-Ch-Ua-Platform': '"macOS"',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    return response.text
