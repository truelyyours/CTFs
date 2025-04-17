import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from pydub import AudioSegment

# 1. Load and preprocess original audio (as server does)
def load_original():
    a = AudioSegment.from_mp3("original.mp3")
    a = a.set_frame_rate(44100).set_channels(1)
    y = np.array(a.get_array_of_samples(), dtype=np.float32)
    y = (y - y.min()) / max(1e-10, (y.max() - y.min()))  # Avoid division by zero
    y = np.pad(y, (0, 80000 - len(y)), mode='constant')[:79999]
    return torch.FloatTensor(y).reshape(1, 1, -1).requires_grad_(False)

original = load_original()


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


# 2. Load the model (same architecture as server)
model = Conv1DNet(num_classes=2)  # Use the class definition from earlier
model.load_state_dict(torch.load("model_weights.pth"))
model.eval()

# --- 2. Optimization setup ---
input_tensor = original.clone().detach().requires_grad_(True)
optimizer = optim.Adam([input_tensor], lr=0.0001)  # Lower LR for finer control

best_input = None
best_prob = 0.0

# --- 3. Optimization loop ---
for epoch in range(1000):
    optimizer.zero_grad()
    output = model(input_tensor)
    prob_class1 = torch.softmax(output, dim=1)[0, 1].item()
    loss = -output[0, 1]  # Maximize class 1 probability
    
    loss.backward()
    optimizer.step()
    
    # --- 4. Project back to ±0.25 constraint ---
    with torch.no_grad():
        input_tensor.data = torch.clamp(input_tensor, original - 0.2, original + 0.2)
        input_tensor.data = torch.clamp(input_tensor, 0, 1)  # Ensure valid audio range
    
    # --- 5. Track best candidate ---
    if prob_class1 > best_prob:
        best_prob = prob_class1
        best_input = input_tensor.clone().detach()
        # print(f"New best: Class 1 prob = {best_prob:.4f}")

    # --- 6. Save every 100 epochs ---
    if epoch % 100 == 0:
        current_input = input_tensor.detach().numpy().flatten()
        with open(f'optimized_epoch_{epoch}.txt', 'w') as f:
            f.write('[' + ','.join(map(str, current_input)) + ']')

# --- 7. Save the best candidate ---
best_input_np = best_input.numpy().flatten()
with open('best_optimized_input.txt', 'w') as f:
    f.write('[' + ','.join(map(str, best_input_np)) + ']')

# --- 8. Verify ---
with torch.no_grad():
    final_output = model(best_input)
    predicted_class = final_output.argmax().item()
    max_diff = torch.abs(best_input - original).max().item()
    print(f"Final prediction: {predicted_class} (prob={best_prob:.4f}, max_diff={max_diff:.6f})")

import requests  # For interacting with the server

def test_on_server(file_content):
    response = requests.post(
        'http://http://52.188.82.43:8050/upload',
        files={'file': ('test.txt', file_content)},
        allow_redirects=False
    )
    return response.text

# Test 1: Send all zeros
zeros = np.zeros(79999, dtype=np.float32)
test_on_server(f"[{','.join(map(str, zeros))}]")

# Test 2: Send all 0.5s
halfs = np.full(79999, 0.5, dtype=np.float32)
test_on_server(f"[{','.join(map(str, halfs))}]")

# Test 3: Send your original
orig = load_original().numpy().flatten()
test_on_server(f"[{','.join(map(str, orig))}]")