from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
import os

from .base_model import Base_Chat_Langchain_Client, CallbackToIterator

# load_config_to_environ(["azure_openai_api_key", "azure_api_base_url", "azure_openai_api_version", "azure_deployment_name"])

class Azure_OpenAI_Client(Base_Chat_Langchain_Client):
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
    
    def get_answer_at_once(self):
        return "yes. get_answer_at_once", sum("yes. get_answer_at_once")
        # assert isinstance(
        #     self.model, BaseChatModel
        # ), "model is not instance of LangChain BaseChatModel"
        # history = self._get_langchain_style_history()
        # response = self.model.generate(history)
        # return response.content, sum(response.content)

    def get_answer_stream_iter(self):
        completion=[{"chunk":"yes "},{"chunk":"get_answer_stream_iter"}]
        partial_text = ""
        for chunk in completion:
            partial_text += chunk.choices[0].delta.content or ""
            yield partial_text

        # it = CallbackToIterator()
        # assert isinstance(
        #     self.model, BaseChatModel
        # ), "model is not instance of LangChain BaseChatModel"
        # history = self._get_langchain_style_history()

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
