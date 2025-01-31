from flask import Flask, jsonify, request, render_template
from scraping_methods import *
from tasks import generate_profile

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
    'new_hampshire': 'NH',
    'new_jersey': 'NJ',
    'new_mexico': 'NM',
    'new_york': 'NY',
    'north_carolina': 'NC',
    'north_dakota': 'ND',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'rhode_island': 'RI',
    'south_carolina': 'SC',
    'south_dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'utah': 'UT',
    'vermont': 'VT',
    'virginia': 'VA',
    'washington': 'WA',
    'west virginia': 'WV',
    'wisconsin': 'WI',
    'wyoming': 'WY',
    'washington_dc': 'DC'
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
        state_lower = state.lower()
        state_code = STATE_ABBREV.get(state_lower)
        
        if state_code is None:
            return jsonify({'error': 'Invalid state name'}), 400

        # Start async task
        task = generate_profile.delay(location, city, state, state_code)
        
        return jsonify({
            'message': 'Profile generation initiated',
            'task_id': task.id,
            'status': 'Processing'
        }), 202
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = generate_profile.AsyncResult(task_id)
    if task.ready():
        result = task.get()
        return jsonify({
            'status': 'Completed',
            'result': result
        })
    return jsonify({
        'status': 'Processing'
    })

if __name__ == '__main__':
    app.run(debug=True)