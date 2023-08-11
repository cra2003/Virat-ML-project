from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)


with open('./model.pkl', 'rb') as f:
    gr = pickle.load(f)

@app.route('/')
def home():
    
    return render_template('virat.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    try:
        opp = request.form.get('opposition')
        form= request.form.get('format')
        inn = request.form.get('innings')
        
        arr=[0]*20
        l=['Afghanistan', 'Australia', 'Bangladesh', 'England', 'HongKong',
       'Ireland', 'Netherlands', 'NewZealand', 'Pakistan', 'Scotland',
       'SouthAfrica', 'SriLanka', 'U.A.E.', 'WestIndies', 'Zimbabwe', 'odi',
       't20', 'test', '1', '2']
        arr[l.index(opp)]=1
        arr[l.index(form)]=1
        arr[l.index(inn)]=1

        predicted_score = None
        if gr.predict([arr])[0]==0:
            predicted_score = 'predicted score <30'
        elif gr.predict([arr])[0]==1:
            predicted_score = 'predicted score 30-50'
        else:
            predicted_score = 'predicted score >50'
        
        return render_template('virat.html', predicted_score=predicted_score)
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
