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
            
            # Extract balance information
            balance_ustx = int(data['balance']['stx']['balance'])
            locked_ustx = int(data['balance']['stx'].get('locked', 0))
            
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
            return {
                'name': name or 'Unknown',
                'address': address,
                'error': f"HTTP Error: {err}",
                'success': False
            }
        except requests.exceptions.RequestException as err:
            return {
                'name': name or 'Unknown',
                'address': address,
                'error': f"Network Error: {err}",
                'success': False
            }
        except (KeyError, ValueError) as err:
            return {
                'name': name or 'Unknown',
                'address': address,
                'error': f"Data parsing error: {err}",
                'success': False
            }
    
    def check_wallets_from_list(self, wallets: List[Dict[str, str]], delay: float = 0.1) -> List[Dict]:
        """
        Check balances for wallets from loaded list
        
        Args:
            wallets: List of wallet dictionaries with 'name' and 'address'
            delay: Delay between requests in seconds
            
        Returns:
            List of balance dictionaries
        """
        results = []
        
        print(f"🔍 Checking balances for {len(wallets)} wallets...")
        
        for i, wallet in enumerate(wallets):
            print(f"   Checking {i+1}/{len(wallets)}: {wallet['name']}")
            result = self.get_balance(wallet['address'], wallet['name'])
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
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
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
    
    else:
        print("❌ Invalid choice")
        return
    
    if not wallets:
        print("❌ No wallets loaded. Exiting.")
        return
    
    # Check balances
    results = checker.check_wallets_from_list(wallets, delay=0.1)
    
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
    