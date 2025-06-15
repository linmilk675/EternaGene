import requests

STRING_API_URL = "https://string-db.org/api"
OUTPUT_FORMAT = "json"
METHOD = "network"

# Организм: человек (taxon ID: 9606)
SPECIES_ID = 9606

def fetch_string_interactions(gene_name, required_score=700, limit=10):
    """
    Получает взаимодействия гена из STRING (min required_score от 0 до 1000).
    Возвращает список партнёров взаимодействий.
    """
    params = {
        "identifiers": gene_name,
        "species": SPECIES_ID,
        "required_score": required_score,
        "limit": limit,
        "caller_identity": "your_script_or_app_name",  # ОБЯЗАТЕЛЬНО
    }

    request_url = f"{STRING_API_URL}/{OUTPUT_FORMAT}/{METHOD}"
    try:
        response = requests.get(request_url, params=params)
        response.raise_for_status()
        interactions = response.json()
    except Exception as e:
        print(f"[STRING] Ошибка запроса: {e}")
        return None

    partners = []
    for interaction in interactions:
        if interaction.get("preferredName_A") == gene_name:
            partner = interaction.get("preferredName_B")
        else:
            partner = interaction.get("preferredName_A")
        partners.append({
            "partner": partner,
            "score": interaction.get("score", 0.0)
        })

    return partners
