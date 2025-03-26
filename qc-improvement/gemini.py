import base64
import os
from google import genai
from google.genai import types

sys = """
### **Instruction to AI:**

**Please act as an Expert QC (Quality Control) Engineer.** Your task is to generate structured test cases in a table format based on user stories and testing requirements. Ensure coverage across all testing types (Functional, Smoke, Performance, Security, System) as suitable for the user story. Follow the guidelines below to ensure clarity, consistency, and completeness.

---

### **1. Core Objectives**

- Generate test cases in a table format.
- Align test cases with user stories and ensure coverage across all testing types (Functional, Smoke, Performance, Security, System) as applicable.
- Use standardized templates for clarity and consistency.
- Include a **Priority** column to categorize test cases based on importance and execution priority.

---

### **2. Instruction Workflow**

#### **Step 1: Define the User Story**

- **Title**: Concise objective (e.g., "Validate email format").
- **Description**: Brief context (e.g., "System displays error for invalid emails").

#### **Step 2: Structure the Test Case**

- **ID**: Hierarchical format (e.g., `[AP-P4-01]` for Functional Testing).
- **Scenario Name**: Test objective (e.g., "Verify Email Validation").
- **Testing Type**: Select from:
  - Functional | Smoke | Performance | Security | System.
- **System**: Component tested (e.g., "Checkout Process").
- **Menu**: Application module (e.g., "Checkout").
- **Progress**: `Ready` / `Draft` / `In Progress`.
- **Priority**: Categorize as `High`, `Medium`, or `Low` based on importance (see **Priority Classification** below).
- **Steps to Execute**:
  - Numbered actions (e.g., "1. Open checkout page").
  - Include inputs (e.g., "Email: john.doecom").
- **Data Test**: Example data (e.g., invalid email).
- **Expected Result**: Outcome (e.g., "Error message displayed").

---

### **3. Testing Type Guidelines**

#### **Functional Testing**

- **Focus**: Validate specific features.
- **Example**:

  | **ID** | **Scenario Name** | **Testing Type** | **System** | **Menu** | **Progress** | **Priority** | **Steps to Execute** | **Data Test** | **Expected Result** |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | \[AP-P4-03\] | Verify Email Validation | Functional | Checkout Process | Checkout | Ready | High | 1\. Enter invalid email.  <br>2\. Click "Place Order". | Email: john.doecom | "Invalid email" error displayed. |

#### **Smoke Testing**

- **Focus**: Validate core functionality.
- **Example**:

  | **ID** | **Scenario Name** | **Testing Type** | **System** | **Menu** | **Progress** | **Priority** | **Steps to Execute** | **Data Test** | **Expected Result** |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | \[AP-P5-01\] | Verify Basic Functionality | Smoke | Checkout Process | Checkout | Ready | High | 1\. Enter valid data.  <br>2\. Submit order. | First Name: John  <br>Email: [john.doe@example.com](https://mailto:john.doe@example.com/) | Order confirmation displayed. |

#### **Performance Testing**

- **Focus**: System behavior under load.
- **Example**:

  | **ID** | **Scenario Name** | **Testing Type** | **System** | **Menu** | **Progress** | **Priority** | **Steps to Execute** | **Data Test** | **Expected Result** |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | \[AP-P6-01\] | Verify System Handling of Load | Performance | Checkout Process | Checkout | Ready | Medium | 1\. Simulate 100 users via JMeter. | N/A | No errors; response time <2s. |

#### **Security Testing**

- **Focus**: Vulnerability checks.
- **Example**:

  | **ID** | **Scenario Name** | **Testing Type** | **System** | **Menu** | **Progress** | **Priority** | **Steps to Execute** | **Data Test** | **Expected Result** |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | \[AP-P7-01\] | Verify SQL Injection Protection | Security | Checkout Process | Checkout | Ready | High | 1\. Inject `OR '1'='1` into email field.  <br>2\. Click "Place Order". | Email: `OR '1'='1` | System blocks input; "Invalid entry" displayed. |

#### **System Testing**

- **Focus**: End-to-end workflows.
- **Example**:

  | **ID** | **Scenario Name** | **Testing Type** | **System** | **Menu** | **Progress** | **Priority** | **Steps to Execute** | **Data Test** | **Expected Result** |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | \[AP-P8-01\] | Verify "Back" Button Navigation | System | Checkout Process | Checkout | Ready | Medium | 1\. Click "Back" button.  <br>2\. Click "Continue Shopping" in popup. | N/A | Redirect to shopping page. |

---

### **4. Priority Classification**

#### **High Priority**
- Directly affects the core functionality of the system.
- Features that are frequently used by users.
- Critical bugs that may cause system crashes.
- Issues impacting security and data integrity.

#### **Medium Priority**
- Affects important functionalities but does not cause system crashes.
- UI or behavior inconsistencies that are not severe.
- Frequently used features that have alternative solutions.

#### **Low Priority**
- Minor UI or aesthetic issues.
- Bugs that do not directly impact user experience.
- Features that are rarely used or have negligible impact on the system.

---

### **5. Rules & Validation**

- **ID Format**: Follow `[AP-PX-XX]` where `X` = testing phase (e.g., P4 = Functional).
- **Data Test**: Use realistic examples (e.g., valid/invalid emails).
- **Avoid Redundancy**: Merge overlapping test cases (e.g., "Back" button tests).
- **Status Tracking**: Default to `Ready` unless specified.
- **Priority**: Assign based on impact, frequency, severity, and urgency.
- **Ensure Coverage**: For each user story, generate test cases across all applicable testing types (Functional, Smoke, Performance, Security, System).

---

### **6. Example Output**

#### **User Story**:

- **Title**: Prevent SQL Injection.
- **Description**: Block malicious inputs in email field.

#### **Test Case Table**:

| **ID** | **Scenario Name** | **Testing Type** | **System** | **Menu** | **Progress** | **Priority** | **Steps to Execute** | **Data Test** | **Expected Result** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| \[AP-P7-01\] | Verify SQL Injection Protection | Security | Checkout Process | Checkout | Ready | High | 1\. Inject `OR '1'='1` into email field.  <br>2\. Click "Place Order". | Email: `OR '1'='1` | System blocks input; "Invalid entry" displayed. |
| \[AP-P4-02\] | Verify Email Validation | Functional | Checkout Process | Checkout | Ready | High | 1\. Enter invalid email.  <br>2\. Click "Place Order". | Email: john.doecom | "Invalid email" error displayed. |
| \[AP-P6-02\] | Verify System Handling of Load | Performance | Checkout Process | Checkout | Ready | Medium | 1\. Simulate 100 users via JMeter. | N/A | No errors; response time <2s. |
| \[AP-P5-02\] | Verify Basic Functionality | Smoke | Checkout Process | Checkout | Ready | High | 1\. Enter valid data.  <br>2\. Submit order. | First Name: John  <br>Email: [john.doe@example.com](https://mailto:john.doe@example.com/) | Order confirmation displayed. |
| \[AP-P8-02\] | Verify "Back" Button Navigation | System | Checkout Process | Checkout | Ready | Medium | 1\. Click "Back" button.  <br>2\. Click "Continue Shopping" in popup. | N/A | Redirect to shopping page. |

---

### **7. Additional Notes**

- **Comprehensive Coverage**: Ensure each user story is tested across all relevant testing types. For example:
  - Functional: Validate specific features.
  - Smoke: Ensure core functionality works.
  - Performance: Test under load/stress conditions.
  - Security: Check for vulnerabilities.
  - System: Validate end-to-end workflows.
- **Adaptability**: Tailor test cases to the specific context of the user story while maintaining consistency and completeness.
"""

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        system_instruction=sys,
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["response"],
            properties = {
                "response": genai.types.Schema(
                    type = genai.types.Type.OBJECT,
                    required = ["user_stories", "key_considerations"],
                    properties = {
                        "user_stories": genai.types.Schema(
                            type = genai.types.Type.ARRAY,
                            items = genai.types.Schema(
                                type = genai.types.Type.OBJECT,
                                required = ["title", "description", "test_cases"],
                                properties = {
                                    "title": genai.types.Schema(
                                        type = genai.types.Type.STRING,
                                    ),
                                    "description": genai.types.Schema(
                                        type = genai.types.Type.STRING,
                                    ),
                                    "test_cases": genai.types.Schema(
                                        type = genai.types.Type.ARRAY,
                                        items = genai.types.Schema(
                                            type = genai.types.Type.OBJECT,
                                            required = ["id", "scenario_name", "testing_type", "system", "menu", "progress", "priority", "steps_to_execute", "expected_result"],
                                            properties = {
                                                "id": genai.types.Schema(
                                                    type = genai.types.Type.STRING,
                                                ),
                                                "scenario_name": genai.types.Schema(
                                                    type = genai.types.Type.STRING,
                                                ),
                                                "testing_type": genai.types.Schema(
                                                    type = genai.types.Type.STRING,
                                                ),
                                                "system": genai.types.Schema(
                                                    type = genai.types.Type.STRING,
                                                ),
                                                "menu": genai.types.Schema(
                                                    type = genai.types.Type.STRING,
                                                ),
                                                "progress": genai.types.Schema(
                                                    type = genai.types.Type.STRING,
                                                ),
                                                "priority": genai.types.Schema(
                                                    type = genai.types.Type.STRING,
                                                ),
                                                "steps_to_execute": genai.types.Schema(
                                                    type = genai.types.Type.ARRAY,
                                                    items = genai.types.Schema(
                                                        type = genai.types.Type.STRING,
                                                    ),
                                                ),
                                                "data_test": genai.types.Schema(
                                                    type = genai.types.Type.OBJECT,
                                                    properties = {
                                                        "username": genai.types.Schema(
                                                            type = genai.types.Type.STRING,
                                                        ),
                                                        "password": genai.types.Schema(
                                                            type = genai.types.Type.STRING,
                                                        ),
                                                        "mobile_email": genai.types.Schema(
                                                            type = genai.types.Type.STRING,
                                                        ),
                                                        "otp": genai.types.Schema(
                                                            type = genai.types.Type.STRING,
                                                        ),
                                                    },
                                                ),
                                                "expected_result": genai.types.Schema(
                                                    type = genai.types.Type.STRING,
                                                ),
                                            },
                                        ),
                                    ),
                                },
                            ),
                        ),
                        "key_considerations": genai.types.Schema(
                            type = genai.types.Type.ARRAY,
                            items = genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        ),
                    },
                ),
            },
        ),
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
