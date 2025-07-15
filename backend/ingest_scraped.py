import json, sys
from data_collection.stackoverflow_scraper import scrape_stackoverflow
from data_collection.reddit_scraper import scrape_reddit
from embeddings.embedder import embed_texts
# We will import chromadb directly here to manage the collection.
import chromadb
import os

# Adjusting sys.path if necessary, ensure these are correct based on your root folder
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # This might be needed depending on how you run it

# Initialize Chroma client globally or pass it. For simplicity, we'll get it here.
client = chromadb.PersistentClient(path="./chroma_storage")

def store_scraped_data_in_chroma(tag="python", n=5, source="all"):
    # Get or create the collection
    collection = client.get_or_create_collection(name="qa_collection") #

    # Clear existing documents in the collection before adding new ones
    # This prevents duplicate data and ensures the selected source's data is fresh
    try:
        collection.delete(ids=collection.get(include=[])['ids'])
        print("✅ Cleared existing documents from the collection.")
    except Exception as e:
        print(f"⚠️ Could not clear existing documents (might be empty): {e}")


    scraped = []
    if source == "stackoverflow" or source == "all":
        so_data = scrape_stackoverflow(tag, n)
        scraped.extend(so_data)
    if source == "reddit" or source == "all":
        reddit_data = scrape_reddit("learnpython", n)
        scraped.extend(reddit_data)

    with open(f"scraped_{tag}.json", "w", encoding="utf-8") as f:
        json.dump(scraped, f, ensure_ascii=False, indent=2)

    documents, ids, metas = [], [], []
    for idx, item in enumerate(scraped):
        qid = f"{tag}_{idx}"
        title = item.get("title", "").strip()
        question = item.get("question", "").strip()
        answer = (item.get("answer") or "").strip()

        source_url = item.get("url", "")

        content_to_embed = f"Q: {title} {question}" if question else f"Q: {title}"

        if not content_to_embed.strip():
            continue

        documents.append(content_to_embed)
        ids.append(f"{qid}_q")
        metas.append({"type": "question", "title": title, "source": source_url})

        if answer:
            documents.append(f"A: {answer}")
            ids.append(f"{qid}_a")
            metas.append({"type": "answer", "title": title, "source": source_url})

    if documents:
        embeds = embed_texts(documents)
        collection.add(documents=documents, ids=ids, metadatas=metas, embeddings=embeds) # Use the local collection object
        print(f"✅ Stored {len(documents)} documents from {source}.")
    else:
        print(f"🤷 No documents found to store from {source}.")

if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "python"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    source_choice = sys.argv[3] if len(sys.argv) > 3 else "all"
    store_scraped_data_in_chroma(tag, count, source_choice)