from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from influxdb_client import InfluxDBClient
import asyncio

TOKEN: Final = '7422813490:AAHtBSdeKG-oowNewgYb75ddwFVv6DG328A'
BOT_USERNAME: Final = '@doctor_stancu_bot'

# Configure InfluxDB client
influxdb_url = 'https://eu-central-1-1.aws.cloud2.influxdata.com/'
influxdb_token = 'KSoF1EdRhOSDo7ZVDpEsl8br2uTXJjqZoO44NToR6stN56WS1lECGOgH80-lgilTLecZEApWKeHid1FsKnsDtQ=='
influxdb_org = 'DraftPractica'
bucket = 'BazaDeDate'

client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
query_api = client.query_api()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! What information would you like to know?")

async def get_latest_value(field: str) -> str:
    query = f'''
    from(bucket: "{bucket}")
        |> range(start: -1h)
        |> filter(fn: (r) => r["_measurement"] == "Parametri" and r["_field"] == "{field}")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: 1)
    '''
    result = query_api.query(org=influxdb_org, query=query)
    
    points = []
    for table in result:
        for record in table.records:
            points.append(record.get_value())

    if points:
        latest_value = points[0]
        return f"Latest {field.replace('_', ' ')}: {latest_value}"
    else:
        return f"No data found for {field.replace('_', ' ')}"

async def ritmcardiac_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await get_latest_value("ritm_cardiac")
    await update.message.reply_text(response)

async def saturatieoxigen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await get_latest_value("saturatie_oxigen")
    await update.message.reply_text(response)

def main():
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('ritmcardiac', ritmcardiac_command))
    application.add_handler(CommandHandler('saturatieoxigen', saturatieoxigen_command))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
