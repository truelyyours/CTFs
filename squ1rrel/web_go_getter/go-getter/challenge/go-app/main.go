package main

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
)

// Struct to parse incoming JSON
type RequestData struct {
	Action string `json:"action"`
}

// Serve the HTML page
func homeHandler(w http.ResponseWriter, r *http.Request) {
	html := `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>What GOpher are you?</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script>
        function sendRequest() {
            const selectedOption = document.querySelector('input[name="action"]:checked');
            if (!selectedOption) {
                alert("Please select an action!");
                return;
            }

            fetch("/execute", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: selectedOption.value })
            })
            .then(response => response.text().then(text => ({ text, response })))
            .then(({ text, response }) => {
                var gopherContainer = document.getElementById("gopher-container");
                var errorContainer = document.getElementById("error-container");
                gopherContainer.innerHTML = "";
                errorContainer.innerHTML = "";
                
                try {
                    var data = JSON.parse(text);
                    if (data.flag) {
                        alert(data.flag);
                    } else if (data.name && data.src) {
                        var nameHeader = document.createElement("h3");
                        nameHeader.textContent = data.name;
                        var gopherImage = document.createElement("img");
                        gopherImage.src = data.src;
                        gopherImage.className = "img-fluid rounded";
                        gopherContainer.appendChild(nameHeader);
                        gopherContainer.appendChild(gopherImage);
                    }
                } catch (error) {
                    errorContainer.textContent = "Error: " + text;
                    errorContainer.className = "text-danger mt-3";
                }
            })
            .catch(function(error) {
                console.error("Error:", error);
            });
        }
    </script>
</head>
<body class="container py-5 text-center">
    <h1 class="mb-4">Choose an Action</h1>
    <div class="d-flex flex-column align-items-center mb-3">
        <div class="form-check">
            <input class="form-check-input" type="radio" name="action" value="getgopher" id="getgopher">
            <label class="form-check-label" for="getgopher">Get GOpher</label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" name="action" value="getflag" id="getflag">
            <label class="form-check-label" for="getflag">I don't care about gophers, I want the flag >:)</label>
        </div>
    </div>
    <button class="btn btn-primary" onclick="sendRequest()">Submit</button>
    <div id="error-container"></div>
    <div id="gopher-container" class="mt-4"></div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>`
	w.Header().Set("Content-Type", "text/html")
	w.Write([]byte(html))
}

// Handler for executing actions
func executeHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	// Read JSON body
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Failed to read request body", http.StatusBadRequest)
		return
	}

	// Parse JSON
	var requestData RequestData
	if err := json.Unmarshal(body, &requestData); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	// Process action
	switch requestData.Action {
	case "getgopher":
		resp, err := http.Post("http://python-service:8081/execute", "application/json", bytes.NewBuffer(body))
		if err != nil {
			log.Printf("Failed to reach Python API: %v", err)
			http.Error(w, "Failed to reach Python API", http.StatusInternalServerError)
			return
		}
		defer resp.Body.Close()

		// Forward response from Python API back to the client
		responseBody, _ := io.ReadAll(resp.Body)
		w.WriteHeader(resp.StatusCode)
		w.Write(responseBody)
	case "getflag":
		w.Write([]byte("Access denied: You are not an admin."))
	default:
		http.Error(w, "Invalid action", http.StatusBadRequest)
	}
}

func main() {
	http.HandleFunc("/", homeHandler)
	http.HandleFunc("/execute", executeHandler)

	log.Println("Server running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
