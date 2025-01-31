from flask import Flask, jsonify, request, render_template
from scraping_methods import *

app = Flask(__name__)

def print_formatted_profile(profile_text):
    print("\n" + "="*80)
    print(profile_text)
    print("="*80 + "\n")

STATE_ABBREV = {
    'alabama': 'AL',
    'alaska': 'AK',
    'arizona': 'AZ',
    'arkansas': 'AR',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'delaware': 'DE',
    'florida': 'FL',
    'georgia': 'GA',
    'hawaii': 'HI',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'iowa': 'IA',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'maine': 'ME',
    'maryland': 'MD',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'mississippi': 'MS',
    'missouri': 'MO',
    'montana': 'MT',
    'nebraska': 'NE',
    'nevada': 'NV',
    'new hampshire': 'NH',
    'new jersey': 'NJ',
    'new mexico': 'NM',
    'new york': 'NY',
    'north carolina': 'NC',
    'north dakota': 'ND',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'rhode island': 'RI',
    'south carolina': 'SC',
    'south dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'utah': 'UT',
    'vermont': 'VT',
    'virginia': 'VA',
    'washington': 'WA',
    'west virginia': 'WV',
    'wisconsin': 'WI',
    'wyoming': 'WY',
    'washington dc': 'DC'
}

@app.route('/wiki', methods = ['GET'])
def get_wiki_content(): 
    try:
        area = request.args.get('area')

        # return error if no area is given
        if area == None:
            return jsonify({'error': 'No area given'}), 400
        
        # call for the retrieval of wiki article pinged
        result = wiki_demo_scrape(area)

        return jsonify(result)

    except:
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/eia', methods = ['GET'])
def get_eia_content(): 
    try:
        state_code = request.args.get('state_code')

        # return error if no area is given
        if state_code == None:
            return jsonify({'error': 'No area given'}), 400
        
        # call for the retrieval of wiki article pinged
        result = eia_profile_scrape(state_code)

        return jsonify(result)

    except:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/profile', methods=['GET'])
def get_complete_profile():
    try:
        location = request.args.get('location')
        
        if location is None:
            return jsonify({'error': 'No location provided'}), 400
  
        parts = location.split(',')
        if len(parts) != 2:
            return jsonify({'error': 'Location must be in format: city,state'}), 400
            
        city = parts[0].strip()
        state = parts[1].strip()
        
        wiki_format = f"{city},_{state}"
        
        state = state.lower()
        state_code = STATE_ABBREV.get(state)
        
        wiki_result = wiki_demo_scrape(wiki_format)
        eia_result = eia_profile_scrape(state_code)
        
        combined_profile = {
            "location": location,
            "community_profile": wiki_result.get("area_information"),
            "state_energy_profile": eia_result.get("state_information")
        }
        
        print_formatted_profile(combined_profile["community_profile"])
        print_formatted_profile(combined_profile["state_energy_profile"])

        with open(f"community_energy_profile_{location}.txt", 'w') as f:
            f.write(f"Community Profile for {location}\n")
            f.write("="*80 + "\n")
            f.write(combined_profile["community_profile"])
            f.write("\n\n")
            f.write("Energy Profile\n")
            f.write("="*80 + "\n")
            f.write(combined_profile["state_energy_profile"])
        
        return jsonify(combined_profile)
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)