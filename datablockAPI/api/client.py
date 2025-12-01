"""
D&B Direct+ API Client
Handles authentication and data block requests to D&B Direct+ API.
"""

import os
import requests
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
import json

from datablockAPI.exceptions import AuthenticationError, RateLimitError, APIError


class DNBAPIClient:
    """Client for D&B Direct+ Data Blocks API."""
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, 
                 api_url: Optional[str] = None):
        """
        Initialize D&B API client.
        
        Args:
            api_key: D&B API key (reads from DNB_API_KEY env var if not provided)
            api_secret: D&B API secret (reads from DNB_API_SECRET env var if not provided)
            api_url: D&B API base URL (reads from DNB_API_URL env var if not provided)
        """
        self.api_key = api_key or os.getenv('DNB_API_KEY')
        self.api_secret = api_secret or os.getenv('DNB_API_SECRET')
        self.api_url = api_url or os.getenv('DNB_API_URL', 'https://plus.dnb.com')
        
        if not self.api_key or not self.api_secret:
            raise ValueError(
                "API credentials not provided. Set DNB_API_KEY and DNB_API_SECRET "
                "environment variables or pass them to the constructor."
            )
        
        self.access_token = None
        self.token_expiry = None
        self.session = requests.Session()
    
    def init_database(self, database_path: str, create_if_not_exists: bool = True):
        """
        Initialize the database connection. Creates database and tables if they don't exist.
        If database already exists, connects to it and ensures all tables are present.
        
        Args:
            database_path: Path to SQLite database file (required)
            create_if_not_exists: Whether to create database if it doesn't exist (default: True)
        
        Example:
            >>> client = DNBAPIClient()
            >>> client.init_database('datablock.db')  # Creates/connects to datablock.db
            >>> client.init_database('production.db', create_if_not_exists=False)  # Must exist
        """
        import datablockAPI as api
        import os
        
        db_url = f"sqlite:///{database_path}"
        
        # Check if database file exists
        db_exists = os.path.exists(database_path)
        
        if db_exists:
            print(f"📍 Connecting to existing database: {database_path}")
        elif create_if_not_exists:
            print(f"🆕 Creating new database: {database_path}")
        else:
            raise FileNotFoundError(f"Database {database_path} does not exist and create_if_not_exists=False")
        
        # Initialize database (creates tables if they don't exist)
        api.init(database=db_url)
        
        if db_exists:
            print(f"✓ Connected to database: {database_path}")
        else:
            print(f"✓ Database created: {database_path}")
    
    def get_session(self):
        """
        Get a SQLAlchemy session for database queries.
        
        Returns:
            SQLAlchemy session object
        
        Example:
            >>> session = client.get_session()
            >>> companies = session.query(Company).all()
        """
        import datablockAPI as api
        return api.get_session()
    
    def authenticate(self) -> str:
        """
        Authenticate with D&B API and get access token.
        Uses Basic Authentication with API key and secret.
        
        Returns:
            Access token string
        """
        import base64
        
        auth_url = f"{self.api_url}/v3/token"
        
        # Create Basic Auth header with base64 encoded key:secret
        credentials = f"{self.api_key}:{self.api_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Use form data instead of JSON
        payload = {
            'grant_type': 'client_credentials'
        }
        
        try:
            response = self.session.post(auth_url, data=payload, headers=headers)
            response.raise_for_status()
            
            auth_data = response.json()
            self.access_token = auth_data.get('access_token')
            
            # Token typically expires in 24 hours
            expires_in = auth_data.get('expiresIn', 86400)
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
            
            print(f"✓ Authenticated successfully")
            # logger.info(f"✓ Authenticated successfully. Token expires at {self.token_expiry}")
            # record_api_call("authenticate", success=True)
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            # Show more detailed error info
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code
                if status_code == 401:
                    raise AuthenticationError(f"Authentication failed: Invalid credentials")
                elif status_code == 429:
                    raise RateLimitError(f"Rate limit exceeded")
                else:
                    raise APIError(f"Authentication failed with status {status_code}: {e}")
            else:
                raise APIError(f"Authentication failed: {e}")
    
    def _ensure_authenticated(self):
        """Ensure we have a valid access token."""
        if not self.access_token or not self.token_expiry or datetime.now() >= self.token_expiry:
            self.authenticate()
    
    def request_data_blocks(self, duns_number: str, block_ids: List[str], output_dir: str = "dnb_data") -> Dict[str, Any]:
        """
        Request specific data blocks from D&B API and save to JSON files.
        
        Args:
            duns_number: 9-digit DUNS number
            block_ids: List of specific block IDs to request (e.g., ['companyinfo_L2_v1', 'companyfinancial_L1_v1'])
            output_dir: Directory to save JSON files (default: 'dnb_data')
        
        Returns:
            Dictionary with API response data
        
        Example:
            >>> client = DNBAPIClient()
            >>> data = client.request_data_blocks('540924028', ['companyinfo_L2_v1'])
            >>> # Requests only company info and saves to dnb_data/
        """
        # Validate inputs
        if not duns_number or not duns_number.isdigit() or len(duns_number) != 9:
            raise ValueError("DUNS number must be a 9-digit string")
        
        if not block_ids:
            raise ValueError("At least one block ID must be specified")
        
        # Ensure we have a valid access token
        self._ensure_authenticated()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Prepare API request
        url = f"{self.api_url}/v1/data/duns/{duns_number}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        params = {
            'blockIDs': ','.join(block_ids)
        }
        
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            # Handle authentication errors by retrying once
            if hasattr(e, 'response') and e.response and e.response.status_code == 401:
                print("Token expired, re-authenticating...")
                self.access_token = None  # Force re-authentication
                self._ensure_authenticated()
                # Retry the request
                response = self.session.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                return data
            elif hasattr(e, 'response') and e.response and e.response.status_code == 404:
                # Handle unavailable data blocks gracefully
                block_id = block_ids[0] if len(block_ids) == 1 else ','.join(block_ids)
                print(f"⚠️ Block(s) {block_id} not available")
                return {}
            else:
                raise Exception(f"API request failed: {e}")

    def request_company_info(self, duns_number: str, output_dir: str = "dnb_data") -> Dict[str, Any]:
        """
        Request company information data block and save raw JSON response to local file.

        Args:
            duns_number: 9-digit DUNS number
            output_dir: Directory to save JSON file (default: 'dnb_data')

        Returns:
            Raw API response data
        """
        data = self.request_data_blocks(duns_number, ['companyinfo_L2_v1'], output_dir)

        # Save the complete raw API response to JSON file
        filename = f"{duns_number}_companyinfo_L2_v1.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved raw response to {filepath}")

        return data
    
    def request_company_financials(self, duns_number: str, output_dir: str = "dnb_data") -> Dict[str, Any]:
        """
        Request company financial data block and save raw JSON response to local file.

        Args:
            duns_number: 9-digit DUNS number
            output_dir: Directory to save JSON file (default: 'dnb_data')

        Returns:
            Raw API response data
        """
        data = self.request_data_blocks(duns_number, ['companyfinancial_L1_v1'], output_dir)

        # Save the complete raw API response to JSON file
        filename = f"{duns_number}_companyfinancial_L1_v1.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved raw response to {filepath}")

        return data
    
    def request_events_filings(self, duns_number: str, output_dir: str = "dnb_data") -> Dict[str, Any]:
        """
        Request events and filings data block and save raw JSON response to local file.

        Args:
            duns_number: 9-digit DUNS number
            output_dir: Directory to save JSON file (default: 'dnb_data')

        Returns:
            Raw API response data
        """
        data = self.request_data_blocks(duns_number, ['eventfilings_L3_v1'], output_dir)

        # Save the complete raw API response to JSON file
        filename = f"{duns_number}_eventfilings_L3_v1.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved raw response to {filepath}")

        return data
    
    def request_all_data(self, duns_number: str, output_dir: str = "dnb_data") -> Dict[str, Any]:
        """
        Request all common data blocks and save each to separate JSON files.
        
        Args:
            duns_number: 9-digit DUNS number
            output_dir: Directory to save JSON files (default: 'dnb_data')
        
        Returns:
            Dictionary containing all response data
        """
        results = {}
        
        # Request each data block separately and save to individual files
        results['companyinfo'] = self.request_company_info(duns_number, output_dir)
        results['companyfinancial'] = self.request_company_financials(duns_number, output_dir)
        results['eventfilings'] = self.request_events_filings(duns_number, output_dir)
        
        return results
    
    def _load_recent_files_to_db(self, output_dir: str = "dnb_data", max_files: int = 10):
        """
        Load recently created JSON files into the database.
        This is called automatically by request_and_load().
        
        Args:
            output_dir: Directory containing JSON files (default: 'dnb_data')
            max_files: Maximum number of recent files to load (default: 10)
        """
        import datablockAPI as api
        import glob
        from pathlib import Path
        
        # Find JSON files in the specified directory
        json_files = glob.glob(f'{output_dir}/*.json')
        if not json_files:
            print(f"⚠️ No JSON files found in {output_dir} directory")
            return
        
        # Sort by modification time (most recent first)
        json_files.sort(key=lambda x: Path(x).stat().st_mtime, reverse=True)
        
        # Load the most recent files (up to max_files)
        files_to_load = json_files[:max_files]
        
        print(f"📥 Loading {len(files_to_load)} recent JSON files from {output_dir} to database...")
        for json_file in files_to_load:
            print(f"  Loading: {Path(json_file).name}")
        
        api.load(files_to_load)
        print("✓ Data loaded to database")
    def load_json_to_db(self, json_files: Union[str, List[str]]):
        """
        Load JSON files into the database.
        
        Args:
            json_files: Single JSON file path or list of JSON file paths
        
        Example:
            >>> client.load_json_to_db('dnb_data/540924028_companyinfo_20241127_120000.json')
            >>> client.load_json_to_db(['file1.json', 'file2.json'])
        """
        import datablockAPI as api
        
        print(f"📥 Loading JSON files to database...")
        api.load(json_files)
        print("✓ Data loaded to database")


