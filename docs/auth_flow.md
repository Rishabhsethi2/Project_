URL: https://api.dhan.co
Authentication Endpoint: /app/generateAccessToken
HTTP Method: POST
Header Keys:
    clientid: 1111283919
    pin: 100207
    TOTP: 
JSON format:
    What we send:
    What we recieve:

# Dhan API Authentication Handshake

# 1. The Target
* **Base URL:** [What is the main URL for the Dhan API? e.g., https://api.dhan.co]
* **Auth Endpoint:** [What is the specific path for logging in? e.g., /v2/session]
* **HTTP Method:** [Is it a GET or a POST request?]

# 2. The Required Headers
To prove who we are, we must send these headers with every request:
* `client-id`: [Where do we get this?]
* `access-token`: [Where do we get this? Does it expire?]

# 3. The JSON Payload (If applicable)
* **What we send:** [If it's a POST request, what JSON dictionary do we have to send them?]
* **What they return:** [When it succeeds, what does the JSON response look like? Paste an example.]