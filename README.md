# NiceCode Telegram Bot

# Content
-   [Content](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#content)
-   [Setup](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#setup)
-   [Input bot-token](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#input-your-bot-token-to-project)
-   [SSH key](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#ssh-key-for-server-connection)
-   [Start bot](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#start-bot-app)
-   [How to use this bot](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#how-to-use-this-bot)

##  Setup
-   open terminal:
    - `mkdir nc-bot`
    - `cd nc-bot`
    - `git clone https://github.com/shaggy-axel/mserver_bot.git`
    - `pip install -r requirements.txt`

##  Input your bot-token to project
-   [@BotFather](https://telegram.me/BotFather)
-   text him: 
            
        -   `/newbot`
        -   Bot Name
        -   username_bot
        -   Use this token to access the HTTP API: `your_token`

-   create `db_keys.json` in `/src/db`
-   copy code from `template_db_keys.json` and paste to `db_keys.json`
-   copy your bot-token and paste to `"telegrambot": "your bot token!!!"`

##  SSH key for server connection
-   rename your ssh key to `bot.key`
-   put into `/src/db`
-   also input your host and username

##  Start bot-app
-   back to terminal
    -   `cd src`
    -   `python3 bot.py`

##  How to Use this bot
-   text `/start` for start and get commands
-   text `/password` for Subscribe on message
-   for help text `/help` and get commands


