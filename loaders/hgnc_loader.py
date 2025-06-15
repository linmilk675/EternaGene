import requests

def fetch_hgnc_info(gene_symbol):
    url = f"https://rest.genenames.org/fetch/symbol/{gene_symbol}"
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers)

    if not r.ok:
        return None

    docs = r.json()["response"]["docs"]
    if not docs:
        return None

    entry = docs[0]
    return {
        "HGNC ID": entry.get("hgnc_id"),
        "Approved Name": entry.get("name"),
        "Synonyms": entry.get("alias_symbol", [])
    }
