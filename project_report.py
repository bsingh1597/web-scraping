import requests

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
    
    if response.status_code == 200:

        local_file_path = 'project-list-a.xlsx'

    # Save the content of the response to the local file
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        

        print('File "project-list-a.xlsx" has been created and written successfully.')
    else:
        print(f'API request failed with status code {response.status_code}')
