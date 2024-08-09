import pytest
#import sys
#sys.path.append('./')
from flask import Flask, jsonify, request
from mem0.memory.main import Memory
import os

app = Flask(__name__)
memory=None

def createMem0():
    #llm
    os.environ["LLM_AZURE_OPENAI_API_KEY"] = "3ed55470cade452cb907e5a928a587d6"
    os.environ["LLM_AZURE_OPENAI_API_VERSION"] = "2023-03-15-preview"#"2024-05-13"#
    os.environ["LLM_AZURE_OPENAI_API_ENDPOINT"] = "https://LuupAI.openai.azure.com/openai/deployments/luup/chat/completions?api-version=2023-03-15-preview"
    os.environ["LLM_AZURE_OPENAI_API_DEPLOYMENT"] = "luup"
    
    #embed
    os.environ["EMBED_AZURE_OPENAI_API_KEY"] = "3ed55470cade452cb907e5a928a587d6"
    os.environ["EMBED_AZURE_OPENAI_API_VERSION"] = "2023-05-15"#"1"#
    os.environ["EMBED_AZURE_OPENAI_API_ENDPOINT"] = "https://LuupAI.openai.azure.com/openai/deployments/text-embedding-3-small/embeddings?api-version=2023-05-15"
    os.environ["EMBED_AZURE_OPENAI_API_DEPLOYMENT"] = "text-embedding-3-small"

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

@app.route("/add", methods=["POST"])   
def testAPI():
    data = request.get_json()
    content = data.get("content")
    userID = "lilei"#data.get("userID")
    try:
        result = memory.add(content, user_id=userID, metadata={"category": "events"})
    except Exception as e:
        return jsonify({"data": f"{e}"}), 500
    # print("add to mem0 2 ...")
    #mid2 = memory.add("I likes to fly kite on weekends", user_id="alice", metadata={"category": "hobbies"})
    #print(mid2)
    #cont1=memory.get('a5f3bafb-5e62-49df-ad80-f3d495f4c272')
    #print(cont1)

    
    # Get all memories
    #print("-------合并后的记忆：get all from alice...")
    #all_memories = memory.get_all(user_id="alice")
    #print(all_memories)
    #print("-------合并后的记忆：get all from mike...")
    all_memories = memory.get_all(user_id=userID)
    simple_memories = []
    for item in all_memories:
        simple_memories.append(item["memory"])
    #print(simple_memories)
    return jsonify({"data": f"{simple_memories}"}), 200

if __name__ == '__main__':
    if memory is None:
        memory = createMem0()
    app.run(host="0.0.0.0", port=5000, debug=False)
    #testAPI()

