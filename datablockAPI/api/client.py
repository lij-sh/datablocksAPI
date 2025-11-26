"""
D&B Direct+ API Client
Handles authentication and data block requests to D&B Direct+ API.
"""

import os
import requests
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json


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
            
            print(f"✓ Authenticated successfully. Token expires at {self.token_expiry}")
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            # Show more detailed error info
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
            raise Exception(f"Authentication failed: {e}")
    
    def _ensure_authenticated(self):
        """Ensure we have a valid access token."""
        if not self.access_token or not self.token_expiry or datetime.now() >= self.token_expiry:
            self.authenticate()
    
    def get_data_blocks(
        self,
        duns_number: str,
        block_ids: List[str],
        trade_up: Optional[str] = None,
        customer_reference: Optional[str] = None,
        save_to_file: bool = False,
        output_dir: str = "dnb_data"
    ) -> Dict[str, Any]:
        """
        Get data blocks for a DUNS number.
        
        Args:
            duns_number: 9-digit DUNS number
            block_ids: List of block IDs to request (e.g., ['companyinfo_L2_v1', 'eventfilings_L3_v1'])
            trade_up: Optional trade up parameter ('hq' or 'domhq')
            customer_reference: Optional reference string (up to 240 chars)
            save_to_file: Whether to save response to JSON file
            output_dir: Directory to save JSON files (if save_to_file=True)
        
        Returns:
            Dictionary with API response data
        
        Example:
            >>> client = DNBAPIClient()
            >>> data = client.get_data_blocks(
            ...     duns_number='540924028',
            ...     block_ids=['companyinfo_L2_v1', 'eventfilings_L3_v1'],
            ...     save_to_file=True
            ... )
        """
        self._ensure_authenticated()
        
        # Build URL
        url = f"{self.api_url}/v1/data/duns/{duns_number}"
        
        # Build query parameters
        params = {
            'blockIDs': ','.join(block_ids)
        }
        
        if trade_up:
            if trade_up not in ['hq', 'domhq']:
                raise ValueError("trade_up must be 'hq' or 'domhq'")
            params['tradeUp'] = trade_up
        
        if customer_reference:
            if len(customer_reference) > 240:
                raise ValueError("customer_reference must be 240 characters or less")
            params['customerReference'] = customer_reference
        
        # Build headers
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json'
        }
        
        try:
            print(f"\n📡 Requesting data blocks for DUNS {duns_number}...")
            print(f"   Block IDs: {', '.join(block_ids)}")
            
            response = self.session.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            print(f"✓ Data retrieved successfully")
            
            # Save to file if requested
            if save_to_file:
                os.makedirs(output_dir, exist_ok=True)
                
                # Determine filename based on block IDs
                block_names = '_'.join([bid.split('_')[0] for bid in block_ids])
                filename = f"{duns_number}_{block_names}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"✓ Saved to: {filepath}")
            
            return data
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise Exception("Authentication failed. Check your API credentials.")
            elif response.status_code == 404:
                raise Exception(f"DUNS {duns_number} not found or you don't have access.")
            else:
                raise Exception(f"API request failed: {e}\n{response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {e}")
    
    def get_company_info(self, duns_number: str, save_to_file: bool = False) -> Dict[str, Any]:
        """
        Get company information data block.
        
        Args:
            duns_number: 9-digit DUNS number
            save_to_file: Whether to save response to JSON file
        
        Returns:
            Company information data
        """
        return self.get_data_blocks(
            duns_number=duns_number,
            block_ids=['companyinfo_L2_v1'],
            save_to_file=save_to_file
        )
    
    def get_events_filings(self, duns_number: str, save_to_file: bool = False) -> Dict[str, Any]:
        """
        Get events and filings data block.
        
        Args:
            duns_number: 9-digit DUNS number
            save_to_file: Whether to save response to JSON file
        
        Returns:
            Events and filings data
        """
        return self.get_data_blocks(
            duns_number=duns_number,
            block_ids=['eventfilings_L3_v1'],
            save_to_file=save_to_file
        )
    
    def get_financials(self, duns_number: str, save_to_file: bool = False) -> Dict[str, Any]:
        """
        Get financial data block.
        
        Args:
            duns_number: 9-digit DUNS number
            save_to_file: Whether to save response to JSON file
        
        Returns:
            Financial data
        """
        return self.get_data_blocks(
            duns_number=duns_number,
            block_ids=['companyfinancial_L1_v1'],
            save_to_file=save_to_file
        )
    
    def get_all_blocks(self, duns_number: str, save_to_file: bool = True) -> Dict[str, Any]:
        """
        Get all common data blocks (company info, events/filings, financials).
        
        Args:
            duns_number: 9-digit DUNS number
            save_to_file: Whether to save response to JSON file
        
        Returns:
            Complete data with all blocks
        """
        return self.get_data_blocks(
            duns_number=duns_number,
            block_ids=[
                'companyinfo_L2_v1',
                'eventfilings_L3_v1',
                'companyfinancial_L1_v1'
            ],
            save_to_file=save_to_file
        )


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
