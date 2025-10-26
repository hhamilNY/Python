# 🔧 Fix Syntax Error in Codespace

## ❌ **Current Error:**
```
SyntaxError: positional argument follows keyword argument
```

This means the histogram function call has mixed positional and keyword arguments incorrectly.

---

## 🛠️ **Fix Commands for Codespace:**

### **Step 1: Edit the file directly**
```bash
nano mobile_earthquake_app.py
```

### **Step 2: Find the create_magnitude_chart function (around line 278)**
Look for this section and replace it:

**Replace this broken code:**
```python
fig = px.histogram(x=magnitudes, bins=15, ...)
```

**With this correct code:**
```python
fig = px.histogram(
    x=magnitudes,
    nbins=15,
    title="📊 Magnitude Distribution",
    labels={'x': 'Magnitude', 'y': 'Count'},
    height=300
)
```

---

## 🚀 **Quick Fix with sed command:**

```bash
# Create a temporary fix file
cat > temp_fix.py << 'EOF'
def create_magnitude_chart(earthquakes):
    """Create mobile-friendly magnitude distribution chart"""
    if not earthquakes:
        return
    
    valid_earthquakes = [eq for eq in earthquakes if eq['magnitude'] > 0]
    magnitudes = [eq['magnitude'] for eq in valid_earthquakes]
    
    if not magnitudes:
        return
    
    # Add proper spacing
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    fig = px.histogram(
        x=magnitudes,
        nbins=15,
        title="📊 Magnitude Distribution",
        labels={'x': 'Magnitude', 'y': 'Count'},
        height=300
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        font=dict(size=12),
        title_font_size=14
    )
    
    st.plotly_chart(fig, use_container_width=True)
EOF

# Replace the function in the main file (this is more complex, so use manual edit)
```

---

## 📝 **Manual Edit Steps (Recommended):**

1. **Open file:**
   ```bash
   nano mobile_earthquake_app.py
   ```

2. **Press Ctrl+W** and search for: `create_magnitude_chart`

3. **Find the histogram line** (around line 278)

4. **Replace the entire histogram call with:**
   ```python
   fig = px.histogram(
       x=magnitudes,
       nbins=15,
       title="📊 Magnitude Distribution",
       labels={'x': 'Magnitude', 'y': 'Count'},
       height=300
   )
   ```

5. **Save:** `Ctrl+O`, `Enter`, `Ctrl+X`

---

## 🚀 **After Fixing:**

```bash
# Restart streamlit
pkill streamlit
streamlit run mobile_earthquake_app.py --server.port=8501
```

**The key fix is changing `bins=15` to `nbins=15` and ensuring proper formatting!** 🔧