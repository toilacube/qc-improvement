# LOTTE MART Login Page - Detailed Requirements Document

## Overview
This document outlines the detailed requirements for the LOTTE MART login page. The interface allows users to authenticate using various methods including traditional account login with email/phone and password, OTP, and third-party login options.

## Page Components and Functionality

**No.** | **Zone** | **Field** | **Detail Description**
--------|----------|-----------|----------------------
1 | Header | LOTTE MART Logo | **Field type**: Image<br>**Position**: Top Left<br>**Functionality**: Serves as a visual identifier for the brand<br>**Action**: Redirects user to the homepage when clicked
2 | Header | Language Selection Dropdown | **Field type**: Single select dropdown<br>**Position**: Top Right<br>**Default display**: Flag icon of currently selected language<br>**Functionality**: Allows users to change the website's display language
3 | Main Content | Login Form Container | **Field type**: Container (div)<br>**Position**: Center Right<br>**Style**: White background with appropriate padding and shadow
4 | Login Form | Login Method Tabs | **Field type**: Tab group<br>**Position**: Inside Login Form, Top<br>**Tab options**:<br>- "Tài Khoản" (Account)<br>- "Bằng OTP" (OTP)<br>**Functionality**: Toggles between login methods
5 | Login Form<br>(Account Tab) | Email/Phone Input Field | **Field type**: Text input<br>**Position**: Inside Login Form<br>**Validation**: Required field<br>**Placeholder text**: "Email address or phone number"<br>**Validation rules**: Must be valid email format or phone number format
6 | Login Form<br>(Account Tab) | Password Input Field | **Field type**: Password input<br>**Position**: Inside Login Form, below Email/Phone field<br>**Validation**: Required field<br>**Features**: Toggle button to show/hide password text<br>**Placeholder text**: "Password"<br>**Validation rules**: Must have at least 8 characters
7 | Login Form<br>(Account Tab) | Forgot Password Link | **Field type**: Hyperlink<br>**Position**: Inside Login Form, below Password field<br>**Text**: "Forgot Password?"<br>**Action**: Redirects to password recovery page
8 | Login Form<br>(Account Tab) | Login Button | **Field type**: Button (Primary)<br>**Position**: Inside Login Form, below Forgot Password link<br>**Text**: "Login"<br>**Action**: Submits credentials to authentication API
9 | Login Form | Login with Zalo Button | **Field type**: Button (Secondary)<br>**Position**: Inside Login Form, Social Login section<br>**Text**: "Login with Zalo"<br>**Icon**: Zalo logo<br>**Action**: Initiates OAuth flow with Zalo
10 | Login Form | Login with Google Button | **Field type**: Button (Secondary)<br>**Position**: Inside Login Form, Social Login section<br>**Text**: "Login with Google"<br>**Icon**: Google logo<br>**Action**: Initiates OAuth flow with Google
11 | Login Form | Login with Kakao Talk Button | **Field type**: Button (Secondary)<br>**Position**: Inside Login Form, Social Login section<br>**Text**: "Login with Kakao Talk"<br>**Icon**: Kakao Talk logo<br>**Action**: Initiates OAuth flow with Kakao Talk
12 | Login Form | Login with Apple ID Button | **Field type**: Button (Secondary)<br>**Position**: Inside Login Form, Social Login section<br>**Text**: "Login with Apple ID"<br>**Icon**: Apple logo<br>**Action**: Initiates OAuth flow with Apple
13 | Login Form<br>(OTP Tab) | Phone Number Input | **Field type**: Text input<br>**Position**: Inside Login Form, OTP tab<br>**Validation**: Required field<br>**Placeholder text**: "Phone Number"<br>**Validation rules**: Must be valid phone number format
14 | Login Form<br>(OTP Tab) | Send OTP Button | **Field type**: Button<br>**Position**: Inside Login Form, OTP tab<br>**Text**: "Send OTP"<br>**Action**: Sends OTP to provided phone number
15 | Login Form<br>(OTP Tab) | OTP Input Field | **Field type**: Text input or segmented OTP input<br>**Position**: Inside Login Form, OTP tab<br>**Validation**: Required field<br>**Placeholder text**: "Enter OTP"<br>**Validation rules**: Must be numeric, correct length
16 | Login Form<br>(OTP Tab) | OTP Timer Display | **Field type**: Text display<br>**Position**: Inside Login Form, OTP tab, near OTP field<br>**Functionality**: Displays countdown timer showing remaining validity time for OTP<br>**Initial value**: "03:00" (3 minutes)<br>**Behavior**: Counts down second by second<br>**Expiry action**: Displays "OTP Expired" message and enables "Resend OTP" option
17 | Login Form<br>(OTP Tab) | Verify OTP Button | **Field type**: Button (Primary)<br>**Position**: Inside Login Form, OTP tab<br>**Text**: "Verify & Login"<br>**Action**: Verifies OTP and logs user in
18 | Login Form | Register Link | **Field type**: Hyperlink<br>**Position**: Inside Login Form, Bottom<br>**Text**: "Don't have an account? Register"<br>**Action**: Redirects to the registration page

## Error Handling and Validation

### Field Validation
1. **Email/Phone Field**:
   - Cannot be empty
   - Must match email format (user@domain.com) or phone format depending on input
   - Error message displays beneath field upon validation failure

2. **Password Field**:
   - Cannot be empty
   - Must have at least 8 characters
   - Error message displays beneath field upon validation failure
   - Error message should be specific: "Password must be at least 8 characters long"

3. **OTP Field**:
   - Cannot be empty
   - Must be numeric
   - Must match expected length (typically 6 digits)
   - Error message displays beneath field upon validation failure
   - OTP is valid for 3 minutes (180 seconds) from time of issue

### API Error Handling
- Invalid credentials: Display appropriate error message above login form
- Account locked: Display message with account recovery options
- Service unavailable: Display system error message with retry option
- Network timeout: Display connection error with retry option
- OTP expired: Display "OTP has expired. Please request a new one" message

## UI/UX Requirements

### Responsive Design
- Login form maintains proper layout across desktop, tablet, and mobile screen sizes
- Minimum width: 320px (mobile)
- Maximum width: 480px (form container)

### Accessibility
- All form fields have proper labels and ARIA attributes
- Tab order follows logical sequence
- Color contrast meets WCAG AA standards
- Error messages are screen-reader friendly

### Security Features
- Password field masking with visibility toggle
- Automatic session timeout after period of inactivity
- CAPTCHA integration for repeated failed login attempts (optional requirement)
- Secure connection (HTTPS) required
- OTP expires after 3 minutes for security purposes

## OTP Functionality
- OTP is sent to user's phone number via SMS
- OTP is valid for exactly 3 minutes (180 seconds)
- A countdown timer displays remaining validity time
- User must receive, enter, and submit the OTP within the 3-minute window
- After expiration, user must request a new OTP
- System should enforce OTP expiration on both client and server side

## Localization
- Support for multiple languages through language selector
- Default language detection based on browser settings
- Text elements should be stored in language resource files for easy translation

## Revision History
- Initial document creation: April 1, 2025
- Updated with OTP expiration time and password requirements: April 1, 2025