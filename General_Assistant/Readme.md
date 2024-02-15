# 利用 crewai 提供的範例，建立一個可調用 Tools 的通用 Assistant

不確定能否成功，先試試。

## 修改的部分：

- 改成可調用 gpt3.5、gpt4、Ollama、Gemini Pro 這4種大模型
- agent：agent 名稱不改，僅修改 role、backstory、goal 為通用助手的內容(參考 autogen)，tools加入目前所有的 tools，
