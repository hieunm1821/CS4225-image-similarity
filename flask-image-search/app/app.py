from matplotlib import image
import pandas as pd 
import time
from flask import Flask, render_template, request, jsonify
# create flask instance
app = Flask(__name__)


# main route
@app.route('/')
def index():
    return render_template('index.html')


# search route
@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        RESULTS_ARRAY = []
        # get url
        image_url = request.form.get('img')
        try:
            time.sleep(5)
            image_url = image_url.split("/")[-1].split(".")[0]
            results = pd.read_csv("app/data/" + image_url + ".csv")
            # loop over the results, displaying the score and image name
            for (resultID, content) in results.iterrows():
                RESULTS_ARRAY.append(
                    {"image": str(content["path"]).replace("data", "static"), "score": str(content["distCol"])})
            # return success
            return jsonify(results=(RESULTS_ARRAY[:4]))
        except:
            # return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500

# run!
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
