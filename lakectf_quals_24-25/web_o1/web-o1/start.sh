#!/bin/bash

# Start the first Flask proxy on port 9222
python app1.py &

# Start the second Flask proxy on port 1111
python app2.py &

# Start the Express proxy on port 3000
node app3.js &

# Wait indefinitely to keep the container running
wait
