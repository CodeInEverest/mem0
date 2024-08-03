import os
from openai import OpenAI
from openai import AzureOpenAI
from mem0.embeddings.base import EmbeddingBase


class AzureOpenAIEmbedding(EmbeddingBase):
    def __init__(self, model="text-embedding-3-small"):# model = "deployment_name"
        self.model = model
        self.dims = 1536

        self.client = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),
            api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    def embed(self, text): 
        #text = text.replace("\n", " ")
        return (
            self.client.embeddings.create(input = [text], model=self.model)
            .data[0]
            .embedding
        )
    