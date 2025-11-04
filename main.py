"""
Books Dashboard - Streamlit Implementation
Optimized for laptop resolutions with automatic screen detection
Data columns expected: Title, Price (£), Rating, Availability
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import re
import tkinter as tk

# ================== SCREEN RESOLUTION DETECTION ==================
def get_screen_resolution():
    """Detect screen resolution for responsive sizing"""
    try:
        root = tk.Tk()
        root.withdraw()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height
    except Exception:
        return 1366, 768  # Fallback to common laptop resolution

SCREEN_W, SCREEN_H = get_screen_resolution()

# Calculate responsive sizing based on screen resolution
FONT_SIZE_BASE = max(12, min(16, int(SCREEN_W / 100)))
FONT_SIZE_LABEL = FONT_SIZE_BASE - 2
FONT_SIZE_KPI = max(20, min(28, int(SCREEN_W / 70)))
FONT_SIZE_HEADER = max(24, min(32, int(SCREEN_W / 60)))
CHART_HEIGHT = int(min(SCREEN_H * 0.30, 350))
TABLE_HEIGHT = int(min(SCREEN_H * 0.25, 250))

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Books Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS WITH RESPONSIVE SIZING =============
st.markdown(f"""
<style>
    /* Global font sizing */
    html, body, [class*='css'] {{ font-size: {FONT_SIZE_BASE}px; }}
    .main-header {{ background: linear-gradient(90deg, #1E88E5 0%, #1565C0 100%); padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
    .main-header h1 {{ font-size: {FONT_SIZE_HEADER}px; margin: 0; }}
    .main-header p {{ font-size: {FONT_SIZE_LABEL}px; margin: 0.5rem 0 0 0; }}
    .kpi-container {{ background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem; border-left: 4px solid #1E88E5; min-height: 100px; }}
    .kpi-value {{ font-size: {FONT_SIZE_KPI}px; font-weight: bold; color: #1E88E5; margin: 0; }}
    .kpi-label {{ font-size: {FONT_SIZE_LABEL}px; color: #666; margin-top: 0.5rem; }}
    .chart-container {{ background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem; }}
    .filter-container {{ background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }}
    .block-container {{ padding-top: 2rem; padding-bottom: 1rem; }}
    .stDataFrame {{ font-size: {FONT_SIZE_BASE}px; }}
</style>
""", unsafe_allow_html=True)

# ================== DATA LOADING ==================
@st.cache_data
def load_data(file_path='books_data.csv'):
    """
    Load books data from CSV, clean columns and data issues.
    Expected columns: Title, Price (£), Rating, Availability
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"❌ File '{file_path}' not found. Please make sure your CSV file is present!")
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None
    df.columns = df.columns.str.strip()
    column_mapping = {}
    for col in df.columns:
        col_lower = col.lower()
        if 'title' in col_lower and 'Title' not in column_mapping.values():
            column_mapping[col] = 'Title'
        elif 'price' in col_lower and 'Price' not in column_mapping.values():
            column_mapping[col] = 'Price'
        elif 'rating' in col_lower and 'Rating' not in column_mapping.values():
            column_mapping[col] = 'Rating'
        elif ('availability' in col_lower or 'avail' in col_lower) and 'Availability' not in column_mapping.values():
            column_mapping[col] = 'Availability'
    df.rename(columns=column_mapping, inplace=True)
    df = df.loc[:, ~df.columns.duplicated()]
    required_cols = ['Title', 'Price', 'Rating', 'Availability']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
        st.info("Expected columns: Title, Price (£), Rating, Availability")
        return None
    df['Price'] = df['Price'].astype(str).str.replace(r'[£,$]', '', regex=True).str.replace('N/A', '').str.strip()
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    def clean_rating(x):
        if pd.isnull(x): return np.nan
        s = str(x).strip()
        if re.match(r'^\d+$', s): return float(s)
        word_to_num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        if s.lower() in word_to_num: return float(word_to_num[s.lower()])
        return np.nan
    df['Rating'] = df['Rating'].apply(clean_rating)
    df['Availability'] = df['Availability'].astype(str).str.strip()
    df = df.dropna(subset=['Title', 'Price', 'Rating', 'Availability'])
    df.reset_index(drop=True, inplace=True)
    return df

# ================== KPI CALCULATIONS ==================
def calculate_kpis(df):
    kpis = {}
    kpis['avg_price'] = df['Price'].mean() if 'Price' in df.columns else np.nan
    kpis['avg_rating'] = df['Rating'].mean() if 'Rating' in df.columns else np.nan
    kpis['total_books'] = len(df)
    kpis['in_stock'] = len(df[df['Availability'].str.contains('In stock', case=False, na=False)]) if 'Availability' in df.columns else 0
    kpis['min_price'] = df['Price'].min() if 'Price' in df.columns else np.nan
    kpis['max_price'] = df['Price'].max() if 'Price' in df.columns else np.nan
    kpis['availability_rate'] = (kpis['in_stock'] / kpis['total_books']) * 100 if kpis['total_books'] > 0 else 0
    return kpis

# ===== VISUALIZATION FUNCTIONS =====
def create_avg_price_by_rating(df):
    avg_by_rating = df.groupby('Rating')['Price'].mean().reset_index().sort_values('Rating')
    fig = go.Figure(go.Bar(
        x=avg_by_rating['Rating'],
        y=avg_by_rating['Price'],
        marker_color='#1E88E5',
        text=avg_by_rating['Price'].round(2),
        textposition='outside',
        texttemplate='£%{text}',
        hovertemplate='<b>Rating:</b> %{x}<br><b>Avg Price:</b> £%{y:.2f}<extra></extra>'
    ))
    fig.update_layout(
        title="Average Price by Rating",
        xaxis_title="Rating",
        yaxis_title="Average Price (£)",
        showlegend=False,
        height=CHART_HEIGHT,
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=FONT_SIZE_BASE),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def create_rating_distribution(df):
    rating_counts = df['Rating'].value_counts().sort_index()
    fig = go.Figure(go.Pie(
        labels=rating_counts.index,
        values=rating_counts.values,
        hole=0.4,
        marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
    ))
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>Rating:</b> %{label}<br><b>Count:</b> %{value}<br><b>Percentage:</b> %{percent}<extra></extra>'
    )
    fig.update_layout(
        title="Distribution of Book Ratings",
        height=CHART_HEIGHT,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5),
        font=dict(size=FONT_SIZE_BASE),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def create_price_distribution(df):
    df_copy = df.copy()
    df_copy['Price_Range'] = pd.cut(df_copy['Price'], bins=5, precision=2)
    price_counts = df_copy['Price_Range'].value_counts().sort_index()
    labels = [f"£{interval.left:.2f} - £{interval.right:.2f}" for interval in price_counts.index]
    fig = go.Figure(go.Bar(
        x=labels,
        y=price_counts.values,
        marker_color='#45B7D1',
        text=price_counts.values,
        textposition='outside',
        hovertemplate='<b>Price Range:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
    ))
    fig.update_layout(
        title="Price Distribution",
        xaxis_title="Price Range",
        yaxis_title="Number of Books",
        showlegend=False,
        height=CHART_HEIGHT,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-45,
        font=dict(size=FONT_SIZE_BASE),
        margin=dict(l=40, r=40, t=60, b=80)
    )
    return fig

def create_availability_chart(df):
    avail_counts = df['Availability'].value_counts()
    fig = go.Figure(go.Bar(
        x=avail_counts.index,
        y=avail_counts.values,
        marker_color=['#28a745' if 'stock' in x.lower() else '#dc3545' for x in avail_counts.index],
        text=avail_counts.values,
        textposition='outside',
        hovertemplate='<b>Status:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
    ))
    fig.update_layout(
        title="Book Availability Status",
        xaxis_title="Availability Status",
        yaxis_title="Number of Books",
        showlegend=False,
        height=CHART_HEIGHT,
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=FONT_SIZE_BASE),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

# ================== MAIN APP ==================
def main():
    st.markdown(f"""
    <div class="main-header">
        <h1>📚 Books Dashboard</h1>
        <p>Data Source: books.toscrape.com | Screen: {SCREEN_W}×{SCREEN_H}</p>
    </div>
    """, unsafe_allow_html=True)
    df = load_data('books_data.csv')
    if df is None:
        st.stop()
    st.sidebar.header("🔍 Filters")
    rating_options = sorted(df['Rating'].dropna().unique())
    selected_ratings = st.sidebar.multiselect(
        "Select Ratings",
        options=rating_options,
        default=rating_options
    )
    min_price, max_price = float(df['Price'].min()), float(df['Price'].max())
    price_range = st.sidebar.slider(
        "Price Range (£)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=0.01
    )
    avail_options = df['Availability'].unique()
    selected_availability = st.sidebar.multiselect(
        "Availability Status",
        options=avail_options,
        default=avail_options
    )
    filtered_df = df[
        (df['Rating'].isin(selected_ratings)) &
        (df['Price'] >= price_range[0]) &
        (df['Price'] <= price_range[1]) &
        (df['Availability'].isin(selected_availability))
    ]
    kpis = calculate_kpis(filtered_df)
    st.subheader("📊 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">£{kpis['avg_price']:.2f}</div>
            <div class="kpi-label">Average Price</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">{kpis['avg_rating']:.1f}</div>
            <div class="kpi-label">Average Rating</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">{kpis['total_books']:,}</div>
            <div class="kpi-label">Total Books</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-value">{kpis['availability_rate']:.1f}%</div>
            <div class="kpi-label">In Stock Rate</div>
        </div>
        """, unsafe_allow_html=True)
    st.subheader("📈 Analytics")
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig1 = create_avg_price_by_rating(filtered_df)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig2 = create_rating_distribution(filtered_df)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig3 = create_price_distribution(filtered_df)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig4 = create_availability_chart(filtered_df)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    st.subheader("📋 Book Details")
    display_df = filtered_df.copy()
    display_df['Price'] = display_df['Price'].apply(lambda x: f"£{x:.2f}")
    st.dataframe(
        display_df,
        use_container_width=True,
        height=TABLE_HEIGHT,
        hide_index=True
    )
    with st.expander("📈 Summary Statistics"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Price Statistics**")
            st.write(f"Minimum: £{kpis['min_price']:.2f}")
            st.write(f"Maximum: £{kpis['max_price']:.2f}")
            st.write(f"Average: £{kpis['avg_price']:.2f}")
        with col2:
            st.write("**Stock Information**")
            st.write(f"Books in Stock: {kpis['in_stock']:,}")
            st.write(f"Total Books: {kpis['total_books']:,}")
            st.write(f"Stock Rate: {kpis['availability_rate']:.1f}%")

if __name__ == "__main__":
    main()