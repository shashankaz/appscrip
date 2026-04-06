def generate_markdown_report(sector: str, analysis: str, source_count: int) -> str:
    normalized_sector = " ".join(word.capitalize() for word in sector.split())
    return (
        f"# {normalized_sector} Sector Analysis\n\n"
        f"Generated for the India market using {source_count} recent source(s).\n\n"
        f"{analysis.strip()}\n"
    )
