import pandas as pd

# Example test cases data
test_cases = [
    {
        "expected_result": "User is successfully logged in, and redirected to the dashboard.",
        "id": "AP-P4-01",
        "steps_to_execute": [
            "1. Navigate to the login page.",
            "2. Enter valid username in the username field.",
            "3. Enter valid password in the password field.",
            "4. Click the 'Login' button."
        ],
        "menu": "Login",
        "progress": "Ready",
        "priority": "High",
        "system": "Authentication",
        "scenario_name": "Verify Successful Login",
        "testing_type": "Functional"
    }
]

# Convert to DataFrame
df = pd.DataFrame(test_cases)

# Convert list to string for better visualization
df["steps_to_execute"] = df["steps_to_execute"].apply(lambda x: "\n".join(x))

# Display DataFrame
print(df)
