from googlesearch import search
import requests
import json
from bs4 import BeautifulSoup
import os

API_KEY = os.getenv('OPENROUTER_API_KEY')
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

models = {
    "main": "deepseek/deepseek-chat-v3-0324:free",
    "classifier": "deepseek/deepseek-chat-v3-0324:free"
}

def get_response_llm(api_key, base_url, model_name, user_prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    }

    response = requests.post(url=base_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

def get_google_results(query, num_results=5):
    refined_query = f"{query} site:.com OR site:.org OR site:.gov OR site:.edu"
    return list(search(refined_query, num_results=num_results))

def filter_reliable_sources(urls):
    trusted_domains = ["cnn.com", "bbc.com", "kompas.com", "detik.com", "wikipedia.org"]
    return [url for url in urls if any(td in url for td in trusted_domains)]

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all(['p', 'article', 'div'])
        text = "\n".join(p.get_text() for p in paragraphs)
        return text.strip()
    except Exception:
        return ""

def chunk_text(text, chunk_size=3000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_text(text, model_name, original_prompt):
    prompt = f"""
Berikut adalah informasi dari hasil pencarian web:

\"\"\"
{text}
\"\"\"

Berdasarkan teks di atas, jawablah pertanyaan ini:

"{original_prompt}"

Gunakan data faktual yang tersedia, jangan mengarang. Jika tidak ditemukan jawaban, katakan "Informasi tidak ditemukan di sumber."
"""
    response = get_response_llm(API_KEY, BASE_URL, model_name, prompt)
    if isinstance(response, dict):
        return response["choices"][0]["message"]["content"]
    else:
        return "Gagal merangkum."

def search_and_ask_llm(prompt, model_name):
    print("[INFO] Melakukan pencarian di Google...")
    urls = get_google_results(prompt)
    urls = filter_reliable_sources(urls)

    if not urls:
        return "Tidak ditemukan hasil yang relevan."

    all_text = ""
    for url in urls:
        print(f"[INFO] Mengambil dan memproses: {url}")
        text = extract_text_from_url(url)
        if text:
            all_text += text + "\n\n"

    if not all_text.strip():
        return "Tidak berhasil mengambil isi dari halaman-halaman web."

    print("[INFO] Melakukan chunking dan ringkasan bertahap...")
    chunks = chunk_text(all_text)
    summaries = [summarize_text(chunk, model_name, prompt) for chunk in chunks]
    final_summary = "\n".join(summaries)

    print("[INFO] Menghasilkan jawaban akhir dari ringkasan...")
    final_prompt = f"""
Gunakan informasi berikut untuk menjawab pertanyaan secara akurat:

Ringkasan:
\"\"\"
{final_summary}
\"\"\"

Pertanyaan:
{prompt}
"""
    response = get_response_llm(API_KEY, BASE_URL, model_name, final_prompt)
    if isinstance(response, dict):
        return response["choices"][0]["message"]["content"]
    else:
        return response

def llm_decides_need_for_web(prompt):
    classifier_prompt = f"""
Evaluasilah pertanyaan berikut:

"{prompt}"

Apakah pertanyaan ini membutuhkan pencarian informasi terbaru atau kontekstual dari internet?

Jika YA, jawab hanya: "YA"
Jika TIDAK, jawab hanya: "TIDAK"
"""

    response = get_response_llm(API_KEY, BASE_URL, models["classifier"], classifier_prompt)
    if isinstance(response, dict):
        answer = response["choices"][0]["message"]["content"].strip().lower()
        return "ya" in answer
    else:
        return False

def main():
    user_prompt = input("Masukkan pertanyaanmu: ")

    print("[INFO] Mengevaluasi apakah perlu pencarian web...")
    if llm_decides_need_for_web(user_prompt):
        answer = search_and_ask_llm(user_prompt, models["main"])
    else:
        print("[INFO] Pertanyaan langsung dijawab oleh LLM...")
        response = get_response_llm(API_KEY, BASE_URL, models["main"], user_prompt)
        if isinstance(response, dict):
            answer = response["choices"][0]["message"]["content"]
        else:
            answer = response

    print("\n[LLM Response]")
    print(answer)

if __name__ == "__main__":
    main()