from pipeline.index_funds import get_opensearch_client, load_model
from scripts.query_funds import search_funds, print_results

PERSONAS = [
    {
        "name": "Major engineering donor",
        "interest": "graduate engineering research",
        "capacity": 500000,
    },
    {
        "name": "Small chemistry scholarship donor",
        "interest": "undergraduate scholarships in chemistry",
        "capacity": 25000,
    },
    {
        "name": "Faculty support donor with no unit preference",
        "interest": "faculty across the university",
        "capacity": 1000000,
    },
    {
        "name": "Small student services support campuswide",
        "interest": "career services across campus",
        "capacity": 1000,
    },
    {
        "name": "Massive Biochem chair creator",
        "interest": "administrative chair of the Biochemistry Department",
        "capacity": 10000000,
    },
]

def run_personas():
    client = get_opensearch_client()
    model = load_model()

    for persona in PERSONAS:
        print("=" * 80)
        print(f"Persona: {persona['name']}")
        print(f"Interest: {persona['interest']} | Capacity ${persona['capacity']:,}")
        print("=" * 80)

        response = search_funds(
            client,
            model,
            persona['interest'],
            persona['capacity'],
            persona.get('unit'),
            persona.get('purpose'),
        )
        print_results(response)

if __name__ == "__main__":
    run_personas()