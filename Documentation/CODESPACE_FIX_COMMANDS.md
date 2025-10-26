# 🔧 Fix the mobile_earthquake_app.py in Your Codespace

## 📝 **Quick Fix Command:**

In your GitHub Codespace terminal, run this command to fix the error:

```bash
sed -i 's/bins=15/nbins=15/g' mobile_earthquake_app.py
```

This will automatically change `bins=15` to `nbins=15` in your file.

---

## 🔍 **Manual Edit Method (Alternative):**

If you prefer to edit manually:

### **Step 1: Open the file**
```bash
nano mobile_earthquake_app.py
```

### **Step 2: Find line 278**
Press `Ctrl + W` and search for: `bins=15`

### **Step 3: Change it to:**
```python
nbins=15
```

### **Step 4: Save and exit**
- Press `Ctrl + O` (save)
- Press `Enter` (confirm)
- Press `Ctrl + X` (exit)

---

## 🚀 **After Making the Change:**

### **Restart Streamlit:**
```bash
# Kill current process
pkill streamlit

# Start with fixed code
streamlit run mobile_earthquake_app.py --server.port=8501
```

### **Make Port Public Again:**
Click "Make Public" when the port forwarding notification appears.

---

## ✅ **Verification:**

After the fix, your earthquake monitor should work perfectly:
- ✅ No more `TypeError` about bins
- ✅ Statistics view works properly
- ✅ All features functional

---

## 📋 **Complete Fix Commands (Copy/Paste):**

```bash
# Fix the file
sed -i 's/bins=15/nbins=15/g' mobile_earthquake_app.py

# Restart streamlit
pkill streamlit
streamlit run mobile_earthquake_app.py --server.port=8501
```

Your public URL will remain the same: 
`https://damp-orb-69wxgvqxxw6gf5g79-8501.app.github.dev/`

Run these commands in your Codespace terminal! 🚀