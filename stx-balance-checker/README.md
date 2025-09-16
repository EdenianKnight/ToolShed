# STX Balance Checker

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A professional-grade Python application for monitoring Stacks (STX) cryptocurrency wallet balances with support for multiple data sources including Excel files, Google Sheets, and CSV files.

## 🌟 Features

- **Multi-format Support**: Read wallet addresses from Excel files, Google Sheets, or CSV files
- **Named Wallets**: Assign custom names to wallets for better organization
- **Comprehensive Balance Information**: Shows available, locked, and total STX balances
- **Rate Limiting**: Respectful API usage with configurable delays
- **Professional Reporting**: Clean, formatted output with summary statistics
- **Export Functionality**: Save results to JSON and Excel formats
- **Error Handling**: Robust error handling for network issues and invalid data
- **Interactive CLI**: User-friendly command-line interface
- **Flexible Column Detection**: Automatically detects various column naming conventions

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Supported File Formats](#-supported-file-formats)
- [API Reference](#-api-reference)
- [Configuration](#️-configuration)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### System Requirements

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip python3-full
```

#### macOS

```bash
# Using Homebrew
brew install python3

# Or using MacPorts
sudo port install python38
```

#### Windows

Download Python from [python.org](https://python.org) and ensure pip is included.

### Project Setup

1. **Clone or create the project directory:**

   ```bash
   mkdir stx-balance-checker
   cd stx-balance-checker
   ```

2. **Create and activate virtual environment:**

   ```bash
   python3 -m venv stx_env
   
   # On Linux/macOS:
   source stx_env/bin/activate
   
   # On Windows:
   stx_env\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install requests pandas openpyxl xlrd
   ```

4. **Create requirements file:**

   ```bash
   pip freeze > requirements.txt
   ```

## 🏃 Quick Start

1. **Download the main script** and save it as `stx_checker.py`

2. **Create a sample wallet file:**

   ```csv
   Name,Address
   Main Wallet,SP1J8ff7N441J2p29F12C0ZA4GDE85X4QY8DRS1X6
   Trading Wallet,SP3VCZ5ASNS5V22QHH2E41R82T960K22G0SK2GTG3
   Cold Storage,SP24G0K7X701P65A7600J8TA053K01DbA2S2D1D6J
   ```

3. **Run the application:**

   ```bash
   python stx_checker.py
   ```

4. **Follow the interactive prompts** to select your data source and view results.

## 📖 Usage

### Command Line Interface

The application provides an interactive menu system:

```table
STX WALLET BALANCE CHECKER
=========================================
Choose data source:
1. Excel file (.xlsx/.xls)
2. Google Sheets (public)
3. CSV file
4. Manual input (hardcoded addresses)

Enter your choice (1-4):
```

### Data Source Options

#### 1. Excel Files

- Supports `.xlsx` and `.xls` formats
- Can specify sheet names or use the first sheet by default
- Automatically detects column headers

#### 2. Google Sheets

- Requires publicly accessible Google Sheets
- Automatically converts sharing URLs to CSV export format
- Supports multiple sheet names

#### 3. CSV Files

- Standard comma-separated values format
- UTF-8 encoding recommended
- Flexible header detection

#### 4. Hardcoded Addresses

- For testing and development purposes
- Predefined wallet addresses with sample names

## 📊 Supported File Formats

### Column Header Detection

The application automatically detects these column variations:

| Name Columns | Address Columns |
|--------------|----------------|
| Name | Address |
| Wallet_Name | Wallet_Address |
| wallet_name | wallet_address |
| name | address |
| Label | STX_Address |
| label | stx_address |

### File Structure Examples

#### Excel/CSV Format

```csv
Name,Address
Personal Wallet,SP1J8ff7N441J2p29F12C0ZA4GDE85X4QY8DRS1X6
Business Wallet,SP3VCZ5ASNS5V22QHH2E41R82T960K22G0SK2GTG3
```

#### Alternative Format

```csv
Wallet_Name,Wallet_Address
Main Account,SP1J8ff7N441J2p29F12C0ZA4GDE85X4QY8DRS1X6
Savings Account,SP3VCZ5ASNS5V22QHH2E41R82T960K22G0SK2GTG3
```

## 🔧 API Reference

### Core Classes

#### `STXBalanceChecker`

The main class that handles all balance checking operations.

**Constructor:**

```python
STXBalanceChecker(base_url: str = "https://api.hiro.so/v2/accounts/")
```

**Key Methods:**

##### `load_wallets_from_excel(file_path: str, sheet_name: str = None)`

Load wallet addresses from Excel files.

- **Parameters:**
  - `file_path`: Path to Excel file
  - `sheet_name`: Optional sheet name (uses first sheet if None)
- **Returns:** List of wallet dictionaries
- **Raises:** `ValueError` if no address column found

##### `load_wallets_from_google_sheets(sheet_url: str, sheet_name: str = None)`

Load wallet addresses from Google Sheets.

- **Parameters:**
  - `sheet_url`: Google Sheets URL or CSV export URL
  - `sheet_name`: Optional sheet name
- **Returns:** List of wallet dictionaries
- **Note:** Requires publicly accessible sheets

##### `get_balance(address: str, name: str = None)`

Retrieve balance information for a single wallet.

- **Parameters:**
  - `address`: Stacks wallet address
  - `name`: Optional wallet name/label
- **Returns:** Dictionary with balance information or error details

##### `check_wallets_from_list(wallets: List[Dict], delay: float = 0.1)`

Check balances for multiple wallets with rate limiting.

- **Parameters:**
  - `wallets`: List of wallet dictionaries
  - `delay`: Delay between API requests in seconds
- **Returns:** List of balance results

## ⚙️ Configuration

### Environment Variables

You can customize the application behavior using environment variables:

```bash
# API base URL (default: https://api.hiro.so/v2/accounts/)
export STX_API_BASE_URL="https://api.hiro.so/v2/accounts/"

# Default delay between requests (default: 0.1 seconds)
export STX_REQUEST_DELAY=0.1

# Request timeout (default: 10 seconds)
export STX_REQUEST_TIMEOUT=10
```

### Rate Limiting

The application implements respectful rate limiting:

- Default delay: 0.1 seconds between requests
- Configurable timeout: 10 seconds per request
- Session reuse for better performance

## 📝 Examples

### Example 1: Basic Usage with CSV

```python
from stx_checker import STXBalanceChecker

checker = STXBalanceChecker()
wallets = checker.load_wallets_from_csv('my_wallets.csv')
results = checker.check_wallets_from_list(wallets)
checker.print_results(results)
```

### Example 2: Google Sheets Integration

```python
checker = STXBalanceChecker()
sheet_url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
wallets = checker.load_wallets_from_google_sheets(sheet_url)
results = checker.check_wallets_from_list(wallets, delay=0.2)
checker.export_results(results, 'monthly_report')
```

### Example 3: Custom Configuration

```python
# Custom API endpoint and longer delays
checker = STXBalanceChecker(base_url="https://custom-api.example.com/v2/accounts/")
results = checker.check_wallets_from_list(wallets, delay=0.5)
```

## 📈 Output Format

### Console Output

```table
================================================================================
STX WALLET BALANCE REPORT
================================================================================

✅ Personal Wallet
   Address:           SP1J8ff7N441J2p29F12C0ZA4GDE85X4QY8DRS1X6
   Available Balance:     1,234.567890 STX
   Locked Balance:            0.000000 STX
   Nonce:                            45

✅ Trading Wallet
   Address:           SP3VCZ5ASNS5V22QHH2E41R82T960K22G0SK2GTG3
   Available Balance:       890.123456 STX
   Locked Balance:          100.000000 STX
   Total Balance:           990.123456 STX
   Nonce:                            23

================================================================================
SUMMARY
================================================================================
Total wallets checked: 2
Successful checks:     2
Failed checks:         0
Combined balance:      2,224.691346 STX
================================================================================
```

### Exported Files

#### JSON Format

```json
[
  {
    "name": "Personal Wallet",
    "address": "SP1J8ff7N441J2p29F12C0ZA4GDE85X4QY8DRS1X6",
    "balance_stx": 1234.567890,
    "locked_stx": 0.0,
    "total_stx": 1234.567890,
    "nonce": 45,
    "success": true
  }
]
```

#### Excel Export

Includes columns: Name, Address, Available_STX, Locked_STX, Total_STX, Nonce, Status

## 🔍 Troubleshooting

### Common Issues

#### 1. Virtual Environment Errors

```bash
# Error: externally-managed-environment
# Solution: Use virtual environment
python3 -m venv stx_env
source stx_env/bin/activate
pip install -r requirements.txt
```

#### 2. Google Sheets Access Issues

- Ensure the sheet is publicly accessible
- Use "Anyone with the link" sharing permissions
- Verify the URL format is correct

#### 3. Column Detection Problems

- Check column headers match supported variations
- Remove extra spaces from headers
- Ensure data starts from row 1 (headers) and row 2 (data)

#### 4. API Rate Limiting

- Increase delay between requests
- Check Hiro API status page
- Verify wallet addresses are valid

#### 5. File Path Issues

```python
# Use absolute paths if relative paths fail
import os
file_path = os.path.abspath('wallets.xlsx')
```

### Error Codes

| Error Type | Description | Solution |
|------------|-------------|----------|
| HTTPError 429 | Rate limit exceeded | Increase delay parameter |
| HTTPError 404 | Invalid wallet address | Verify address format |
| NetworkError | Connection timeout | Check internet connection |
| FileNotFoundError | File not found | Verify file path |
| ValueError | Invalid column headers | Check column names |

## 🧪 Testing

### Unit Tests

```bash
# Run unit tests (when available)
python -m pytest tests/
```

### Manual Testing

```bash
# Test with sample data
python create_sample_excel.py
python stx_checker.py
```

## 📊 Performance Considerations

### Optimization Tips

1. **Batch Size**: Process wallets in reasonable batches (50-100 addresses)
2. **Rate Limiting**: Use appropriate delays (0.1-0.5 seconds)
3. **Session Reuse**: The application automatically reuses HTTP sessions
4. **Error Handling**: Failed requests don't stop the entire process
5. **Memory Usage**: Large datasets are processed iteratively

### Benchmarks

- **Small datasets** (1-10 wallets): ~1-5 seconds
- **Medium datasets** (10-100 wallets): ~10-60 seconds
- **Large datasets** (100+ wallets): ~2-10 minutes

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install development dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

4. Make your changes
5. Run tests and linting
6. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for public methods
- Maintain test coverage above 80%

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hiro API](https://docs.hiro.so/) for providing STX blockchain data
- [Pandas](https://pandas.pydata.org/) for data manipulation
- [Requests](https://requests.readthedocs.io/) for HTTP client functionality

## 📞 Support

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/stx-balance-checker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/stx-balance-checker/discussions)
- **Email**: <support@yourproject.com>

### FAQ

**Q: Can I check other cryptocurrencies?**
A: Currently, this tool is specifically designed for Stacks (STX). For other cryptocurrencies, you would need to modify the API endpoints and parsing logic.

**Q: Is there a rate limit for the Hiro API?**
A: Yes, the Hiro API has rate limits. The application includes built-in delays to respect these limits.

**Q: Can I run this as a scheduled job?**
A: Yes! You can set up cron jobs or systemd timers to run the checker periodically and export results automatically.

**Q: What about private Google Sheets?**
A: Currently, only publicly accessible Google Sheets are supported. For private sheets, you would need to implement OAuth authentication.

---

## Last updated: September 2025
