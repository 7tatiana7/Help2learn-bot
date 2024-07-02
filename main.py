""" 
1. Подключение пакета telegram-bot к python
2. Создать ТГ бот через Bot-father
3. Получить секретный ключ для доступа к ТГ бота
4. Подключение к ТГ боту
5. Логика игры
  1. Приветствие
  2. Мануал
  3. Словарь
  4. Вопрос
  5. Варианты ответа
  6. Ответ игрока
  7. Обработка ответа
"""
import random

from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder
from telegram.ext import filters, ContextTypes
from telegram import ReplyKeyboardMarkup, Update

SECRET_KEY = "YOUR SECRET KEY HERE"

WORDS = {
'жыл' : 'год',
'адам' : 'человек',
'уақыт' : 'время',
'іс' : 'дело',
'өмір' : 'жизнь',
'күн' : 'день',
'қол' : 'рука',
'рет' : 'раз',
'жұмыс' : 'работа',
'сөз' : 'слово',
'орын' : 'место',
'бет' : 'лицо',
'дос' : 'друг',
'көз' : 'глаз',
'сұрақ' : 'вопрос',
'үй' : 'дом',
'жақ' : 'сторона',
'ел' : 'страна',
'әлем' : 'мир',
'оқиға' : 'случай',
'бас' : 'голова',
'бала' : 'ребёнок',
'күш' : 'сила',
'аяқ' : 'конец/нога',
'түр' : 'вид',
'жүйе' : 'система',
'бөлік' : 'часть',
'қала' : 'город',
'қатынас' : 'отношение',
'әйел' : 'женщина/жена',
'ақша' : 'деньги',
'жер' : 'земля',
'көлік' : 'машина',
'су' : 'вода',
'әке' : 'отец',
'мәселе' : 'проблема',
'сағат' : 'час',
'оң' : 'право',
'шешім' : 'решение',
'есік' : 'дверь',
'бейне' : 'образ',
'билік' : 'власть',
'заң' : 'закон',
'соғыс' : 'война',
'құдай' : 'бог',
'дауыс' : 'голос',
'мың' : 'тысяча',
'кітап' : 'книга',
'мүмкіндік' : 'возможность',
'нәтиже' : 'результат',
'түн' : 'ночь',
'үстел' : 'стол',
'ат/есім' : 'имя',
'облыс' : 'область',
'мақала' : 'статья',
'сан' : 'число',
'халық' : 'народ',
'топ' : 'группа',
'даму' : 'развитие',
'үдеріс' : 'процесс',
'сот' : 'суд',
'жағдай' : 'условие',
'құрал' : 'средство',
'бастау' : 'начало',
'жарық' : 'свет',
'кез' : 'пора',
'жол' : 'путь/дорога',
'жан' : 'душа',
'деңгей' : 'уровень',
'пішін' : 'форма',
'байланыс' : 'связь',
'минут' : 'минута',
'көше' : 'улица',
'кеш' : 'вечер',
'сапа' : 'качество',
'ой' : 'мысль',
'ана' : 'мать'
}
  
async def generate_question():
  options = random.sample(WORDS.keys(), 4)
  question = random.choice(options)
  correct_answer = WORDS[question]
  return options, question, correct_answer

async def handle_start(update, context):
  await update.message.reply_text(
    "Приветствую!"
  )
  await update.message.reply_text(
    "Вам будет дано слово на казахском языке и 4 варианта его перевода на русский язык. "
    "Выберите верный перевод."
  )

  await give_question(update, context)

async def give_question(update, context):
  options, question, correct_answer = await generate_question()

  translate_options = []
  for word in options: 
    translate_options.append(WORDS[word])

  keyboard = ReplyKeyboardMarkup.from_column(
    translate_options,
    one_time_keyboard=True,
    resize_keyboard=True
  )

  await update.message.reply_text(
    text=f'Переведите слово: "{question}"',
    reply_markup=keyboard
  )
  context.user_data['correct_answer'] = correct_answer

async def handle_answer(update, context):
  player_answer = update.effective_message.text
  correct_answer = context.user_data['correct_answer']

  if player_answer == correct_answer:
    await update.message.reply_text(
      "Верно!"
    )
  else:
    await update.message.reply_text(
      f'Неверно! Верный ответ - "{correct_answer}"'
    )

  await give_question(update, context)
  
app = ApplicationBuilder().token(SECRET_KEY).build()

app.add_handler(CommandHandler('start', handle_start))
app.add_handler(CommandHandler('restart', handle_start))
app.add_handler(MessageHandler(filters.TEXT, handle_answer))

app.run_polling()
