import requests
import json
import time
import pandas as pd
from typing import List, Dict, Optional
import os

class STXBalanceChecker:
    def __init__(self, base_url: str = "https://api.hiro.so/v2/accounts/"):
        self.base_url = base_url
        self.session = requests.Session()
        # Add a user agent to be a good API citizen
        self.session.headers.update({
            'User-Agent': 'STX-Balance-Checker/1.0'
        })
    
    def load_wallets_from_excel(self, file_path: str, sheet_name: str = None) -> List[Dict[str, str]]:
        """
        Load wallet addresses and names from Excel file
        
        Expected columns: 'Name', 'Address' (or 'Wallet_Name', 'Wallet_Address')
        
        Args:
            file_path: Path to Excel file (.xlsx or .xls)
            sheet_name: Specific sheet name (if None, uses first sheet)
            
        Returns:
            List of dictionaries with 'name' and 'address' keys
        """
        try:
            # Read Excel file
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            # Try different column name variations
            name_columns = ['Name', 'Wallet_Name', 'wallet_name', 'name', 'Label', 'label']
            address_columns = ['Address', 'Wallet_Address', 'wallet_address', 'address', 'STX_Address', 'stx_address']
            
            name_col = None
            address_col = None
            
            # Find the correct column names
            for col in df.columns:
                if col in name_columns:
                    name_col = col
                if col in address_columns:
                    address_col = col
            
            if not address_col:
                raise ValueError("No address column found. Expected columns: 'Address', 'Wallet_Address', 'address', etc.")
            
            wallets = []
            for _, row in df.iterrows():
                address = str(row[address_col]).strip()
                name = str(row[name_col]).strip() if name_col and pd.notna(row[name_col]) else f"Wallet_{len(wallets) + 1}"
                
                if address and address.lower() != 'nan' and len(address) > 10:  # Basic validation
                    wallets.append({
                        'name': name,
                        'address': address
                    })
            
            print(f"✅ Loaded {len(wallets)} wallet addresses from Excel file")
            return wallets
            
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            return []
    
    def load_wallets_from_google_sheets(self, sheet_url: str, sheet_name: str = None) -> List[Dict[str, str]]:
        """
        Load wallet addresses from Google Sheets (must be publicly accessible)
        
        Args:
            sheet_url: Google Sheets URL or CSV export URL
            sheet_name: Sheet name (for Excel-like Google Sheets)
            
        Returns:
            List of dictionaries with 'name' and 'address' keys
        """
        try:
            # Convert Google Sheets URL to CSV export format if needed
            if 'docs.google.com/spreadsheets' in sheet_url and 'export' not in sheet_url:
                # Extract the sheet ID from the URL
                sheet_id = sheet_url.split('/d/')[1].split('/')[0]
                
                if sheet_name:
                    # For specific sheet, we need to use the gid parameter
                    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
                    print("⚠️  Note: For specific sheet names, you may need to manually get the gid parameter from Google Sheets")
                else:
                    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            else:
                csv_url = sheet_url
            
            # Read the CSV data
            df = pd.read_csv(csv_url)
            
            # Try different column name variations
            name_columns = ['Name', 'Wallet_Name', 'wallet_name', 'name', 'Label', 'label']
            address_columns = ['Address', 'Wallet_Address', 'wallet_address', 'address', 'STX_Address', 'stx_address']
            
            name_col = None
            address_col = None
            
            # Find the correct column names
            for col in df.columns:
                if col in name_columns:
                    name_col = col
                if col in address_columns:
                    address_col = col
            
            if not address_col:
                raise ValueError("No address column found. Expected columns: 'Address', 'Wallet_Address', 'address', etc.")
            
            wallets = []
            for _, row in df.iterrows():
                address = str(row[address_col]).strip()
                name = str(row[name_col]).strip() if name_col and pd.notna(row[name_col]) else f"Wallet_{len(wallets) + 1}"
                
                if address and address.lower() != 'nan' and len(address) > 10:  # Basic validation
                    wallets.append({
                        'name': name,
                        'address': address
                    })
            
            print(f"✅ Loaded {len(wallets)} wallet addresses from Google Sheets")
            return wallets
            
        except Exception as e:
            print(f"❌ Error loading Google Sheets: {e}")
            print("💡 Make sure the Google Sheet is publicly accessible or shared with 'Anyone with the link'")
            return []
    
    def load_wallets_from_csv(self, file_path: str) -> List[Dict[str, str]]:
        """
        Load wallet addresses from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of dictionaries with 'name' and 'address' keys
        """
        try:
            df = pd.read_csv(file_path)
            
            # Try different column name variations
            name_columns = ['Name', 'Wallet_Name', 'wallet_name', 'name', 'Label', 'label']
            address_columns = ['Address', 'Wallet_Address', 'wallet_address', 'address', 'STX_Address', 'stx_address']
            
            name_col = None
            address_col = None
            
            # Find the correct column names
            for col in df.columns:
                if col in name_columns:
                    name_col = col
                if col in address_columns:
                    address_col = col
            
            if not address_col:
                raise ValueError("No address column found. Expected columns: 'Address', 'Wallet_Address', 'address', etc.")
            
            wallets = []
            for _, row in df.iterrows():
                address = str(row[address_col]).strip()
                name = str(row[name_col]).strip() if name_col and pd.notna(row[name_col]) else f"Wallet_{len(wallets) + 1}"
                
                if address and address.lower() != 'nan' and len(address) > 10:  # Basic validation
                    wallets.append({
                        'name': name,
                        'address': address
                    })
            
            print(f"✅ Loaded {len(wallets)} wallet addresses from CSV file")
            return wallets
            
        except Exception as e:
            print(f"❌ Error loading CSV file: {e}")
            return []
    
    def get_balance(self, address: str, name: str = None) -> Optional[Dict]:
        """
        Get balance information for a single wallet address
        
        Args:
            address: Stacks wallet address
            name: Optional wallet name/label
            
        Returns:
            Dictionary with balance info or None if error
        """
        try:
            url = f"{self.base_url}{address}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Debug: Print the response structure for troubleshooting
            # Uncomment the next line if you need to debug API responses
            # print(f"DEBUG - API Response for {address}: {json.dumps(data, indent=2)}")
            
            # Check if the response has the expected structure
            if not isinstance(data, dict):
                return {
                    'name': name or 'Unknown',
                    'address': address,
                    'error': f"Invalid API response format: expected dict, got {type(data)}",
                    'success': False
                }
            
            # Handle different response formats
            if 'balance' not in data:
                return {
                    'name': name or 'Unknown',
                    'address': address,
                    'error': "No balance information found in API response",
                    'success': False
                }
            
            balance_info = data['balance']
            
            # Handle case where balance is a string (hex value) instead of dict
            if isinstance(balance_info, str):
                # Check if it's a hex value (balance in µSTX)
                if balance_info.startswith('0x'):
                    try:
                        # Convert hex to integer (µSTX)
                        balance_ustx = int(balance_info, 16)
                        balance_stx = balance_ustx / 1_000_000
                        
                        return {
                            'name': name or 'Unknown',
                            'address': address,
                            'balance_stx': balance_stx,
                            'locked_stx': 0.0,  # No locked info available in this format
                            'total_stx': balance_stx,
                            'balance_ustx': balance_ustx,
                            'locked_ustx': 0,
                            'nonce': data.get('nonce', 0),
                            'success': True
                        }
                    except ValueError:
                        return {
                            'name': name or 'Unknown',
                            'address': address,
                            'error': f"Invalid hex balance format: {balance_info}",
                            'success': False
                        }
                else:
                    return {
                        'name': name or 'Unknown',
                        'address': address,
                        'error': f"API returned error: {balance_info}",
                        'success': False
                    }
            
            # Check if STX balance information exists
            if not isinstance(balance_info, dict) or 'stx' not in balance_info:
                return {
                    'name': name or 'Unknown',
                    'address': address,
                    'error': "No STX balance information found",
                    'success': False
                }
            
            stx_info = balance_info['stx']
            
            # Handle case where stx info is also a string
            if isinstance(stx_info, str):
                return {
                    'name': name or 'Unknown',
                    'address': address,
                    'error': f"STX info error: {stx_info}",
                    'success': False
                }
            
            # Extract balance information with safe defaults
            balance_ustx = int(stx_info.get('balance', 0))
            locked_ustx = int(stx_info.get('locked', 0))
            
            balance_stx = balance_ustx / 1_000_000
            locked_stx = locked_ustx / 1_000_000
            
            return {
                'name': name or 'Unknown',
                'address': address,
                'balance_stx': balance_stx,
                'locked_stx': locked_stx,
                'total_stx': balance_stx + locked_stx,
                'balance_ustx': balance_ustx,
                'locked_ustx': locked_ustx,
                'nonce': data.get('nonce', 0),
                'success': True
            }
            
        except requests.exceptions.HTTPError as err:
            # Handle specific HTTP errors
            if response.status_code == 404:
                error_msg = "Wallet address not found or invalid"
            elif response.status_code == 429:
                error_msg = "Rate limit exceeded. Try increasing delay between requests"
            else:
                error_msg = f"HTTP Error {response.status_code}: {err}"
                
            return {
                'name': name or 'Unknown',
                'address': address,
                'error': error_msg,
                'success': False
            }
        except requests.exceptions.RequestException as err:
            return {
                'name': name or 'Unknown',
                'address': address,
                'error': f"Network Error: {err}",
                'success': False
            }
        except (KeyError, ValueError, TypeError) as err:
            return {
                'name': name or 'Unknown',
                'address': address,
                'error': f"Data parsing error: {err}",
                'success': False
            }
    
    def check_wallets_from_list(self, wallets: List[Dict[str, str]], delay: float = 0.1, debug_mode: bool = False) -> List[Dict]:
        """
        Check balances for wallets from loaded list
        
        Args:
            wallets: List of wallet dictionaries with 'name' and 'address'
            delay: Delay between requests in seconds
            debug_mode: Enable debug output for failed requests
            
        Returns:
            List of balance dictionaries
        """
        results = []
        
        print(f"🔍 Checking balances for {len(wallets)} wallets...")
        if debug_mode:
            print("🐛 Debug mode enabled - will show detailed errors")
        
        for i, wallet in enumerate(wallets):
            print(f"   Checking {i+1}/{len(wallets)}: {wallet['name']}")
            result = self.get_balance(wallet['address'], wallet['name'])
            
            # Debug output for failed requests
            if debug_mode and not result['success']:
                print(f"     ⚠️  Failed: {result['error']}")
                print(f"     📍 Address: {result['address']}")
                
                # Try to get raw API response for debugging
                try:
                    url = f"{self.base_url}{wallet['address']}"
                    response = self.session.get(url, timeout=5)
                    print(f"     📡 Status: {response.status_code}")
                    if response.status_code != 200:
                        print(f"     📄 Response: {response.text[:200]}...")
                except Exception as debug_error:
                    print(f"     🔧 Debug error: {debug_error}")
            
            results.append(result)
            
            # Add delay between requests (except for the last one)
            if i < len(wallets) - 1 and delay > 0:
                time.sleep(delay)
        
        return results
    
    def print_results(self, results: List[Dict]):
        """Print formatted results"""
        print("\n" + "=" * 100)
        print("STX WALLET BALANCE REPORT")
        print("=" * 100)
        
        total_balance = 0
        successful_checks = 0
        
        for result in results:
            if result['success']:
                print(f"\n✅ {result['name']}")
                print(f"   Address:           {result['address']}")
                print(f"   Available Balance: {result['balance_stx']:>12.6f} STX")
                if result['locked_stx'] > 0:
                    print(f"   Locked Balance:    {result['locked_stx']:>12.6f} STX")
                    print(f"   Total Balance:     {result['total_stx']:>12.6f} STX")
                else:
                    print(f"   Locked Balance:    {0:>12.6f} STX")
                print(f"   Nonce:             {result['nonce']:>12}")
                
                total_balance += result['total_stx']
                successful_checks += 1
            else:
                print(f"\n❌ {result['name']}")
                print(f"   Address: {result['address']}")
                print(f"   Error: {result['error']}")
        
        print("\n" + "=" * 100)
        print("SUMMARY")
        print("=" * 100)
        print(f"Total wallets checked: {len(results)}")
        print(f"Successful checks:     {successful_checks}")
        print(f"Failed checks:         {len(results) - successful_checks}")
        if successful_checks > 0:
            print(f"Combined balance:      {total_balance:>12.6f} STX")
        print("=" * 100)
    
    def export_results(self, results: List[Dict], filename: str = 'stx_balance_report'):
        """Export results to both JSON and Excel"""
        # JSON export
        json_file = f"{filename}.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Excel export
        excel_file = f"{filename}.xlsx"
        df_data = []
        for result in results:
            if result['success']:
                df_data.append({
                    'Name': result['name'],
                    'Address': result['address'],
                    'Available_STX': result['balance_stx'],
                    'Locked_STX': result['locked_stx'],
                    'Total_STX': result['total_stx'],
                    'Nonce': result['nonce'],
                    'Status': 'Success'
                })
            else:
                df_data.append({
                    'Name': result['name'],
                    'Address': result['address'],
                    'Available_STX': 0,
                    'Locked_STX': 0,
                    'Total_STX': 0,
                    'Nonce': 0,
                    'Status': f"Error: {result['error']}"
                })
        
        df = pd.DataFrame(df_data)
        df.to_excel(excel_file, index=False)
        
        print(f"\n📁 Results exported to:")
        print(f"   - {json_file}")
        print(f"   - {excel_file}")

