from flask import Flask, request, render_template, redirect, url_for, flash
import torch
import torch.nn as nn
import numpy as np
import os
from pydub import AudioSegment

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Conv1DNet(nn.Module):
    def __init__(self, num_classes):
        super(Conv1DNet, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=16, kernel_size=3)
        self.pool1 = nn.MaxPool1d(kernel_size=2)
        self.conv2 = nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3)
        self.pool2 = nn.MaxPool1d(kernel_size=2)
        self.conv3 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=3)
        self.global_pool = nn.AdaptiveMaxPool1d(1)
        self.fc1 = nn.Linear(64, 64)
        self.fc2 = nn.Linear(64, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.pool1(x)
        x = self.relu(self.conv2(x))
        x = self.pool2(x)
        x = self.relu(self.conv3(x))
        x = self.global_pool(x)
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def normalize_min_max(arr):
    min_val = np.min(arr)
    max_val = np.max(arr)
    return (arr - min_val) / (max_val - min_val)

def load_original():
    a = AudioSegment.from_mp3("original.mp3")
    a = a.set_frame_rate(44100).set_channels(1)
    y = np.array(a.get_array_of_samples())
    y = normalize_min_max(y)
    y = np.pad(y, (0, 80000 - len(y)), mode='constant', constant_values=0)
    return y[:-1].astype(np.float32).reshape(1, 1, -1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            contents = file.read().decode('utf-8')
            try:
                user_input = contents.strip('[]')
                user_input = [float(x.strip()) for x in user_input.split(',') if x.strip()]
                if len(user_input) != 79999:
                    return render_template('index.html', message="Input array must be of length 79999")

                user_input = np.array(user_input).astype(np.float32).reshape(1, 1, -1)
                original = load_original()
                diff = np.abs(original - user_input)
                if np.max(diff) > 0.25:
                    return render_template('index.html', message="This isn't the file I sent you!")

                model = Conv1DNet(num_classes=2)
                model.load_state_dict(torch.load('model_weights.pth', map_location=torch.device('cpu')))
                model.eval()

                with torch.no_grad():
                    user_input_tensor = torch.tensor(user_input)
                    output = model(user_input_tensor)
                    probabilities = torch.softmax(output, dim=1)
                    predicted_class = torch.argmax(probabilities, dim=1)

                if predicted_class.item() == 1:
                    return render_template('index.html', message="Thanks for helping me out! Here's a flag for your trouble: squ1rrel{brainrot}")
                else:
                    return render_template('index.html', message="No brainrot detected.")

            except Exception as e:
                return render_template('index.html', message=f"Error processing file: {str(e)}")

    return render_template('index.html', message="")

if __name__ == '__main__':
    app.run(port=4000)
