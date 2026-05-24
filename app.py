"""
Currency Converter Application
A modern web app for real-time currency conversion using Streamlit
Built with: Python + Streamlit + Free Currency Exchange API
"""

import streamlit as st
import requests
from datetime import datetime
import json
from typing import Optional, Dict, Tuple

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Currency Converter",
    page_icon="💱",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================================
# STYLING & THEME
# ============================================================================
def get_theme_css(dark_mode: bool) -> str:
    """
    Generate CSS based on the current theme (light or dark mode).
    
    Args:
        dark_mode: Boolean indicating if dark mode is enabled
    
    Returns:
        CSS string with theme-appropriate styling
    """
    if dark_mode:
        # Dark mode colors
        bg_color = "#1e1e1e"
        text_color = "#e0e0e0"
        card_bg = "rgba(255, 255, 255, 0.05)"
        card_border = "rgba(255, 255, 255, 0.1)"
        footer_text = "rgba(255, 255, 255, 0.5)"
        footer_border = "rgba(255, 255, 255, 0.1)"
        sidebar_bg = "#262730"
        sidebar_text = "#e0e0e0"
        history_border = "#667eea"
        font_family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        input_text_color = "#e0e0e0"
        button_text_color = "#ffffff"
    else:
        # Light mode colors
        bg_color = "#ffffff"
        text_color = "#1a1a1a"
        card_bg = "#f8f9fa"
        card_border = "#e0e0e0"
        footer_text = "#666666"
        footer_border = "#e0e0e0"
        sidebar_bg = "#f0f2f6"
        sidebar_text = "#1a1a1a"
        history_border = "#667eea"
        font_family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        input_text_color = "#1a1a1a"
        button_text_color = "#ffffff"
    
    return f"""
        <style>
        * {{
            font-family: {font_family};
        }}
        
        /* Main container styling */
        .main {{
            padding: 0rem 0;
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* Title styling - removed default background */
        .title-section {{
            text-align: center;
            margin-bottom: 1rem;
            margin-top: 0.5rem;
            padding: 0.5rem 0;
            border-radius: 10px;
            color: {text_color};
            background: transparent !important;
        }}
        
        /* Converter card styling */
        .converter-card {{
            background-color: {card_bg};
            border-radius: 15px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            border: 1px solid {card_border};
            color: {text_color};
        }}
        
        /* Result display */
        .result-display {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin: 1.5rem 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }}
        
        /* Button styling */
        .stButton > button {{
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            font-family: {font_family};
            color: {button_text_color} !important;
            font-size: 0.95rem;
        }}
        
        /* History styling */
        .history-item {{
            background-color: {card_bg};
            padding: 0.75rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border-left: 3px solid {history_border};
            color: {text_color};
            font-family: {font_family};
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            color: {footer_text};
            font-size: 0.9rem;
            border-top: 1px solid {footer_border};
            font-family: {font_family};
        }}
        
        /* Input and select styling */
        .stSelectbox, .stNumberInput, .stTextInput {{
            color: {input_text_color} !important;
        }}
        
        /* Text styling */
        p, label, h1, h2, h3, h4, h5, h6 {{
            color: {text_color};
            font-family: {font_family};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
        }}
        
        [data-testid="stSidebar"] [class*="stMarkdown"] {{
            color: {sidebar_text} !important;
        }}
        
        [data-testid="stSidebar"] h3 {{
            color: {sidebar_text} !important;
        }}
        
        [data-testid="stSidebar"] label {{
            color: {sidebar_text} !important;
        }}
        
        [data-testid="stSidebar"] small {{
            color: {sidebar_text} !important;
        }}
        
        /* Subheader styling */
        .stSubheader {{
            color: {text_color} !important;
        }}
        </style>
    """

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'conversion_history' not in st.session_state:
    st.session_state.conversion_history = []

if 'cached_rates' not in st.session_state:
    st.session_state.cached_rates = {}

