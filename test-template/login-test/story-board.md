# **Web UI Widget Captioning – Login UI**  

This section describes the detailed elements of the **Lotte Mart Login UI**, covering both **account-based login** and **OTP login** options.  

---

## **1. Header Section**  

### **1-1 Lotte Mart Logo (Top Left)**  
- The official Lotte Mart logo functions as a **navigational element**, typically linking to the homepage.  

### **1-2 Language/Region Selector (Top Right)**  
- A dropdown menu allowing users to **select their preferred language or region**.  
- The selected flag represents the **current language/region setting** (e.g., Vietnamese).  

---

## **2. Login Form Section**  

The login UI provides **two login methods**, accessible via **tab navigation**:  

### **2-1 [Tài Khoản] Tab (Account Login)**  
- The default tab selected for **email or phone number login with a password**.  

### **2-2 [Bằng OTP] Tab (OTP Login)**  
- The alternative login tab that allows users to **log in using a One-Time Password (OTP)**.  
- Switching to this tab updates the form to display OTP-related fields.  

---

## **3. Account Login Components** *(Displayed when "Tài Khoản" Tab is Selected)*  

### **3-1 Email/Phone Number Input Field**  
- A required text field labeled **"Email/Số điện thoại*"** where users enter their registered email or phone number.  
- The asterisk (*) indicates that this is a **mandatory field**.  

### **3-2 Password Input Field**  
- A required password field labeled **"Mật khẩu*"** for entering the user's password.  
- **Lock icon** present to indicate **secure input**.  

### **3-3 Show/Hide Password Icon (Eye Icon)**  
- A **toggle button** within the password field to **show or hide** the entered password.  

### **3-4 [Quên mật khẩu?] Link ("Forgot Password?")**  
- A clickable text link directing users to the **password recovery page**.  

### **3-5 [Đăng nhập] Button ("Login")**  
- The **primary call-to-action button** that submits the login form.  

---

## **4. OTP Login Components** *(Displayed when "Bằng OTP" Tab is Selected)*  

### **4-1 Email/Phone Number Input Field**  
- A required text field labeled **"Email/Số điện thoại*"** for users to enter their registered contact information.  

### **4-2 OTP Instructions Text**  
- **Guidance message** for OTP retrieval, including:  
  - "If you are using **VinaPhone**, please select Email to receive the OTP verification code."  
  - "You can use the **Phone number/Email registered at SPEED L** to log in."  

### **4-3 [Gửi mã OTP] Button ("Send OTP")**  
- The **primary action button** that sends a one-time password to the user's email or phone number.  

---

## **5. Alternative Login Methods (Social Login Section)**  

### **5-1 Social Login Title ("Hoặc đăng nhập với")**  
- A section that introduces **alternative login options** using social media accounts.  

### **5-2 Social Login Buttons** *(Displayed Below Login Form)*  
Users can log in using:  
- **Zalo** *(Zalo logo button)*  
- **Google** *(Google logo button)*  
- **Kakao Talk** *(Kakao Talk logo button)*  
- **Apple ID** *(Apple logo button)*  

---

## **6. Registration Section**  

### **6-1 [Đăng ký] Link ("Register")**  
- A text link labeled **"Quý khách chưa có tài khoản? Đăng ký"** *(“Don't have an account? Register”)*.  
- Redirects users to the **account registration page**.  

---

## **7. Overall Web UI Interaction Summary**  

- **User Journey:**  
  - The login UI provides a **clear, structured experience**, allowing users to log in via **email/password, OTP, or social login**.  
  - Switching between **account login and OTP login** is handled via **tab navigation**.  

- **Usability Factors:**  
  - **Clear labels, intuitive input fields, and call-to-action buttons** improve ease of use.  
  - The **social login section** offers alternative authentication options.  

- **Accessibility Considerations:**  
  - **Keyboard navigation** should be supported for **input fields, buttons, and tab selection**.  
  - **Screen reader compatibility** for form labels, placeholders, and error messages enhances inclusivity.  

- **Potential UX Improvements:**  
  - Adding **real-time validation** for incorrect email formats or invalid phone numbers.  
  - Providing **feedback messages** (e.g., "OTP sent successfully") when users request an OTP.  
  - Implementing **visual indicators** (e.g., active tab highlights) for better navigation clarity.  

This structured breakdown ensures a **seamless and user-friendly login experience** while maintaining **accessibility and usability best practices**. 🚀  
