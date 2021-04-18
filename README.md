# NiceCode Telegram Bot

# Content
-   [Content](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#content)
-   [Setup](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#setup)
-   [Input bot-token](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#input-your-bot-token-to-project)
-   [SSH key](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#ssh-key-for-server-connection)
-   [Start with Docker](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#start-with-docker)
-   [How to use Django Admin](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#how-to-use-django-admin)
-   [How to use this bot](https://gitlab.nicecode.biz/korneev.r/telebot-3/-/blob/readme-fixes/README.md#how-to-use-this-bot)

##  Setup
-   open terminal:
    - `mkdir nc-bot`
    - `cd nc-bot`
    - `git clone https://github.com/shaggy-axel/mserver_bot.git`
    - `touch .env`
-   copy paste from env_sample to `.env` and change values for you

##  Input your bot-token to project
-   [@BotFather](https://telegram.me/BotFather)
-   text him: 
            
        -   `/newbot`
        -   Bot Name
        -   username_bot
        -   Use this token to access the HTTP API: `your_token`
-   copy your bot-token and paste to `.env`

##  SSH key for server connection
-   your ssh keys have to save in `src/db`

##  Start with docker
-   back to terminal
    -   `cd nc-bot/telebot-3`
    -   `docker-compose up`

##  How to Use Django Admin
-   go to `0.0.0.0:8080/admin`
-   login: `username`
-   password: `password`
-   you can add your server in `Bot servers +Add`
-   put your username, host and `filename.key`(which must be in `src/db`)

##  How to Use this bot
-   text `/start` for start and get commands
-   text `/subscribe` for Subscribe on message
-   for help text `/help` and get commands


