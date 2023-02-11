from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



b1 = KeyboardButton(text='🔤 Написать всем')
kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

support = InlineKeyboardButton(text='💌 Связаться', url='https://t.me/pijawca')
reviews = InlineKeyboardButton(text='🤝🏻 Отзывы', url='https://t.me/+xjK57xE6ffY4ZDBi')

a1 = KeyboardButton(text='⚙️ Администрирование')
a2 = KeyboardButton(text='🦾 Железяки')
back = KeyboardButton(text='Назад')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

#
kb_admin.insert(b1).add(back)
kb_client.insert(support).insert(reviews).insert(a1).add(a2)
kb_support = InlineKeyboardMarkup().insert(support)
kb_reviews = InlineKeyboardMarkup().insert(reviews)
