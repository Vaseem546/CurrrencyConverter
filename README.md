# 💱 Currency Converter

A modern, beginner-friendly web application for real-time currency conversion built with Python and Streamlit.

## 🌟 Features

- **Real-time Exchange Rates**: Live currency conversion using free API
- **20+ Currencies**: Support for major global currencies with country flags
- **Clean UI**: Modern, responsive design for desktop and mobile devices
- **Swap Currencies**: Quick button to swap "From" and "To" currencies
- **Conversion History**: Track your recent conversions in the sidebar
- **Error Handling**: Graceful error messages and validation
- **Loading Indicators**: Visual feedback while fetching data
- **Exchange Rate Display**: Shows the exact rate used for conversion
- **Timestamp**: Displays when rates were last updated
- **Currency Symbols**: Shows proper currency symbols in results

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd CurrencyConverter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📋 How to Use

1. **Select Currencies**: Choose your source currency in the left dropdown and target currency in the right dropdown
2. **Enter Amount**: Type the amount you want to convert
3. **Swap (Optional)**: Click the swap button to reverse the conversion direction
4. **Convert**: Click the "Convert" button to see the result
5. **View History**: Check your recent conversions in the left sidebar
6. **Clear History**: Click "Clear History" to reset the conversion history

## 🏗️ Project Structure

```
CurrencyConverter/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 💻 Code Overview

### Main Components

#### 1. **Page Configuration**
- Sets up Streamlit page layout and title
- Configures custom CSS for styling

#### 2. **API Functions**
- `fetch_exchange_rates()`: Fetches live rates from exchangerate-api.com
- `convert_currency()`: Performs the currency conversion
- `add_to_history()`: Tracks conversion history

#### 3. **UI Components**
- `render_header()`: Application title and subtitle
- `render_converter()`: Main converter interface with dropdowns and input
- `render_result()`: Beautiful result display
- `render_history()`: Sidebar history widget
- `render_footer()`: Footer with credits

#### 4. **Error Handling**
- Timeout handling
- Connection error handling
- API error handling
- Input validation
- User-friendly error messages

### Session State Management

The app uses Streamlit's `session_state` to maintain:
- Conversion history across interactions
- Cached API responses
- Last update timestamp

### Caching

- Exchange rates are cached for 1 hour using `@st.cache_data` to minimize API calls
- Reduces server load and improves performance

## 🌐 Supported Currencies

- USD (US Dollar)
- EUR (Euro)
- GBP (British Pound)
- JPY (Japanese Yen)
- AUD (Australian Dollar)
- CAD (Canadian Dollar)
- CHF (Swiss Franc)
- CNY (Chinese Yuan)
- INR (Indian Rupee)
- MXN (Mexican Peso)
- BRL (Brazilian Real)
- ZAR (South African Rand)
- SGD (Singapore Dollar)
- HKD (Hong Kong Dollar)
- NOK (Norwegian Krone)
- SEK (Swedish Krona)
- NZD (New Zealand Dollar)
- MYR (Malaysian Ringgit)
- PHP (Philippine Peso)
- THB (Thai Baht)

## 🔧 Technical Details

### API Used
- **exchangerate-api.com**: Free, reliable currency exchange API
- No authentication required
- 1500 requests per month on free tier

### Dependencies
- **Streamlit**: Web framework for creating interactive applications
- **Requests**: HTTP library for API calls

### Performance Optimizations
- Data caching reduces unnecessary API calls
- Session state prevents data loss during interactions
- Efficient UI rendering with Streamlit columns

## 🎨 Customization

### Add More Currencies
Edit the `SUPPORTED_CURRENCIES` dictionary in `app.py`:
```python
SUPPORTED_CURRENCIES = {
    "USD": "🇺🇸 US Dollar",
    "EUR": "🇪🇺 Euro",
    # Add more here
}
```

### Add Currency Symbols
Edit the `CURRENCY_SYMBOLS` dictionary:
```python
CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    # Add more here
}
```

### Modify Styling
Update the CSS in the `st.markdown()` call in the `STYLING & THEME` section.

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Run `pip install -r requirements.txt`

### "Failed to get local version of pip"
**Solution**: Update pip: `python -m pip install --upgrade pip`

### API not responding
**Solution**: 
- Check your internet connection
- The free tier has a 1500 request/month limit
- Wait a moment and try again

### App not opening in browser
**Solution**: 
- Check the terminal output for the URL (usually http://localhost:8501)
- Copy and paste it into your browser manually

## 📝 Code Comments Explained

The code is heavily commented to help beginners understand each section:

- `# ============================================================================` marks major sections
- Comments above functions explain what they do
- Inline comments clarify complex logic
- Type hints show expected data types

## 🎓 Learning Outcomes

By studying this code, you'll learn:
- Streamlit basics and widgets
- API integration and JSON parsing
- Error handling best practices
- Session state management
- Responsive UI design
- CSS styling in Streamlit
- Function organization
- Python best practices

## 📄 License

This project is open source and available for educational use.

## 🤝 Contributing

Feel free to:
- Add more currencies
- Improve the UI
- Optimize performance
- Add new features

## 💡 Future Enhancement Ideas

- Add cryptocurrency conversion
- Implement historical rate charts
- Add favorite currency pairs
- Export conversion history as CSV
- Add conversion fee calculations
- Support for offline mode with cached rates

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review the code comments
3. Check Streamlit documentation: https://docs.streamlit.io
4. Check exchangerate-api.com documentation

---

**Built with ❤️ using Python + Streamlit + Free Currency Exchange API**

Happy converting! 💰
