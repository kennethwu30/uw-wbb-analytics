import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ============================================
# TEMPLATE: CONNECT TO GOOGLE SHEETS
# ============================================


def read_sheet(sheet_name, tab_name='Sheet1'):
    """
    Reads data from Google Sheets into a pandas DataFrame

    Args:
        sheet_name: Name of your Google Sheet (e.g., 'WBB')
        tab_name: Name of the tab/worksheet (default: 'Sheet1')

    Returns:
        df: pandas DataFrame with your data
        spreadsheet: spreadsheet object (needed for writing back)
    """
    # Setup credentials
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file(
        'credentials.json', scopes=scopes)
    client = gspread.authorize(creds)

    # Open spreadsheet and get data
    spreadsheet = client.open(sheet_name)
    sheet = spreadsheet.worksheet(tab_name)
    data = sheet.get_all_records(head=3)
    df = pd.DataFrame(data)

    # Clean column names (remove extra spaces)
    df.columns = df.columns.str.strip()

    return df, spreadsheet


# ============================================
# TEMPLATE: WRITE BACK TO GOOGLE SHEETS
# ============================================

def write_sheet(df, spreadsheet, output_tab_name='Analysis'):
    """
    Writes pandas DataFrame back to Google Sheets

    Args:
        df: pandas DataFrame to write
        spreadsheet: spreadsheet object from read_sheet()
        output_tab_name: Name of tab to write to (default: 'Analysis')
    """
    # Try to get existing sheet, or create new one
    try:
        output_sheet = spreadsheet.worksheet(output_tab_name)
        print(f"✅ Found existing '{output_tab_name}' sheet")
    except:
        output_sheet = spreadsheet.add_worksheet(
            title=output_tab_name, rows=100, cols=20)
        print(f"✅ Created new '{output_tab_name}' sheet")

    # Clear existing data
    output_sheet.clear()

    # Convert DataFrame to format Google Sheets understands
    data_to_write = [df.columns.values.tolist()] + df.values.tolist()

    # Write to sheet
    output_sheet.update('A1', data_to_write)
    print(f"✅ Data written to '{output_tab_name}' tab!")
    print(
        f"📊 View it: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
