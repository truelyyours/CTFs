import mido
import numpy as np
from scipy.io.wavfile import write

# Load the MIDI file
midi_file_path = "transmission.mid"
mid = mido.MidiFile(midi_file_path)

# Define parameters
SAMPLE_RATE = 44100  # Standard sample rate for WAV
DURATION_PER_TICK = 0.01  # Approximate duration per MIDI tick (adjustable)
AMPLITUDE = 0.5  # Volume of the sine wave

# Define new tempo for 145 BPM
BPM = 145
TICKS_PER_BEAT = 96  # Based on MIDI file metadata
MICROSECONDS_PER_BEAT = int(60_000_000 / BPM)  # Convert BPM to µs per beat

# Convert MIDI ticks to seconds
SECONDS_PER_TICK = MICROSECONDS_PER_BEAT / (TICKS_PER_BEAT * 1_000_000)


# Function to generate a sine wave for a given note and duration
def generate_sine_wave(frequency, duration, sample_rate=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return AMPLITUDE * np.sin(2 * np.pi * frequency * t)

# MIDI note to frequency conversion (A4 = 440Hz, MIDI 69)
def midi_to_freq(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12.0))

# Process MIDI file and generate audio samples
audio_data = np.zeros(int(SAMPLE_RATE * 10))  # 10 sec buffer
current_time = 0

for msg in mid.play():
    if msg.type == 'note_on' and msg.velocity > 0:
        frequency = midi_to_freq(msg.note)
        duration = SECONDS_PER_TICK * msg.time  # Scale duration
        wave = generate_sine_wave(frequency, duration)

        start_idx = int(current_time * SAMPLE_RATE)
        end_idx = start_idx + len(wave)

        if end_idx < len(audio_data):
            audio_data[start_idx:end_idx] += wave  # Add waveform to buffer

        current_time += duration

# Normalize and save as WAV file
audio_data = np.int16(audio_data / np.max(np.abs(audio_data)) * 32767)  # Convert to 16-bit PCM
wav_output_path = "output_s.wav"
write(wav_output_path, SAMPLE_RATE, audio_data)

print(f"WAV file saved: {wav_output_path}")

