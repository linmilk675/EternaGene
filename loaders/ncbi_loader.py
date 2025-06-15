from Bio import Entrez

Entrez.email = "debian576@gmail.com"

def fetch_gene_summary_ncbi(gene_name):
    handle = Entrez.esearch(db="gene", term=f"{gene_name}[Gene Name] AND Homo sapiens[Organism]")
    record = Entrez.read(handle)
    handle.close()

    if not record["IdList"]:
        return None

    gene_id = record["IdList"][0]
    summary_handle = Entrez.esummary(db="gene", id=gene_id)
    summary = Entrez.read(summary_handle)
    summary_handle.close()

    return summary["DocumentSummarySet"]["DocumentSummary"][0]
