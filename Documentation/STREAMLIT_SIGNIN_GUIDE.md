# 🔐 Streamlit Cloud Sign-In Guide

## 📋 **Step-by-Step Sign-In Process:**

### **Step 1: Go to Streamlit Cloud**
1. Open your browser
2. Go to: **[share.streamlit.io](https://share.streamlit.io)**
3. You'll see the sign-in page

### **Step 2: Sign In with GitHub**
1. **Click "Sign in with GitHub"** (big blue button)
2. **Enter your GitHub credentials:**
   - Username: `hhamilNY` (or your GitHub username)
   - Password: (your GitHub password)
3. **Authorize Streamlit** (if prompted)
   - Click "Authorize streamlit" to give permission

### **Step 3: First-Time Setup**
After signing in, you might need to:
1. **Verify your email** (if prompted)
2. **Accept terms of service**
3. **Complete profile setup**

---

## 🚀 **Deploy Your App (After Sign-In):**

### **Once You're Signed In:**
1. **Click "New app"** (or "Create app")
2. **Fill out the form:**
   - **Repository:** `hhamilNY/Python`
   - **Branch:** `main`
   - **Main file path:** `mobile_earthquake_app.py`
   - **App URL:** Choose a name like `earthquake-monitor`
3. **Click "Deploy!"**

### **Deployment Process:**
- ⏳ **Installing dependencies** (1-2 minutes)
- ⏳ **Starting app** (30 seconds)
- ✅ **App ready** (you'll get a public URL)

---

## 🎯 **What You'll Get:**

After successful deployment:
- **Public URL** like: `https://earthquake-monitor-abc123.streamlit.app`
- **24/7 hosting** on Streamlit's servers
- **Global access** from anywhere in the world

---

## 🔧 **Troubleshooting Sign-In Issues:**

### **Can't Remember GitHub Password?**
1. Go to [github.com/login](https://github.com/login)
2. Click "Forgot password?"
3. Reset via email

### **Don't Have GitHub Account?**
1. Go to [github.com/signup](https://github.com/signup)
2. Create account with same email
3. Upload your files to new repository
4. Then sign into Streamlit Cloud

### **Authorization Issues?**
1. Make sure you're signed into GitHub first
2. Try signing out of GitHub and back in
3. Clear browser cache/cookies
4. Try incognito/private browser window

---

## 📱 **Alternative: GitHub Codespaces (No Streamlit Account Needed)**

If sign-in issues persist:

1. **Go to:** https://github.com/hhamilNY/Python
2. **Click "Code"** → **"Codespaces"** → **"Create codespace"**
3. **In terminal run:**
   ```bash
   pip install streamlit plotly pandas requests
   streamlit run mobile_earthquake_app.py --server.port=8501
   ```
4. **Click "Make Public"** when port forwarding appears
5. **Share the public URL** with your friend

This gives you a temporary public URL without needing Streamlit Cloud account!

---

## ✅ **Next Steps:**

1. **Sign in to Streamlit Cloud** with GitHub
2. **Deploy your earthquake app**
3. **Get your public URL**
4. **Share with your friend**

The sign-in is just a one-time setup - after this, your app will be permanently hosted! 🌍🚀