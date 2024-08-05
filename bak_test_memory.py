import pytest
#import sys
#sys.path.append('./')

from mem0.memory.main import Memory
import os

def createMem0():
    #llm
    os.environ["AZURE_API_KEY"] = "3ed55470cade452cb907e5a928a587d6"
    os.environ["AZURE_API_BASE"] = "https://LuupAI.openai.azure.com/openai/deployments/luup/chat/completions?api-version=2023-03-15-preview"
    os.environ["AZURE_API_VERSION"] = "2023-03-15-preview"#"2024-05-13"#
    
    #embed
    os.environ["AZURE_OPENAI_API_KEY"] = "3ed55470cade452cb907e5a928a587d6"
    os.environ["AZURE_OPENAI_API_VERSION"] = "2023-05-15"#"1"#
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://LuupAI.openai.azure.com/openai/deployments/text-embedding-3-small/embeddings?api-version=2023-05-15"

    config = {
        "llm": {
            "provider": "litellm",
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
        "history_db_path":"/home/azureuser/ailurus/history.db"
    }

    m = Memory.from_config(config)
    return m
    
def testAPI():
    m = createMem0()
    print("add to mem0 1 ...")
    m.add("I likes to play cricket on weekends", user_id="alice", metadata={"category": "hobbies"})
    print("add to mem0 2 ...")
    m.add("I likes hopping too", user_id="alice", metadata={"category": "hobbies"})
    # Get all memories
    print("get all from mem0...")
    all_memories = m.get_all()
    print(all_memories)


if __name__ == '__main__':
    testAPI()
