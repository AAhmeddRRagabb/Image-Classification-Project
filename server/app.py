# --------------------------------------------------------------------------
# بسم الله الرحمن الرحيم
# الحمد لله رب العالمين 
# والصلاة والسلام على أشرف المرسلين - صلى الله عليه وسلم
# Image Classification App - The server file
# --------------------------------------------------------------------------

# Basic Imports & cfg
from flask import Flask, render_template, request, jsonify 
from utils.classification import classify, load_json_classes, load_model
from utils.llm_details import get_shikh_details
from pathlib import Path
import re
import os


app = Flask(__name__)
BASE_DIR = Path(__file__).parent
port = 5000

# --------------------------------------------------------------------------
# Routing

# Render the Main HTML File
@app.route("/")
def home():
    return render_template("index.html")


# Receiving & Classifying Images
@app.route("/api/on-receive-img", methods=["POST", "GET"])
def process_img():
    # Receiving
    payload = request.get_json(silent=True)
    if not payload or "img" not in payload:
        return jsonify({
                "status": "SERVER_ERR",
                "prediction": "-1",
                "message": 'لم يتم إرسال صورة'
        })
    

    img = payload["img"].split(f'{port}/')[1]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, img)

    try:

        # Classifying the Image
        cls, _ = classify(image_path, model=model) 

        prediction = classes.get(str(cls), {}).get("arabic_name", "")

        return jsonify({
            "status": "SUCCESS",
            "prediction": prediction,
            "message": "تم التصنيف بنجاح"
        })
    
        
    except Exception as e:
        return jsonify({
            "status": "CLASSIFICATION_ERR",
            "prediction": None,
            "message": 'حدث خطأ، رجاء المحاولة مرة أخرى مع اختيار صورة أعلى جودة'
        })



# Interacting with the LLM model
@app.route('/api/llm-get-details', methods = ['POST', 'GET'])
def process_llm_response():
    payload = request.get_json(silent = True)
    if not payload or 'prompt' not in payload:
        return jsonify ({
            "status"  : 'SERVER_ERR',
            'details' : -1,
            'message' : 'لم يتم تلقي أمر'
        })
    
    prompt = payload['prompt']
    
    # Asking LLM for details about the shikh
    response = get_shikh_details(prompt = prompt)

    if response['status'] == 'LLM_ERR':
        return jsonify({
            'status' : 'LLM_ERR',
            'details' : '',
            'message'  : 'فشل في استدعاء النموذج'
        })
    

    details = re.sub(r"<think>.*?</think>", "", response['details'], flags=re.DOTALL).strip()

    return jsonify({
        'status'  : 'SUCCESS',
        'details' : details,
        'message'  : 'تم، الحمد لله'
    })






# --------------------------------------------------------------------------

# Running the App   
if __name__ == "__main__":
    model = load_model()
    classes = load_json_classes()
    app.run(debug=True, port=port)