def main():
    """Main function with interactive menu"""
    checker = STXBalanceChecker()
    
    print("=" * 60)
    print("STX WALLET BALANCE CHECKER")
    print("=" * 60)
    print("Choose data source:")
    print("1. Excel file (.xlsx/.xls)")
    print("2. Google Sheets (public)")
    print("3. CSV file")
    print("4. Manual input (hardcoded addresses)")
    print("5. Debug mode (test single address)")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    wallets = []
    
    if choice == '1':
        file_path = input("Enter Excel file path: ").strip()
        sheet_name = input("Enter sheet name (press Enter for first sheet): ").strip()
        sheet_name = sheet_name if sheet_name else None
        wallets = checker.load_wallets_from_excel(file_path, sheet_name)
        
    elif choice == '2':
        sheet_url = input("Enter Google Sheets URL: ").strip()
        wallets = checker.load_wallets_from_google_sheets(sheet_url)
        
    elif choice == '3':
        file_path = input("Enter CSV file path: ").strip()
        wallets = checker.load_wallets_from_csv(file_path)
        
    elif choice == '4':
        # Hardcoded wallets for testing
        wallets = [
            {'name': 'Wallet 1', 'address': 'SP1J8ff7N441J2p29F12C0ZA4GDE85X4QY8DRS1X6'},
            {'name': 'Wallet 2', 'address': 'SP3VCZ5ASNS5V22QHH2E41R82T960K22G0SK2GTG3'},
            {'name': 'Wallet 3', 'address': 'SP24G0K7X701P65A7600J8TA053K01DbA2S2D1D6J'}
        ]
        print(f"✅ Using {len(wallets)} hardcoded wallet addresses")
    
    elif choice == '5':
        # Debug mode - test single address with full API response
        test_address = input("Enter wallet address to debug: ").strip()
        if not test_address:
            test_address = "SP1J8ff7N441J2p29F12C0ZA4GDE85X4QY8DRS1X6"  # Default test address
        
        print(f"\n🔍 Debug mode: Testing address {test_address}")
        
        try:
            url = f"{checker.base_url}{test_address}"
            print(f"📡 API URL: {url}")
            
            response = checker.session.get(url, timeout=10)
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📋 Full API Response:")
                print(json.dumps(data, indent=2))
                
                # Test our parsing logic
                result = checker.get_balance(test_address, "Debug Test")
                print(f"\n✅ Parsed Result:")
                print(json.dumps(result, indent=2))
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Debug error: {e}")
        
        return
    
    else:
        print("❌ Invalid choice")
        return
    
    if not wallets:
        print("❌ No wallets loaded. Exiting.")
        return
    
    # Ask about debug mode for problematic addresses
    debug_choice = input(f"\nFound {len(wallets)} wallets. Enable debug output for failed addresses? (y/n): ").strip().lower()
    debug_mode = debug_choice in ['y', 'yes']
    
    # Check balances
    results = checker.check_wallets_from_list(wallets, delay=0.1, debug_mode=debug_mode)
    
    # Display results
    checker.print_results(results)
    
    # Ask if user wants to export results
    export_choice = input("\nDo you want to export results to files? (y/n): ").strip().lower()
    if export_choice in ['y', 'yes']:
        filename = input("Enter filename (without extension): ").strip()
        if not filename:
            filename = 'stx_balance_report'
        checker.export_results(results, filename)

if __name__ == "__main__":
    main()