# load the cookie string from the file
with open('cookies.txt', 'r') as file:
    cookie_string = file.read()

# Split the cookie string by ';' to get individual cookies
individual_cookies = cookie_string.split(';')

# Initialize an empty list to store cookie dictionaries
cookies = []

# Iterate over each cookie
for cookie in individual_cookies:
    # Trim leading and trailing spaces
    trimmed_cookie = cookie.strip()
    # Split each cookie into name and value
    name, value = trimmed_cookie.split('=', 1)
    # Create a dictionary with name and value and append to the list
    cookies.append({'name': name, 'value': value})

# Print the list of cookie dictionaries
print(cookies)
