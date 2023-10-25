import requests
import openpyxl
from unidecode import unidecode

login_url = "https://data.archwaypartnership.uga.edu/user/login"

# Form data as a dictionary
form_data = {
    "name": "bs83243",
    "pass": "Arch@4269112",
    "op": "Log in",
    "form_id": "user_login_form",
}

login_header = {"Content-Type": "application/x-www-form-urlencoded"}

login_response = requests.post(login_url, headers=login_header, data=form_data)

session_cookie =""

if login_response.status_code == 200:
    cookies = login_response.history[0].cookies
    
    for cookie in cookies:
        print(f"Name: {cookie.name} :: Val: {cookie.value}")
        session_cookie = f"{cookie.name}={cookie.value}"
else:
    print("Login Failed")

if(len(session_cookie) > 0):
    excel_url = "https://data.archwaypartnership.uga.edu/projects/project-list/export?combine=&amp;field_start_end_date_value%5Bmin%5D=June%201st%2C2017&amp;field_start_end_date_value%5Bmax%5D=&amp;field_project_member_multiref_target_id=&amp;field_semester_code=&amp;page&amp;_format=txt"

    headers = {
    'Cookie': session_cookie
    }

    response = requests.request("GET", excel_url, headers=headers)
    
    # if response.status_code == 200:
    #     print(response.headers)
    #     cookies = response.cookies
    
    #     print(response.text)
    
    #     with open('test.xlsx', 'w', encoding='utf-8') as file:
    #         file.write(response.text)

    #     print('File "example.txt" has been created and written successfully.')
    # else:
    #     print("REquest for Excel failed")
    
    if response.status_code == 200:

        # Create a new workbook and select the active sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        
         # Encode response text to UTF-8 before writing to the worksheet
        # cleaned_text = clean_string(encoded_text.decode('utf-8'))

        try:
            sheet['A1'] =  unidecode(response.text)
        except Exception as e:
            print(f'Exception: {e}')

        # Save the workbook to a file
        workbook.save('api_response.xlsx')

        print('API response saved to "api_response.xlsx" successfully.')
    else:
        print(f'API request failed with status code {response.status_code}')
        print('Response:', response.text)
