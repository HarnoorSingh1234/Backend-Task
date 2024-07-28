from google.oauth2 import service_account
from googleapiclient.discovery import build

INPUT_SPREADSHEET_ID = '1zuGXEkV_Fk0WwbYj4lG369w0Xfgfz1-qgYIlWny7MG8'
OUTPUT_SPREADSHEET_ID = '1d4CcTH3-6knoZsZmxtZVRx473MtjwSNsnxbmQra6EnI'
RANGE_NAME = 'Input NBFC!A1:I15'
OUTPUT_RANGE = 'Output_Sheet!A1:F15'

def authenticate_sheets():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'Credentials.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=credentials).spreadsheets()

def add_additional_data():
    sheets = authenticate_sheets()
    result = sheets.values().get(spreadsheetId=INPUT_SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        output_values = [["Sr No", "Name", "Website", "Regional Office", "Address", "Email ID"]]

        for row in values[1:]:
            if len(row) >= 9:
                sr_no, name, website = row[0], row[1], row[2]
                regional_office = row[2]
                address = row[7]
                email_id = row[8]
                output_values.append([sr_no, name, website, regional_office, address, email_id])
                print(f'{sr_no}, {name}, {website}, {regional_office}, {address}, {email_id}')
            else:
                output_values.append([row[0], row[1] if len(row) > 1 else "", "", "", "", ""])

        body = {'values': output_values}
        sheets.values().update(
            spreadsheetId=OUTPUT_SPREADSHEET_ID,
            range=OUTPUT_RANGE,
            valueInputOption="RAW",
            body=body
        ).execute()
        print('Additional data successfully written to output sheet.')

if __name__ == '__main__':
    add_additional_data()
