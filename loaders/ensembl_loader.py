import requests

ENSEMBL_REST = "https://rest.ensembl.org"

def fetch_ensembl_gene_info(gene_symbol):
    url = f"{ENSEMBL_REST}/lookup/symbol/homo_sapiens/{gene_symbol}?content-type=application/json"
    r = requests.get(url)
    if not r.ok:
        return None
    return r.json()

def fetch_gene_ontology(gene_id):
    url = f"{ENSEMBL_REST}/xrefs/id/{gene_id}?content-type=application/json"
    r = requests.get(url)
    if not r.ok:
        return []
    return [entry for entry in r.json() if entry["dbname"] == "GO"]
