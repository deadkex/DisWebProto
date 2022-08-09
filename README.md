# Discord OAuth2 Website Prototype

### Simple OAuth2 example which shows:
- how to use the discord login authentication  
- display the user's guilds in a select
- create a role with a custom name in the selected guild

### Dependencies:
- [Python](https://www.python.org/downloads/) Version >= 3.10
- all packages in requirements.txt

### Setup:
- Create an application https://discord.com/developers/applications
  - In OAuth2 settings
    - reset/copy the client secret
    - copy client id
    - set the redirect to `http://localhost:63883/login`
  - Create a bot
    - reset/copy bot token
- Fill data in dwp_secrets.py

### Oauth2 workflow:  
- authorize discord login page -> get code -> get access_token + refresh_token
- the access_token gets saved in an encrypted cookie

### Credit
This project was made to claim a bounty fom [@BoredManCodes](https://github.com/BoredManCodes)