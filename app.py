import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from utils.video_processor import process_video
from utils.model_loader import load_model

app = Flask(__name__)
app.secret_key = '8a688084a95cdfac893e9b48506e238b15036f46120b2c330d71cea1002f27fd'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB limit

# Load model at startup
model = load_model('models/deepfake_model.h5')

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('home'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('home'))
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process video
        result = process_video(filepath, model)
        
        # Save to user history (if logged in)
        if 'user_id' in session:
            save_to_history(session['user_id'], filename, result)
        
        return render_template('results.html', 
                            filename=filename,
                            result=result,
                            confidence=result['confidence'])

# Authentication routes would go here...

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)