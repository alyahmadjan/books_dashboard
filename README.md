# 📚 Books Dashboard

A responsive **Streamlit-based data visualization dashboard** for analyzing book data scraped from [books.toscrape.com](https://books.toscrape.com). The dashboard provides interactive charts, key performance indicators, and detailed data tables with automatic screen resolution detection for optimal viewing.

## 🎯 Features

- **Responsive Design**: Automatically adjusts layout and font sizes based on screen resolution
- **Interactive KPIs**: Display key metrics including average price, average rating, total books, and availability rate
- **Dynamic Visualizations**: Interactive charts powered by Plotly for better data exploration
- **Data Cleaning**: Automatic handling of various data formats (currencies, ratings, availability status)
- **Screen Detection**: Detects screen resolution for optimal user experience
- **Data Filtering**: Easy filtering and exploration of book data with Streamlit widgets

## 📊 Expected Data Format

The dashboard expects a CSV file (`books_data.csv`) with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| Title | Book title | "The Great Gatsby" |
| Price (£) | Price in pounds | "12.99" or "£12.99" |
| Rating | Book rating | "5" or "five" |
| Availability | Stock status | "In stock" or "Out of stock" |

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/books-dashboard.git
cd books-dashboard
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

1. **Prepare your data**: Ensure you have a `books_data.csv` file in the project root directory with the required columns.

2. **Run Streamlit**
```bash
streamlit run main.py
```

3. **Access the dashboard**: Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
books-dashboard/
├── main.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── CONTRIBUTING.md        # Contribution guidelines
├── LICENSE                # License file
├── books_data.csv         # Sample/actual book data
└── .gitignore            # Git ignore file
```

## 🛠️ Tech Stack

- **Streamlit**: Web app framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **NumPy**: Numerical computing
- **Tkinter**: Screen resolution detection

## 📈 Dashboard Metrics

The dashboard displays the following KPIs:

- **Average Price**: Mean price of all books
- **Average Rating**: Mean rating across all books
- **Total Books**: Total number of books in the dataset
- **In Stock**: Count of books currently in stock
- **Availability Rate**: Percentage of books in stock
- **Price Range**: Minimum and maximum book prices

## 🔧 Customization

### Modify Screen Resolution Breakpoints

Edit the font size calculations in `main.py`:

```python
FONT_SIZE_BASE = max(12, min(16, int(SCREEN_W / 100)))
FONT_SIZE_KPI = max(20, min(28, int(SCREEN_W / 70)))
```

### Update Data Source

Change the CSV file path in the `load_data()` function:

```python
def load_data(file_path='your_custom_path.csv'):
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the maintainer.

## 🔗 Data Source

Book data is sourced from [books.toscrape.com](https://books.toscrape.com), a sandbox website for web scraping practice.

---

**Last Updated**: November 2025
