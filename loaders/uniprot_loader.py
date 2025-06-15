import requests

def fetch_uniprot_summary(gene_symbol, organism="human"):
    search_url = "https://rest.uniprot.org/uniprotkb/search"
    query = f'{gene_symbol}+{organism}'

    params = {
        "query": query,
        "format": "json",
        "size": 1
    }

    response = requests.get(search_url, params=params)
    print(f"URL: {response.url}")
    if not response.ok:
        print(f"[UniProt] Ошибка поиска: {response.status_code}")
        print(f"URL: {response.url}")
        return None

    data = response.json()
    results = data.get("results", [])
    if not results:
        print(f"[UniProt] Не найдено данных для гена {gene_symbol}")
        return None

    # получаем accession и переходим к детальному запросу
    accession = results[0]["primaryAccession"]
    entry_url = f"https://www.uniprot.org/uniprotkb/{accession}.json"
    entry_resp = requests.get(entry_url)

    if not entry_resp.ok:
        print(f"[UniProt] Ошибка при получении данных для {accession}")
        return None

    entry = entry_resp.json()
    summary = {
        "UniProt ID": accession,
        "Protein name": None,
        "Function": None,
        "UniProt URL": f"https://www.uniprot.org/uniprotkb/{accession}/entry"
    }

    # Название белка
    try:
        summary["Protein name"] = entry["proteinDescription"]["recommendedName"]["fullName"]["value"]
    except KeyError:
        pass

    # Функция
    for comment in entry.get("comments", []):
        if comment.get("commentType") == "FUNCTION":
            summary["Function"] = comment["texts"][0]["value"]
            break

    return summary
