import requests, time

def fetch_top_answer(question_id):
    time.sleep(1)
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {"order": "desc", "sort": "votes", "site": "stackoverflow", "pagesize": 1, "filter": "!9_bDE(B6I"}
    res = requests.get(url, params=params)
    if res.status_code != 200: return None
    answers = res.json().get("items", [])
    return answers[0].get("body_markdown", "") if answers else None

def scrape_stackoverflow(tag="python", num_questions=20):
    print(f"📡 Fetching StackOverflow questions with tag: {tag}")
    url = "https://api.stackexchange.com/2.3/questions"
    params = {"order": "desc", "sort": "votes", "tagged": tag, "site": "stackoverflow",
              "pagesize": num_questions, "filter": "!9_bDE(fI5"}
    response = requests.get(url, params=params)
    if response.status_code != 200: return []
    data = response.json().get("items", [])
    results = []
    for item in data:
        answer = fetch_top_answer(item["question_id"])
        results.append({
            "title": item["title"],
            "question": item.get("body_markdown", ""),
            "answer": answer,
            "url": item["link"],
            "is_answered": item.get("is_answered", False)
        })
    return results
