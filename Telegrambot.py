from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import bot_handlers.handlers as handlers
import configs.configs as configs
import configs.database as db

class Telegrambot:
    
    # Start bot 
    def __init__(self, token):
        db.create_tables()
        self.token = token
        self.app = Application.builder().token(self.token).build()
        self.run()
        
    def run(self):
        handlers.addHandlers(self.app)
        self.app.run_polling()
    
if __name__ == "__main__":
    bot = Telegrambot(configs.KEY_BOT)