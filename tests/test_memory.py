import pytest

from mem0 import Memory
import os

def createMem0():
    #llm
    os.environ["AZURE_API_KEY"] = "3ed55470cade452cb907e5a928a587d6"
    os.environ["AZURE_API_BASE"] = "https://LuupAI.openai.azure.com/openai/deployments/luup/chat/completions?api-version=2023-03-15-preview"
    os.environ["AZURE_API_VERSION"] = "2023-03-15-preview"

    #embed
    os.environ["AZURE_OPENAI_API_KEY"] = "3ed55470cade452cb907e5a928a587d6"
    os.environ["AZURE_OPENAI_API_VERSION"] = "2023-05-15"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "https://LuupAI.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"

    config = {
        "llm": {
            "provider": "litellm",
            "config": {
                "model": "azure_ai/command-r-plus",
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


@pytest.fixture
def memory_store():
    return Memory()

@pytest.mark.skip(reason="Not implemented")
def test_create_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.create(data=data)
    assert memory_store.get(memory_id) == data


@pytest.mark.skip(reason="Not implemented")
def test_get_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.create(data=data)
    retrieved_data = memory_store.get(memory_id)
    assert retrieved_data == data


@pytest.mark.skip(reason="Not implemented")
def test_update_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.create(data=data)
    new_data = "Name is John Kapoor."
    updated_memory = memory_store.update(memory_id, new_data)
    assert updated_memory == new_data
    assert memory_store.get(memory_id) == new_data


@pytest.mark.skip(reason="Not implemented")
def test_delete_memory(memory_store):
    data = "Name is John Doe."
    memory_id = memory_store.create(data=data)
    memory_store.delete(memory_id)
    assert memory_store.get(memory_id) is None


@pytest.mark.skip(reason="Not implemented")
def test_history(memory_store):
    data = "I like indian food."
    memory_id = memory_store.create(data=data)
    history = memory_store.history(memory_id)
    assert history == [data]
    assert memory_store.get(memory_id) == data

    new_data = "I like italian food."
    memory_store.update(memory_id, new_data)
    history = memory_store.history(memory_id)
    assert history == [data, new_data]
    assert memory_store.get(memory_id) == new_data


@pytest.mark.skip(reason="Not implemented")
def test_list_memories(memory_store):
    data1 = "Name is John Doe."
    data2 = "Name is John Doe. I like to code in Python."
    memory_store.create(data=data1)
    memory_store.create(data=data2)
    memories = memory_store.list()
    assert data1 in memories
    assert data2 in memories

if __name__ == '__main__':
    testAPI()
