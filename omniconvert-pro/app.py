import streamlit as st
from unit_registry import UnitRegistry
from converter_engine import ConverterEngine
from currency_provider import CurrencyProvider

# Page configuration
st.set_page_config(
    page_title="OmniConvert Pro",
    page_icon="⚡",
    layout="wide",
)

# Theme selection in sidebar
st.sidebar.markdown("### Settings")
theme = st.sidebar.radio("Theme", ["Dark", "Light"], index=0)

# Custom CSS for theme support
dark_css = """
<style>
    .stApp {
        background-color: #050505;
        color: #e5e7eb;
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.05em;
        font-size: 3rem;
        margin-bottom: 0;
        color: white;
    }
    .sub-header {
        color: #6366f1;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.2em;
        margin-bottom: 2rem;
    }
    div.stButton > button {
        background-color: #4f46e5;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #4338ca;
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.4);
    }
    .result-card {
        background: rgba(79, 70, 229, 0.05);
        border: 1px solid rgba(79, 70, 229, 0.2);
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        margin-top: 2rem;
    }
    .result-value {
        font-size: 4rem;
        font-weight: 800;
        color: white;
    }
    .chain-step {
        font-family: 'JetBrains Mono', monospace;
        color: #71717a;
        font-size: 0.8rem;
        text-align: left;
    }
</style>
"""

light_css = """
<style>
    .stApp {
        background-color: #ffffff;
        color: #111827;
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.05em;
        font-size: 3rem;
        margin-bottom: 0;
        color: #111827;
    }
    .sub-header {
        color: #4f46e5;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.2em;
        margin-bottom: 2rem;
    }
    div.stButton > button {
        background-color: #4f46e5;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color: #4338ca;
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.2);
    }
    .result-card {
        background: rgba(79, 70, 229, 0.03);
        border: 1px solid rgba(79, 70, 229, 0.1);
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        margin-top: 2rem;
    }
    .result-value {
        font-size: 4rem;
        font-weight: 800;
        color: #111827;
    }
    .chain-step {
        font-family: 'JetBrains Mono', monospace;
        color: #4b5563;
        font-size: 0.8rem;
        text-align: left;
    }
</style>
"""

if theme == "Dark":
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    st.markdown(light_css, unsafe_allow_html=True)

# Initialize engines
@st.cache_resource
def get_engines():
    reg = UnitRegistry()
    eng = ConverterEngine(reg)
    cur = CurrencyProvider()
    return reg, eng, cur

registry, engine, currency = get_engines()

# Header
st.markdown('<h1 class="main-header">OMNICONVERT <span style="color: #6366f1">PRO</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">STRICT PYTHON ENGINE • STREAMLIT CORE</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["⚡ Units", "💰 Currency", "🔍 Explorer"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Source")
        value = st.number_input("Amount", value=10.0, step=0.1, format="%.4f")
        
        quantities = registry.get_quantities()
        selected_q = st.selectbox("Category", quantities, index=0)
        
        from_units = registry.get_units_for_quantity(selected_q)
        from_unit = st.selectbox("From Unit", from_units, key="from_unit")

    with col2:
        st.markdown("### Target")
        to_units = registry.get_units_for_quantity(selected_q)
        to_unit = st.selectbox("To Unit", to_units, key="to_unit", index=min(1, len(to_units)-1))
        
        st.markdown("### Context")
        c1, c2 = st.columns(2)
        with c1:
            country = st.selectbox("Country/System", ["US", "UK", "IN", "PK"], index=0)
        with c2:
            state = st.selectbox("State/Region", ["", "UP", "RJ"], index=0)

    st.divider()
    
    precision = st.slider("Decimal Precision", 0, 10, 4)
    
    if st.button("Calculate Conversion"):
        try:
            res = engine.convert(
                value, 
                from_unit, 
                to_unit, 
                country=country if country else None, 
                state=state if state else None,
                precision=precision
            )
            
            st.markdown(f"""
            <div class="result-card">
                <p style="text-transform: uppercase; font-size: 0.7rem; font-weight: bold; color: #71717a; margin-bottom: 0.5rem;">Resulting Value</p>
                <div class="result-value">{res.formatted_value} <span style="font-size: 1.5rem; color: #6366f1;">{res.to_unit}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Dimensional Chain Analysis"):
                for step in res.chain:
                    st.markdown(f'<div class="chain-step">{step}</div>', unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"Computation Error: {str(e)}")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        cur_amount = st.number_input("Amount", value=1.0, key="cur_amount")
        supported = currency.get_supported()
        f_cur = st.selectbox("From Currency", supported, index=0)
    with col2:
        t_cur = st.selectbox("To Currency", supported, index=min(1, len(supported)-1))
    
    if st.button("Convert Currency"):
        try:
            res = currency.convert(cur_amount, f_cur, t_cur)
            st.markdown(f"""
            <div class="result-card">
                <p style="text-transform: uppercase; font-size: 0.7rem; font-weight: bold; color: #71717a; margin-bottom: 0.5rem;">Market Projection</p>
                <div class="result-value">{res.result:,.2f} <span style="font-size: 1.5rem; color: #6366f1;">{res.to_code}</span></div>
                <p style="font-size: 0.8rem; color: #71717a; margin-top: 1rem;">Rate: 1 {res.from_code} = {res.rate:.4f} {res.to_code}</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(str(e))

with tab3:
    st.markdown("### Registry Explorer")
    for q in quantities:
        with st.expander(f"{q.upper()} System"):
            st.write(f"SI Base Unit: **{registry.get_base_unit(q)}**")
            units = registry.get_units_for_quantity(q)
            st.write("Supported Indices:")
            st.code(", ".join(units))

st.markdown("---")
st.markdown('<p style="text-align: center; color: #3f3f46; font-size: 0.7rem;">PRO-GRADE PRECISION ENGINE • © 2026 OMNICONVERT LABS</p>', unsafe_allow_html=True)
