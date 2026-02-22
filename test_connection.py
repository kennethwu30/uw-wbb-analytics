import gspread
from google.oauth2.service_account import Credentials

# Setup
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_file(
    'credentials.json', scopes=scopes)
client = gspread.authorize(creds)

# Your sheet name
sheet_name = 'WBB'

try:
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()

    print("✅ Connected successfully!")
    print(f"Found {len(data)} rows")
    if data:
        print("\nFirst row:", data[0])
        print("\nColumn names:", list(data[0].keys()))
except Exception as e:
    print("❌ Error:", e)
    print("\nTroubleshooting:")
    print("1. Make sure you clicked 'Send' to share the sheet")
    print("2. Make sure credentials.json is in the same folder")
    print("3. Sheet name is case-sensitive: 'WBB'")
