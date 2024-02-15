"""
這段代碼看起來是Python程式碼，它似乎定義了一個名為CalculatorTools的類別，該類別具有一個裝飾器（@tool("Make a calculation")）和一個名為calculate的方法。
讓我們一步步解釋這段代碼：
from langchain.tools import tool: 這個語句導入了一個叫做tool的模組或函式，它似乎是用來定義一些工具或功能的。
class CalculatorTools(): 這行代碼定義了一個名為CalculatorTools的Python類別。
@tool("Make a calculation"): 這是一個裝飾器，它將下一個方法calculate標記為一個工具，並提供了一個描述，即"Make a calculation"。這個裝飾器的作用可能是將calculate方法註冊為一個可用的工具，以便在其他地方使用。
def calculate(operation): 這是一個方法定義，它接受一個名為operation的參數。根據註釋，這個方法用於執行數學計算，例如加法、減法、乘法、除法等。它使用Python的eval函式來評估傳遞給它的operation，這個operation應該是一個數學表達式，例如200*7或5000/2*10。評估結果將被返回。
總結來說，這個程式碼看起來是定義了一個名為CalculatorTools的類別，該類別具有一個用於執行數學計算的工具方法calculate，這個工具方法可以接受一個數學表達式並返回計算結果。該代碼還使用了tool裝飾器，可能是將calculate方法註冊為一個可用的工具，以便在其他地方使用。
"""
from langchain.tools import tool

class CalculatorTools():

  @tool("Make a calcualtion")
  def calculate(operation):
    """Useful to perform any mathematical calculations, 
    like sum, minus, multiplication, division, etc.
    The input to this tool should be a mathematical 
    expression, a couple examples are `200*7` or `5000/2*10`
    """
    return eval(operation)
