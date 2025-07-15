import chromadb

client = chromadb.PersistentClient(path="./chroma_storage")
collection = client.get_or_create_collection(name="qa_collection")

def add_documents(docs, ids, metas, embeddings):
    collection.add(documents=docs, ids=ids, metadatas=metas, embeddings=embeddings)
