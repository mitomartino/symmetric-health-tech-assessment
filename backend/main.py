# -----------------------------------------------------------------------------
# dependencies
# -----------------------------------------------------------------------------
from flask import Flask
from flask import jsonify
from flask import request
import indexer

# -----------------------------------------------------------------------------
# application setup 
# -----------------------------------------------------------------------------

app = Flask(__name__)
searchIndex = indexer.Index('../sample_data.csv.gz')

# -----------------------------------------------------------------------------
# routes
# -----------------------------------------------------------------------------

@app.route('/header')
def getHeader():
    return {'header': searchIndex.header}
    
@app.route('/data')
def search():
    terms = request.args.get('terms')
    results = {"entries":[], "count": 0}

    if terms:
        results['entries'] = searchIndex.search(terms.split())
        results['count'] = len(results['entries'])
        
    return results

# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run()

# -----------------------------------------------------------------------------
# end main.py
# -----------------------------------------------------------------------------
