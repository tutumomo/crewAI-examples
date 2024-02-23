"""
find_papers_arxiv：
這段代碼的目的是使用arXiv API從arXiv學術文獻數據庫中搜索相關論文，並將搜索結果保存到本地緩存中，以便日後快速訪問。以下是代碼的逐步解釋：
導入所需模塊：
os：用於操作系統相關功能，例如創建目錄。
re：正則表達式模塊，用於處理字符串。
json：處理JSON格式數據。
hashlib：提供數據加密功能，這裡用於生成唯一的緩存鍵。
arxiv：arXiv API 的一個接口，用於搜索arXiv數據庫。
定義 search_arxiv 函數：
query：搜索查詢字符串。
max_results：最多返回的結果數量，預設為10。
生成緩存鍵：使用MD5對搜索查詢進行加密，以創建獨特的緩存文件名。
創建緩存目錄：如果 .cache 目錄不存在，則創建它。
檢查緩存：如果對應緩存文件存在，則從緩存讀取數據並返回。
處理搜索查詢：
使用正則表達式移除查詢中的特殊字符和操作符（如“and”, “or”, “not”）。
將查詢轉換為小寫並去除多餘空格。
執行搜索：使用arXiv模塊執行實際的搜索。
處理搜索結果：
將每篇論文的資訊（如標題、作者、摘要等）整理為字典格式。
將這些字典添加到結果列表中。
限制結果數量：如果結果數量超過 max_results，則截斷列表。
保存結果到緩存：將搜索結果以JSON格式保存到緩存文件中。
返回結果：返回處理後的搜索結果列表。
整體而言，這個函數提供了從arXiv檢索學術文獻並將結果緩存到本地的功能，這可以提高重複查詢的效率。
=====================================================
find_papers_arxiv 原本是 autogen stuido 範例的 skills(Tools)，
在 autogen stuido 未使用 class 定義類別，只使用函式定義來當成工具
但 crewai 無法調用，所以還是改成"類別+函式"
經測試正常，可以使用。

autogen studio 的 skill 轉換成 crewai 的 tools 庫工具做法：
1.放在專案資料夾的 tools 子資料夾內
2.改成類別2行
3.檔案名、類別名、函式名 皆不同(如果都相同可以嗎?待確認)

crewai 的 tools 庫工具改成 autogen studio 的 skill 做法
1.取消類別，改為函式(如果維持類別的定義，可以嗎?待確認)
"""
import os
import re
import json
import hashlib
import arxiv
from langchain.tools import tool

class FindPapersArxiv():
    @tool("Searches arXiv for the given query") 
    def search_arxiv(query, max_results=10):
        """
        Searches arXiv for the given query using the arXiv API, then returns the search results.
        Args:
            query (str): The search query.
            max_results (int, optional): The maximum number of search results to return. Defaults to 10.
        Returns:
            jresults (list): A list of dictionaries. Each dictionary contains fields such as 'title', 'authors', 'summary', and 'pdf_url'
        Example:
            >>> results = FindPapersArxiv.search_arxiv("attention is all you need")
            >>> print(results)
        """
        key = hashlib.md5(("search_arxiv(" + str(max_results) + ")" + query).encode("utf-8")).hexdigest()
        cache_dir = ".cache"
        if not os.path.isdir(cache_dir):
            os.mkdir(cache_dir)

        fname = os.path.join(cache_dir, key + ".cache")

        # Check cache
        if os.path.isfile(fname):
            with open(fname, "r", encoding="utf-8") as fh:
                return json.load(fh)

        # Normalize the query
        query = re.sub(r"[^\s\w]", " ", query.lower())
        query = re.sub(r"\s(and|or|not)\s", " ", " " + query + " ")
        query = re.sub(r"[^\s\w]", " ", query.lower())
        query = re.sub(r"\s+", " ", query).strip()

        # Search arXiv
        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)

        jresults = []
        for result in search.results():
            r = {
                "entry_id": result.entry_id,
                "updated": str(result.updated),
                "published": str(result.published),
                "title": result.title,
                "authors": [str(a) for a in result.authors],
                "summary": result.summary,
                "comment": result.comment,
                "journal_ref": result.journal_ref,
                "doi": result.doi,
                "primary_category": result.primary_category,
                "categories": result.categories,
                "links": [str(link) for link in result.links],
                "pdf_url": result.pdf_url
            }
            jresults.append(r)

        # Save to cache
        with open(fname, "w") as fh:
            json.dump(jresults, fh)

        return jresults

# Example usage
# results = FindPapersArxiv.search_arxiv("attention is all you need")
# print(results)

