from telegram.ext import CommandHandler, MessageHandler, filters, Application, ConversationHandler
from telegram import Update
import configs.database as db
import configs.configs as conf
import requests

# States for conversation handlers
CITY = 1

# weather API url and key
weather_api_key = conf.WEATHER_API_KEY

# Create commands 
# Ex: "/start"

# Functions ======================================================================

async def start(update: Update, context):
    
    # Get user ID
    user_id = update.effective_user.id
    if db.user_exists(user_id) == 1: await update.message.reply_text("Bem Vindo Novamente!"
                                                                     "\n\nPara ver o clima em sua cidade, utilize /clima"
                                                                     "\nPara criar um novo avento na agenda, utilize /novoEvento")
    else:
        await update.message.reply_text("Bem Vindo! Sou seu assistente diário para informações como clima e eventos, é um prazer!\n"
                                        "Vamos iniciar seu cadastro, preciso que informe o nome de sua cidade!")
        return CITY
    
async def addUser(update: Update, context):
    user_city = update.message.text
    city_response = f"http://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={weather_api_key}"
    
    # Valid City
    if requests.get(city_response).status_code == 200:
        user_id = update.effective_user.id
        db.new_user(user_id, user_city)
        await update.message.reply_text(f"Seu cadastro foi concluido {update.effective_user.name} com sucesso para a cidade ({user_city})!"
                                        "\n\nVocê pode utilizar o comando /start para verificar todos os comandos!")
        return
        
    # Invalid City or Error
    else: 
        await update.message.reply_text(f"Cidade ({user_city}) não foi encontrada, por favor tente novamente")
        return CITY
    
async def weather(update: Update, context):
    user_id = update.effective_user.id
    if not db.user_exists(user_id): 
        await update.message.reply_text("Parece que você ainda não possui um cadastro"
                                        ", digite /start para iniciar seu cadastro.")
        return
    user_city = db.getCity(user_id)
    weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={weather_api_key}&lang=pt"
    print(f"Busca na cidade {user_city}")
    response = requests.get(weather_api_url)
    if response.status_code != 200:
        await update.message.reply_text(f"Algo deu errado ao buscar pela cidade {user_city}, por favor tente novamente.")
        return
    data = response.json()
    
    temp = data["main"]["temp"] - 273.15 # Kelvin to Celsius
    description = data["weather"][0]["description"]
    
    await update.message.reply_text(f"O clima em {user_city} atualmente é {description} com temperatura de "
                                    f"{temp:.2f}°C.")
    
async def newEvent(update: Update, context):
    return

#=================================================================================

# create all commands
def addHandlers(app : Application) -> None:
    
    # Add a conversationhandler to create user
    conversation_handler_createUser = ConversationHandler(
        # /start command
        entry_points=[CommandHandler("start", start)],
        states={
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, addUser)],
        },
        fallbacks=[]
    )
    
    # Add conversation cicle
    app.add_handler(conversation_handler_createUser)
    # Add /clima command
    app.add_handler(CommandHandler("clima", weather))
    
    # Add diary commands
    app.add_handler(CommandHandler("NovoEvento", newEvent))