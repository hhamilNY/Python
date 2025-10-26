# 🛑 How to Kill Streamlit Process in GitHub Codespace

## ⚡ **Quick Methods to Stop Streamlit:**

### **Method 1: Keyboard Shortcut (Easiest)**
In the terminal where Streamlit is running:
```bash
Ctrl + C
```
This should immediately stop the Streamlit process.

---

### **Method 2: Find and Kill Process by Port**
```bash
# Find what's using port 8501
lsof -i :8501

# Kill the process (replace PID with actual process ID)
kill -9 <PID>
```

Example:
```bash
# Find the process
lsof -i :8501
# Output might show: python 1234 codespace ... :8501
# Then kill it:
kill -9 1234
```

---

### **Method 3: Kill All Python Processes**
```bash
# Kill all python processes (nuclear option)
pkill -f python

# Or more specific to streamlit
pkill -f streamlit
```

---

### **Method 4: Kill by Process Name**
```bash
# Find streamlit processes
ps aux | grep streamlit

# Kill streamlit specifically
pkill streamlit
```

---

### **Method 5: Use Different Port (Alternative)**
If killing doesn't work, just use a different port:
```bash
streamlit run mobile_earthquake_app.py --server.port=8502
```

---

## 🔧 **Step-by-Step Fix Process:**

### **Step 1: Kill Current Process**
```bash
Ctrl + C
# or
pkill streamlit
```

### **Step 2: Edit the File**
```bash
nano mobile_earthquake_app.py
```
Change line 278: `bins=15` → `nbins=15`

### **Step 3: Restart Streamlit**
```bash
streamlit run mobile_earthquake_app.py --server.port=8501
```

### **Step 4: Make Port Public Again**
Click "Make Public" when the port forwarding notification appears.

---

## 🚀 **Quick Commands (Copy/Paste):**

```bash
# Stop streamlit
pkill streamlit

# Edit the file (fix bins → nbins)
nano mobile_earthquake_app.py

# Restart with fixed code
streamlit run mobile_earthquake_app.py --server.port=8501
```

---

## 🎯 **Expected Result:**

After fixing and restarting:
- ✅ No more `TypeError: unexpected keyword argument 'bins'`
- ✅ Statistics view will work properly
- ✅ Your earthquake monitor runs perfectly
- ✅ Same public URL continues to work

---

## 💡 **Pro Tip:**

In Codespaces, you can also:
1. **Open new terminal tab** (+ button)
2. **Keep old one for monitoring**
3. **Use new one for commands**

This way you can always see what's running where! 🖥️