if 'last_update_time' not in st.session_state:
    st.session_state.last_update_time = None

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Apply theme CSS after session state is initialized
st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ============================================================================
# API CONFIGURATION
# ============================================================================
API_URL = "https://api.exchangerate-api.com/v4/latest"
SUPPORTED_CURRENCIES = {
    # Major Global Currencies
    "USD": "🇺🇸 US Dollar",
    "EUR": "🇪🇺 Euro",
    "GBP": "🇬🇧 British Pound",
    "JPY": "🇯🇵 Japanese Yen",
    "AUD": "🇦🇺 Australian Dollar",
    "CAD": "🇨🇦 Canadian Dollar",
    
    # European Currencies
    "CHF": "🇨🇭 Swiss Franc",
    "SEK": "🇸🇪 Swedish Krona",
    "NOK": "🇳🇴 Norwegian Krone",
    "DKK": "🇩🇰 Danish Krone",
    "PLN": "🇵🇱 Polish Zloty",
    "CZK": "🇨🇿 Czech Koruna",
    "HUF": "🇭🇺 Hungarian Forint",
    "RON": "🇷🇴 Romanian Leu",
    "BGN": "🇧🇬 Bulgarian Lev",
    "HRK": "🇭🇷 Croatian Kuna",
    "RUB": "🇷🇺 Russian Ruble",
    "TRY": "🇹🇷 Turkish Lira",
    "GRK": "🇬🇷 Greek Euro",
    
    # Asian-Pacific Currencies
    "CNY": "🇨🇳 Chinese Yuan",
    "INR": "🇮🇳 Indian Rupee",
    "SGD": "🇸🇬 Singapore Dollar",
    "HKD": "🇭🇰 Hong Kong Dollar",
    "NZD": "🇳🇿 New Zealand Dollar",
    "MYR": "🇲🇾 Malaysian Ringgit",
    "PHP": "🇵🇭 Philippine Peso",
    "THB": "🇹🇭 Thai Baht",
    "IDR": "🇮🇩 Indonesian Rupiah",
    "VND": "🇻🇳 Vietnamese Dong",
    "KRW": "🇰🇷 South Korean Won",
    "TWD": "🇹🇼 Taiwan Dollar",
    "BDT": "🇧🇩 Bangladeshi Taka",
    "PKR": "🇵🇰 Pakistani Rupee",
    
    # Americas Currencies
    "MXN": "🇲🇽 Mexican Peso",
    "BRL": "🇧🇷 Brazilian Real",
    "ARS": "🇦🇷 Argentine Peso",
    "CLP": "🇨🇱 Chilean Peso",
    "COP": "🇨🇴 Colombian Peso",
    "PEN": "🇵🇪 Peruvian Sol",
    "VEF": "🇻🇪 Venezuelan Bolívar",
    
    # African Currencies
    "ZAR": "🇿🇦 South African Rand",
    "EGP": "🇪🇬 Egyptian Pound",
    "NGN": "🇳🇬 Nigerian Naira",
    "GHS": "🇬🇭 Ghanaian Cedi",
    "KES": "🇰🇪 Kenyan Shilling",
    "MAD": "🇲🇦 Moroccan Dirham",
    "TND": "🇹🇳 Tunisian Dinar",
    "ZWL": "🇿🇼 Zimbabwean Dollar",
    
    # Middle East Currencies
    "AED": "🇦🇪 UAE Dirham",
    "SAR": "🇸🇦 Saudi Riyal",
    "QAR": "🇶🇦 Qatari Riyal",
    "KWD": "🇰🇼 Kuwaiti Dinar",
    "BHD": "🇧🇭 Bahraini Dinar",
    "OMR": "🇴🇲 Omani Rial",
    "JOD": "🇯🇴 Jordanian Dinar",
    "ILS": "🇮🇱 Israeli Shekel",
    "IRR": "🇮🇷 Iranian Rial",
}

CURRENCY_SYMBOLS = {
    # Major Global Currencies
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "AUD": "A$",
    "CAD": "C$",
    
    # European Currencies
    "CHF": "CHF",
    "SEK": "kr",
    "NOK": "kr",
    "DKK": "kr",
    "PLN": "zł",
    "CZK": "Kč",
    "HUF": "Ft",
    "RON": "lei",
    "BGN": "лв",
    "HRK": "kn",
    "RUB": "₽",
    "TRY": "₺",
    "GRK": "€",
    
    # Asian-Pacific Currencies
    "CNY": "¥",
    "INR": "₹",
    "SGD": "S$",
    "HKD": "HK$",
    "NZD": "NZ$",
    "MYR": "RM",
    "PHP": "₱",
    "THB": "฿",
    "IDR": "Rp",
    "VND": "₫",
    "KRW": "₩",
    "TWD": "NT$",
    "BDT": "৳",
    "PKR": "₨",
    
    # Americas Currencies
    "MXN": "$",
    "BRL": "R$",
    "ARS": "$",
    "CLP": "$",
    "COP": "$",
    "PEN": "S/",
    "VEF": "Bs",
    
    # African Currencies
    "ZAR": "R",
    "EGP": "£",
    "NGN": "₦",
    "GHS": "₵",
    "KES": "Sh",
    "MAD": "د.م.",
    "TND": "د.ت",
    "ZWL": "Z$",
    
    # Middle East Currencies
    "AED": "د.إ",
    "SAR": "﷼",
    "QAR": "ر.ق",
    "KWD": "د.ك",
    "BHD": ".د.ب",
    "OMR": "ر.ع.",
    "JOD": "د.ا",
    "ILS": "₪",
    "IRR": "﷼",
}

