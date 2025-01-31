from celery import Celery
from scraping_methods import wiki_demo_scrape, eia_profile_scrape

celery = Celery('tasks',
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')  

@celery.task
def generate_profile(location, city, state, state_code):
    try:
        wiki_format = f"{city},_{state}"
        wiki_result = wiki_demo_scrape(wiki_format)
        eia_result = eia_profile_scrape(state_code)
        
        combined_profile = {
            "location": location,
            "community_profile": wiki_result.get("area_information"),
            "state_energy_profile": eia_result.get("state_information")
        }

        with open(f"community_energy_profile_{location}.txt", 'w') as f:
            f.write(f"Community Profile for {location}\n")
            f.write("="*80 + "\n")
            f.write(combined_profile["community_profile"])
            f.write("\n\n")
            f.write("Energy Profile\n")
            f.write("="*80 + "\n")
            f.write(combined_profile["state_energy_profile"])
            
        return combined_profile
    except Exception as e:
        return {"error": str(e)}