import requests
import socket

def request_with_redirect_handling_and_ip(url):
    """
    Makes an HTTP request to a specified URL, handling redirects manually and attempting
    to resolve and print the IP address of the server for successful responses. 
    Includes comprehensive error handling for request errors and domain resolution failures.

    Parameters:
    - url: The URL to make the request to.

    Returns:
    A list of tuples, each containing a URL and its response status code.
    """
    
    # Initialize a list to record each URL visited and its response status code
    recorded_responses = []

    # Use a session object for persistent settings across requests
    with requests.Session() as session:
        try:
            # Attempt to make the initial request without following redirects
            response = session.get(url, allow_redirects=False)
        except requests.exceptions.RequestException as e:
            # Handle errors such as connectivity issues or invalid URLs
            print(f"Request error: {e}")
            return recorded_responses  # Return the empty list or partial data collected so far

        # Record the initial response
        recorded_responses.append((url, response.status_code))
        
        if response.status_code == 200:
            try:
                # Attempt to resolve the server's hostname to an IP address
                hostname = requests.utils.urlparse(response.url).hostname
                ip_address = socket.gethostbyname(hostname)
                print(f"URL: {response.url} - IP Address: {ip_address}")
            except socket.gaierror:
                # Handle the case where the hostname cannot be resolved
                print(f"Failed to resolve hostname: {hostname}")
        
        elif response.status_code in [301, 302]:
            # Handle HTTP redirects (status codes 301 and 302) by manually following the 'Location' header
            new_url = response.headers['Location']
            print(f"Redirecting to: {new_url}")
            try:
                # Attempt the redirected request
                new_response = session.get(new_url)
                recorded_responses.append((new_url, new_response.status_code))

                if new_response.status_code == 200:
                    try:
                        hostname = requests.utils.urlparse(new_response.url).hostname
                        ip_address = socket.gethostbyname(hostname)
                        print(f"URL: {new_response.url} - IP Address: {ip_address}")
                    except socket.gaierror:
                        print(f"Failed to resolve hostname: {hostname}")
            except requests.exceptions.RequestException as e:
                # Handle request errors during redirection
                print(f"Request error during redirect: {e}")
        
        elif 400 <= response.status_code < 500:
            # Print the client error encountered (4XX status codes)
            print(f"Error encountered: {response.status_code}")
    
    return recorded_responses

# Example usage
url = 'http://example.com'  # Adjust the URL as needed
responses = request_with_redirect_handling_and_ip(url)
for response_url, status_code in responses:
    print(f"URL: {response_url} - Status Code: {status_code}")