# ============================================================================
# API FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_exchange_rates(from_currency: str) -> Optional[Dict]:
    """
    Fetch exchange rates from the API for a given currency.
    Uses caching to minimize API calls.
    
    Args:
        from_currency: Currency code (e.g., 'USD')
    
    Returns:
        Dictionary with rates or None if API fails
    """
    try:
        with st.spinner(f"📊 Fetching live rates for {from_currency}..."):
            response = requests.get(
                f"{API_URL}/{from_currency}",
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            # Update last update time
            st.session_state.last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return data
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Connection error. Please check your internet connection.")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ API Error: {response.status_code}. Please try again.")
        return None
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        return None


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
    rates: Dict
) -> Optional[Tuple[float, float]]:
    """
    Convert amount from one currency to another.
    
    Args:
        amount: Amount to convert
        from_currency: Source currency code
        to_currency: Target currency code
        rates: Exchange rates dictionary from API
    
    Returns:
        Tuple of (converted_amount, exchange_rate) or None if conversion fails
    """
    try:
        if amount <= 0:
            st.error("❌ Please enter a positive amount.")
            return None
        
        # Extract the exchange rate
        exchange_rate = rates.get('rates', {}).get(to_currency)
        
        if exchange_rate is None:
            st.error(f"❌ Exchange rate for {to_currency} not available.")
            return None
        
        converted_amount = amount * exchange_rate
        return converted_amount, exchange_rate
    
    except Exception as e:
        st.error(f"❌ Conversion error: {str(e)}")
        return None


def add_to_history(
    amount: float,
    from_curr: str,
    to_curr: str,
    result: float,
    rate: float
) -> None:
    """
    Add conversion to history.
    
    Args:
        amount: Original amount
        from_curr: Source currency
        to_curr: Target currency
        result: Converted amount
        rate: Exchange rate used
    """
    history_entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "from": from_curr,
        "to": to_curr,
        "amount": amount,
        "result": result,
        "rate": rate
    }
    st.session_state.conversion_history.insert(0, history_entry)
    
    # Keep only last 20 conversions
    st.session_state.conversion_history = st.session_state.conversion_history[:20]


# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_theme_toggle():
    """Render the theme toggle button in the sidebar header area."""
    # Add toggle button in sidebar
    if st.sidebar.button(
        f"{'🌙 Dark Mode' if not st.session_state.dark_mode else '☀️ Light Mode'}",
        use_container_width=True,
        key="theme_toggle",
    ):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()


