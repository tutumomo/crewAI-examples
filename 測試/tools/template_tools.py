"""
這段代碼定義了一個名為 TemplateTools 的 Python 類別，其中包含兩個方法，用於處理與學習管理系統相關的網頁模板。以下是對代碼的逐行解釋：

import json - 引入 Python 的 json 模組，用於處理 JSON 格式的數據。
import shutil - 引入 shutil 模組，提供了一系列文件和文件夾操作功能。
from pathlib import Path - 從 pathlib 模組中引入 Path 類別，用於輕鬆處理文件路徑。
from langchain.tools import tool - 從 langchain.tools 模組中引入 tool 裝飾器，用於定義工具方法。
TemplateTools 類別定義了兩個方法：

learn_landing_page_options(input):

使用 @tool("Learn landing page options") 裝飾器，這可能是為了在某個框架或應用程式中註冊這個工具方法。
該方法加載一個 JSON 文件（config/templates.json），這個文件可能包含不同的網頁模板選項。
它返回這些模板選項的 JSON 字符串表示。
copy_landing_page_template_to_project_folder(landing_page_template):

使用 @tool("Copy landing page template to project folder") 裝飾器。
此方法接受一個參數 landing_page_template，表示要使用的模板名稱。
它計算源文件夾和目標文件夾的路徑（基於提供的模板名稱）。
使用 shutil.copytree 函數將模板從源路徑複製到目標路徑。
方法返回一條消息，說明模板已被複製並且可以開始進行修改。
總的來說，這段代碼提供了一個工具類別，用於從配置文件中學習可用的網頁模板選項，

以及將選定的模板複製到項目文件夾以供進一步修改。這對於需要快速設置和自定義網頁模板的開發者來說可能非常有用。
"""
import json
import shutil
from pathlib import Path

from langchain.tools import tool

class TemplateTools():

  @tool("Learn landing page options")
  def learn_landing_page_options(input):
    """Learn the templates at your disposal"""
    templates = json.load(open("config/templates.json"))
    return json.dumps(templates, indent=2)

  @tool("Copy landing page template to project folder")
  def copy_landing_page_template_to_project_folder(landing_page_template):
    """Copy a landing page template to your project 
    folder so you can start modifying it, it expects 
    a landing page template folder as input"""
    source_path = Path(f"templates/{landing_page_template}")
    destination_path = Path(f"workdir/{landing_page_template}")
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_path, destination_path)
    return f"Template copied to {landing_page_template} and ready to be modified, main files should be under ./{landing_page_template}/src/components, you should focus on those."
