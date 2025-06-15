from loaders.genage_loader import load_genage_data, is_longevity_gene
from loaders.ncbi_loader import fetch_gene_summary_ncbi
from loaders.ensembl_loader import fetch_ensembl_gene_info, fetch_gene_ontology
from loaders.uniprot_loader import fetch_uniprot_summary
from loaders.hgnc_loader import fetch_hgnc_info
from loaders.genecards_loader import fetch_genecards_summary
from loaders.alliance_loader import fetch_alliance_summary

def analyze_gene(gene_name):
    # GenAge
    genage_df = load_genage_data()
    in_genage = is_longevity_gene(gene_name, genage_df)

    # NCBI
    # ncbi_summary = fetch_gene_summary_ncbi(gene_name)
    ncbi_full = fetch_gene_summary_ncbi(gene_name)
    ncbi_summary = ncbi_full.get("Summary") if ncbi_full else None

    # Ensembl + GO
    ensembl_full = fetch_ensembl_gene_info(gene_name)
    ensembl_description = ensembl_full.get("description") if ensembl_full else None

    # ensembl_data = fetch_ensembl_gene_info(gene_name)
    # go_terms = fetch_gene_ontology(ensembl_data["id"]) if ensembl_data else []

    # UniProt
    uniprot_data = fetch_uniprot_summary(gene_name)

    # HGNC
    hgnc_data = fetch_hgnc_info(gene_name)
    
    # alliance
    #hgnc_id = hgnc_data.get("HGNC ID")
    #print(hgnc_id)
    #alliance_summary = fetch_alliance_summary(hgnc_id) if hgnc_id else None
    # GeneCards
    # genecards_summary = fetch_genecards_summary(gene_name)

    return {
        "gene_name": gene_name,
        "in_genage": in_genage,
        "ncbi_summary": ncbi_summary,
        "ensembl": ensembl_description,
        # "go_terms": go_terms,
        "uniprot": uniprot_data,
        # "hgnc": hgnc_data,
        # "genecards_summary": genecards_summary
        # "alliance_summary": alliance_summary
    }
