# JK TRINETRA - Stock Analysis Dashboard

A professional stock analysis application built with Streamlit, featuring technical indicators, Gann Square of Nine strategy, and Smart Money Concepts.

## Features

- **Real-time Stock Analysis**: Fetch and analyze stock data from Yahoo Finance
- **Technical Indicators**: RSI, ADX, Moving Averages (10, 20, 50, 100, 200 SMA)
- **Gann Square of Nine**: Advanced price target calculations
- **Smart Money Concepts**: Volume and price action analysis
- **Pivot Points**: Support and resistance level calculations
- **Stock Scanner**: Batch scan for buy signals, sell signals, and reversals
- **Interactive Dashboard**: Clean, responsive UI with real-time updates

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository or navigate to the project directory:
```bash
cd "d:\Work\Python Projects\JK-FINAL"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
streamlit run streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Authentication

- Default password: `JK2026`
- You can change this in `config.py` by modifying the `ACCESS_PASSWORD` constant

### Features Guide

#### Stock Selection
- Use the dropdown to select from predefined stocks
- Or type a custom stock symbol (e.g., "TRENT")

#### Scanners
- **BUY SCAN**: Find all stocks with buy signals
- **SELL SCAN**: Find all stocks with sell signals
- **REVERSAL SCAN**: Find stocks in reversal zones (reached 5th target)

#### Dashboard Components
- **Signal Banner**: Shows current trading signal (BUY/SELL/WAIT)
- **Key Metrics**: LTP, Smart Money Concept, VWAP, Trend
- **Price Levels**: Today's and previous day's high/low
- **Pivot Points**: S2, S1, Pivot, R1, R2
- **Moving Averages**: 10, 20, 50, 100, 200 SMA
- **Gann Levels**: Entry points and 5 targets for both buy and sell
- **Indicators**: RSI and ADX with interpretations

## Project Structure

```
JK-FINAL/
├── streamlit_app.py        # Main application entry point
├── config.py               # Configuration and constants
├── models.py               # Data models and enums
├── data_fetcher.py         # Yahoo Finance data fetching
├── technical_analysis.py   # Technical indicator calculations
├── trading_strategy.py     # Gann Square of Nine implementation
├── analyzer.py             # Stock analysis orchestration
├── scanner.py              # Batch stock scanning
├── ui_components.py        # Reusable UI components
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Code Architecture

The application follows clean architecture principles with clear separation of concerns:

### Layers

1. **Configuration Layer** (`config.py`)
   - All constants and settings
   - Stock symbol mappings
   - CSS styling

2. **Data Layer** (`models.py`, `data_fetcher.py`)
   - Type-safe data models
   - Data fetching and caching
   - API interactions

3. **Business Logic Layer** (`technical_analysis.py`, `trading_strategy.py`, `analyzer.py`)
   - Technical indicator calculations
   - Trading signal generation
   - Stock analysis orchestration

4. **Application Layer** (`scanner.py`, `ui_components.py`, `streamlit_app.py`)
   - Batch processing
   - UI rendering
   - User interaction handling

### Key Design Patterns

- **Separation of Concerns**: Each module has a single, well-defined responsibility
- **Type Safety**: Using dataclasses and enums for type-safe data handling
- **Caching**: Streamlit's `@st.cache_data` for performance optimization
- **Error Handling**: Comprehensive try-except blocks with logging
- **Modularity**: Reusable functions and components

## Technical Indicators

### RSI (Relative Strength Index)
- Period: 14
- Overbought: > 70
- Oversold: < 30

### ADX (Average Directional Index)
- Period: 14
- Trending: > 25
- Sideways: < 20

### Moving Averages
- Simple Moving Averages: 10, 20, 50, 100, 200 periods
- Used for trend identification and support/resistance

### Smart Money Concepts
- **Long Buildup**: Price ↑, Volume ↑
- **Short Buildup**: Price ↓, Volume ↑
- **Short Covering**: Price ↑, Volume ↓
- **Long Unwinding**: Price ↓, Volume ↓

### Gann Square of Nine
- Buy Entry: Pivot × 1.001
- Sell Entry: Pivot × 0.999
- Step Size: 0.125
- Targets: 5 levels calculated using square root method

## Security Considerations

- Password authentication for access control
- No sensitive data stored in code
- Input validation for stock symbols
- Safe HTML rendering with Streamlit

## Performance Optimization

- Data caching with 60-second TTL
- Efficient pandas operations
- Minimal API calls through caching
- Lazy loading of stock data

## Disclaimer

**IMPORTANT**: This application is for educational and study purposes only. It is NOT a buy/sell recommendation. Always consult your financial advisor before making any investment decisions.

## Contributing

When contributing to this project, please:

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Write docstrings for all public functions
4. Add logging for important operations
5. Write unit tests for new features
6. Update documentation as needed

## License

This project is for private use only.

## Support

For issues or questions, please contact the development team.

## Version History

- **v2.0** (2026-01-19): Complete refactoring with clean architecture
- **v1.0** (Initial): Basic functionality