def main():
    """Example usage of DNB API client."""
    import argparse
    
    parser = argparse.ArgumentParser(description='D&B Direct+ API Client')
    parser.add_argument('duns', help='DUNS number to query')
    parser.add_argument('--blocks', nargs='+', 
                       default=['companyinfo_L2_v1', 'eventfilings_L3_v1', 'companyfinancial_L1_v1'],
                       help='Block IDs to request')
    parser.add_argument('--trade-up', choices=['hq', 'domhq'], help='Trade up parameter')
    parser.add_argument('--reference', help='Customer reference string')
    parser.add_argument('--output-dir', default='dnb_data', help='Output directory for JSON files')
    parser.add_argument('--no-save', action='store_true', help='Do not save to file')
    
    args = parser.parse_args()
    
    try:
        client = DNBAPIClient()
        
        data = client.get_data_blocks(
            duns_number=args.duns,
            block_ids=args.blocks,
            trade_up=args.trade_up,
            customer_reference=args.reference,
            save_to_file=not args.no_save,
            output_dir=args.output_dir
        )
        
        # Print summary
        org = data.get('organization', {})
        print(f"\n{'='*60}")
        print(f"Company: {org.get('primaryName', 'N/A')}")
        print(f"DUNS: {org.get('duns', 'N/A')}")
        print(f"Country: {org.get('countryISOAlpha2Code', 'N/A')}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
