# ADAuthAPI

## Overview
ADAuthAPI is a custom-built RESTful API designed to facilitate seamless authentication 
against Active Directory (AD) for web applications and services. It aims to provide a 
straightforward and secure method for integrating AD authentication, simplifying the process 
for developers and enhancing security by minimizing direct interactions with AD servers.

## Features
- **User Authentication**: Allows web applications to authenticate users against an Active Directory server.
- **Group Validation**: Supports checking if authenticated users are members of specific AD security group, enabling role-based access control.

## Prerequisites
Before you begin, ensure you have the following:
- Access to an Active Directory server with permission to query user credentials.
- Python 3.10 or later installed on your server.

## Installation
To set up ADAuthAPI on your server, follow these steps on a typical windows server:

1. Create a or update the env.txt file in the deployment folder:
   ```sh
   SERVER_ADDRESS=192.168.1.10
   DOMAIN_NAME=xyz
   SEARCH_BASE=dc=xyz,dc=local
   GROUP_NAME=local-group
   ALLOWED_HOSTS=127.0.0.1,localhost
   
2. deploy the app to the server:
   ```sh
   rem assuming the app is location is d:\apps\adauthapi
   
   d:
   cd \apps\adauthapi
   
   rmdir /s /q .\api
   mkdir api 
   cd .\api
   git clone https://github.com/jcarter62/adauthapi.git  .
   copy ..\env.txt .\.env
   python.exe -m venv venv 
   .\venv\Scripts\pip.exe install -r requirements.txt 

    ```
3. Run the following command to start the API:
   ```sh
   rem assuming the app is installed in d:\apps\adauthapi
   rem and the ip address of the server is 192.168.1.123 and the port is 5110
   
   d:
   cd \apps\adauthapi\api
   .\venv\Scripts\uvicorn main:app --host=192.168.1.123 --port=5110
   
   ```
4. Test the API by sending a POST request to the following endpoint:
   ```sh
   http://192.168.1.123:5110/auth/local-group
   
   Curl example:
   curl --location 'http://192.168.1.123:5110/auth/local-group' \
   --header 'Content-Type: application/json' \
   --data '{ "username": "user", "password": "secret" }'
   ```   
5. If the request should respond with:is successful, you should receive a response with the user's details and a token.
* 200: username password success, member of group
* 206: username password success, not member of group
* 401: failure
 
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Dependencies
* fastapi
* pydantic
* uvicorn
* ldap3
* python_decouple
