from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from mem0.memory.main import Memory
import os

from .base_model import Base_Chat_Langchain_Client, CallbackToIterator

# load_config_to_environ(["azure_openai_api_key", "azure_api_base_url", "azure_openai_api_version", "azure_deployment_name"])

class TestMem0_Client(Base_Chat_Langchain_Client):
    def __init__(self, model_name, user_name=""):
        super().__init__(model_name, user_name)
        self.memory=None

    def setup_model(self):
        # inplement this to setup the model then return it
        return AzureChatOpenAI(
            openai_api_base=os.environ["AZURE_OPENAI_API_BASE_URL"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            deployment_name=os.environ["AZURE_DEPLOYMENT_NAME"],
            openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
            openai_api_type="azure",
            streaming=True
        )
    
    def createMem0(self):
        #llm
        os.environ["LLM_AZURE_OPENAI_API_KEY"] = os.environ["AZURE_OPENAI_API_KEY"]
        os.environ["LLM_AZURE_OPENAI_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"]
        os.environ["LLM_AZURE_OPENAI_API_ENDPOINT"] = os.environ["AZURE_OPENAI_API_BASE_URL"]
        os.environ["LLM_AZURE_OPENAI_API_DEPLOYMENT"] = os.environ["AZURE_DEPLOYMENT_NAME"]
        
        #embed
        os.environ["EMBED_AZURE_OPENAI_API_KEY"] = os.environ["AZURE_EMBEDDING_API_KEY"]
        os.environ["EMBED_AZURE_OPENAI_API_VERSION"] = os.environ["AZURE_EMBEDDING_API_VERSION"]
        os.environ["EMBED_AZURE_OPENAI_API_ENDPOINT"] = os.environ["AZURE_EMBEDDING_API_BASE_URL"]
        os.environ["EMBED_AZURE_OPENAI_API_DEPLOYMENT"] = os.environ["AZURE_EMBEDDING_DEPLOYMENT_NAME"]

        config = {
            "llm": {
                "provider": "azure_openai",
                "config": {
                    "model": "luup",
                    "temperature": 0.1,
                    "max_tokens": 2000,
                }
            },
            "embedder": {
                "provider": "azureOpenai",
                "config": {
                    "model": "text-embedding-3-small",
                    "temperature": 0.1,
                    "max_tokens": 2000,
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "host": "localhost",
                    "port": 6333,
                }
            },
            "history_db_path":"../history.db"
        }

        m = Memory.from_config(config)
        return m
    
    def get_answer_at_once(self):
        return "yes. get_answer_at_once", sum("yes. get_answer_at_once")
        # assert isinstance(
        #     self.model, BaseChatModel
        # ), "model is not instance of LangChain BaseChatModel"
        # history = self._get_langchain_style_history()
        # response = self.model.generate(history)
        # return response.content, sum(response.content)

    def get_answer_stream_iter(self):
        if self.memory is None:
            self.memory = self.createMem0()
        userID = "xiaoming1"
        #读取历史
        history = self._get_langchain_style_history()
        #print(f"history:{history}")
        #本次输入内容加入记忆
        currContent = ""
        addMemory = ""
        if len(history) > 0:
            currContent = history[len(history)-1].content
            #print(f"currContent:{currContent}")
            addMemory = self.memory.add(data=currContent, user_id=userID, metadata={"category": "hobbies"})["addMemory"]
        ##本次记忆作为返回
        #completion = [addMemory]
        
        #读取所有记忆作为返回
        all_memories = self.memory.get_all(user_id=userID)
        completion = []
        for item in all_memories:
            completion.append("- "+item["memory"]+"\r\n")
            
        # it = CallbackToIterator()
        # assert isinstance(
        #     self.model, BaseChatModel
        # ), "model is not instance of LangChain BaseChatModel"
        
        # def thread_func():
        #     self.model(
        #         messages=history, callbacks=[ChuanhuCallbackHandler(it.callback)]
        #     )
        #     it.finish()

        # t = Thread(target=thread_func)
        # t.start()
        # partial_text = ""
        # for value in it:
        #     partial_text += value
        #     yield partial_text

        #completion=["yes ", "get_answer_stream_iter"]
        partial_text = ""
        for chunk in completion:
            partial_text += chunk
            yield partial_text
