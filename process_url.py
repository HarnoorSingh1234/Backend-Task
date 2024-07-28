import os
from googlesearch import search
from google.oauth2 import service_account
from googleapiclient.discovery import build
from tqdm import tqdm

# Define your spreadsheet details
INPUT_SPREADSHEET_ID = '1zuGXEkV_Fk0WwbYj4lG369w0Xfgfz1-qgYIlWny7MG8'
OUTPUT_SPREADSHEET_ID = '1d4CcTH3-6knoZsZmxtZVRx473MtjwSNsnxbmQra6EnI'
RANGE_NAME = 'Input NBFC!A1:B15'
OUTPUT_RANGE = 'Output_Sheet!A1:C15'

def authenticate_sheets():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'Credentials.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=credentials).spreadsheets()

def search_official_website(name):
    query = f"{name} official website"
    for result in search(query):
        return result
    return "No URL found"

def process_urls():
    sheets = authenticate_sheets()
    result = sheets.values().get(spreadsheetId=INPUT_SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        output_values = [["Sr No", "Name", "Website"]]
        for row in tqdm(values[1:], desc="Processing rows"):
            if len(row) >= 2:
                sr_no, name = row[0], row[1]
                website = search_official_website(name)
                output_values.append([sr_no, name, website])
                print(f'{sr_no}, {name}, {website}')
            else:
                output_values.append([row[0], row[1] if len(row) > 1 else "", ""])

        body = {'values': output_values}
        sheets.values().update(
            spreadsheetId=OUTPUT_SPREADSHEET_ID,
            range=OUTPUT_RANGE,
            valueInputOption="RAW",
            body=body
        ).execute()
        print('Data successfully written to output sheet.')

if __name__ == '__main__':
    process_urls()