def render_header():
    """Render the application header."""
    # Determine text colors based on mode
    subtitle_style = "rgba(0, 0, 0, 0.6)" if not st.session_state.dark_mode else "rgba(255, 255, 255, 0.6)"
    title_style = "#1a1a1a" if not st.session_state.dark_mode else "#e0e0e0"
    
    st.markdown(f"""
    <div class="title-section">
        <h1 style="color: {title_style}; margin: 0; font-size: 2.5rem; font-weight: 700;">💱 Currency Converter</h1>
        <p style="font-size: 0.95rem; color: {subtitle_style}; margin: 0.5rem 0 0 0; font-weight: 400;">
            Real-time currency conversion using live exchange rates
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_converter():
    """Render the main currency converter interface."""
    col1, col2, col3 = st.columns([1, 0.8, 1])
    
    with col1:
        st.markdown("**From Currency**")
        from_currency = st.selectbox(
            label="From Currency",
            options=list(SUPPORTED_CURRENCIES.keys()),
            format_func=lambda x: SUPPORTED_CURRENCIES[x],
            key="from_curr",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("**Action**")
        if st.button("🔄 Swap", use_container_width=True, key="swap_btn"):
            st.session_state.from_curr, st.session_state.to_curr = (
                st.session_state.to_curr,
                st.session_state.from_curr
            )
            st.rerun()
    
    with col3:
        st.markdown("**To Currency**")
        to_currency = st.selectbox(
            label="To Currency",
            options=list(SUPPORTED_CURRENCIES.keys()),
            index=1 if len(SUPPORTED_CURRENCIES) > 1 else 0,
            format_func=lambda x: SUPPORTED_CURRENCIES[x],
            key="to_curr",
            label_visibility="collapsed"
        )
    
    # Amount input
    st.markdown("**Amount**")
    amount = st.number_input(
        label="Amount to convert",
        value=1.0,
        min_value=0.0,
        step=0.01,
        format="%.2f",
        label_visibility="collapsed"
    )
    
    return from_currency, to_currency, amount


def render_result(
    converted_amount: float,
    exchange_rate: float,
    from_curr: str,
    to_curr: str,
    amount: float
):
    """Render the conversion result in an attractive format."""
    from_symbol = CURRENCY_SYMBOLS.get(from_curr, from_curr)
    to_symbol = CURRENCY_SYMBOLS.get(to_curr, to_curr)
    
    st.markdown(f"""
    <div class="result-display">
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9; font-weight: 500;">Conversion Result</p>
        <h2 style="margin: 0.5rem 0; font-size: 2.5rem; font-weight: 700;">
            {to_symbol} {converted_amount:,.2f}
        </h2>
        <p style="margin: 0.5rem 0; font-size: 0.95rem; opacity: 0.9;">
            from {from_symbol} {amount:,.2f}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Exchange rate and timestamp
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Exchange Rate",
            f"{exchange_rate:.6f}",
            f"1 {from_curr} = {exchange_rate:.6f} {to_curr}"
        )
    with col2:
        if st.session_state.last_update_time:
            st.metric(
                "Last Updated",
                st.session_state.last_update_time,
                "🔄 Live rates"
            )


def render_history():
    """Render conversion history in the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 History")
    
    if st.session_state.conversion_history:
        # Clear history button
        if st.sidebar.button("🗑️ Clear History", use_container_width=True):
            st.session_state.conversion_history = []
            st.rerun()
        
        st.sidebar.markdown("<b>Recent conversions:</b>", unsafe_allow_html=True)
        
        for idx, entry in enumerate(st.session_state.conversion_history):
            from_sym = CURRENCY_SYMBOLS.get(entry['from'], entry['from'])
            to_sym = CURRENCY_SYMBOLS.get(entry['to'], entry['to'])
            
            st.sidebar.markdown(f"""
            <div class="history-item">
                <small><strong style="font-weight: 700;">{entry['timestamp']}</strong></small><br>
                {from_sym} {entry['amount']:.2f} → {to_sym} {entry['result']:.2f}<br>
                <small>Rate: {entry['rate']:.6f}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.info("No conversions yet. Start converting!")


def render_footer():
    """Render the application footer."""
    mode_text = "Dark Mode" if st.session_state.dark_mode else "Light Mode"
    st.markdown(f"""
    <div class="footer">
        <p style="margin: 0.5rem 0;">Built with ❤️ using Python + Streamlit + Free Currency Exchange API</p>
        <p style="font-size: 0.85rem; margin: 0.5rem 0; font-weight: 600;">Made By Syed Vaseem Basha</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">Currently in: <strong>{mode_text}</strong></p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application logic."""
    
    # Render theme toggle in sidebar (top)
    render_theme_toggle()
    
    # Render header
    render_header()
    
    # Render converter interface
    st.markdown('<div class="converter-card">', unsafe_allow_html=True)
    from_currency, to_currency, amount = render_converter()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Convert button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        convert_btn = st.button(
            "✨ Convert",
            use_container_width=True,
            type="primary"
        )
    
    # Perform conversion
    if convert_btn:
        if amount <= 0:
            st.error("❌ Please enter a positive amount.")
        else:
            # Fetch rates from API
            rates = fetch_exchange_rates(from_currency)
            
            if rates:
                # Convert currency
                result = convert_currency(amount, from_currency, to_currency, rates)
                
                if result:
                    converted_amount, exchange_rate = result
                    
                    # Display result
                    render_result(
                        converted_amount,
                        exchange_rate,
                        from_currency,
                        to_currency,
                        amount
                    )
                    
                    # Add to history
                    add_to_history(
                        amount,
                        from_currency,
                        to_currency,
                        converted_amount,
                        exchange_rate
                    )
    
    # Render history in sidebar
    render_history()
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
