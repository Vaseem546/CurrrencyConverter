# 🚀 Currency Converter - Setup Instructions

Follow these steps to get your Currency Converter application running!

## Step 1: Prerequisites Check

Make sure you have **Python 3.7 or higher** installed.

Check your Python version:
```bash
python --version
```

If Python is not installed, download it from: https://www.python.org/downloads/

## Step 2: Navigate to Project Directory

Open your terminal/command prompt and navigate to the project folder:

```bash
cd CurrencyConverter
```

## Step 3: Create Virtual Environment (Optional but Recommended)

Creating a virtual environment keeps your dependencies isolated:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

## Step 4: Install Dependencies

Install all required packages using pip:

```bash
pip install -r requirements.txt
```

This will install:
- **Streamlit** (web framework)
- **Requests** (for API calls)

## Step 5: Run the Application

Start the Currency Converter:

```bash
streamlit run app.py
```

### Expected Output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

## Step 6: Open in Browser

1. Your browser should open automatically
2. If not, manually open: http://localhost:8501

## ✅ You're Ready!

The application is now running! Start converting currencies with live exchange rates.

## 📦 What Gets Installed

| Package | Version | Purpose |
|---------|---------|---------|
| Streamlit | 1.32.2 | Web framework for interactive UI |
| Requests | 2.31.0 | HTTP library for API calls |

## 🛠️ Troubleshooting

### Issue: "Command not found: streamlit"
**Fix**: Make sure dependencies are installed: `pip install -r requirements.txt`

### Issue: Port 8501 is already in use
**Fix**: Run on a different port: `streamlit run app.py --server.port 8502`

### Issue: "ModuleNotFoundError"
**Fix**: Verify virtual environment is activated or reinstall: `pip install --force-reinstall -r requirements.txt`

### Issue: API timeout or no response
**Fix**: 
- Check internet connection
- Try again after a moment
- The free API has rate limits

## 🎮 Features to Try

1. **Convert Currencies**: Select currencies and enter an amount
2. **Swap Currencies**: Click the swap button to reverse direction
3. **View History**: Check the sidebar for your recent conversions
4. **Clear History**: Reset all previous conversions
5. **Live Updates**: See the exact exchange rate and update time

## 📱 Responsive Design

The app works great on:
- ✅ Desktop browsers
- ✅ Tablets
- ✅ Mobile phones

Just open http://localhost:8501 on any device!

## 🌐 Supported Currencies

20+ currencies including:
- 🇺🇸 USD (US Dollar)
- 🇪🇺 EUR (Euro)
- 🇬🇧 GBP (British Pound)
- 🇯🇵 JPY (Japanese Yen)
- 🇦🇺 AUD (Australian Dollar)
- 🇨🇦 CAD (Canadian Dollar)
- 🇮🇳 INR (Indian Rupee)
- And 13 more!

## 🚫 To Stop the Application

Press `Ctrl+C` in your terminal to stop the Streamlit server.

## 💾 Deactivate Virtual Environment (When Done)

If you used a virtual environment, deactivate it when finished:

```bash
deactivate
```

## 📚 Next Steps

- Explore the code in `app.py` to understand how it works
- Read the `README.md` for detailed documentation
- Try customizing the currencies or styling
- Add this to your portfolio!

## 🎓 Learning Resources

- Streamlit Docs: https://docs.streamlit.io
- Requests Library: https://docs.python-requests.org
- ExchangeRate API: https://exchangerate-api.com

---

**Enjoy your Currency Converter! Happy converting! 💰**
