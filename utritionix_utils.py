# Hardcode your credentials temporarily (REMOVE AFTER TESTING!)
APP_ID = "1a211f0b"
API_KEY = "db523a76dc7bdfa08646051c87726b68"

# Make the API call with hardcoded values
response = requests.post(
    "https://trackapi.nutritionix.com/v2/natural/nutrients",
    headers={
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    },
    json={"query": "apple"},
    timeout=10
)
st.write(response.status_code, response.text)