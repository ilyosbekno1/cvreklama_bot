import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = "8447022335:AAFRZ0dbWeq70_gi2wxx1bxNFdz0k2at9Jg"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# CV uchun State (bosqichlar)
class CVForm(StatesGroup):
    name = State()
    age = State()
    skills = State()
    experience = State()
    location = State()
    email = State()
    phone = State()


# /start komandasi
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📄 CV yaratish")
    await message.answer("Assalomu alaykum! Men sizga CV tuzishda yordam beraman.\n\n👇 Pastdagi tugmani bosing:", reply_markup=keyboard)


# CV yaratish tugmasi
@dp.message_handler(lambda message: message.text == "📄 CV yaratish")
async def create_cv(message: types.Message):
    await CVForm.name.set()
    await message.answer("Ismingizni kiriting:")


@dp.message_handler(state=CVForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await CVForm.next()
    await message.answer("Yoshingizni kiriting:")


@dp.message_handler(state=CVForm.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await CVForm.next()
    await message.answer("Qanday ish yoki sohalarda ko‘nikmalaringiz bor?")


@dp.message_handler(state=CVForm.skills)
async def process_skills(message: types.Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await CVForm.next()
    await message.answer("O‘sha ish bo‘yicha tajribangizni yozing:")


@dp.message_handler(state=CVForm.experience)
async def process_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await CVForm.next()
    await message.answer("Yashash joyingizni kiriting:")


@dp.message_handler(state=CVForm.location)
async def process_location(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await CVForm.next()
    await message.answer("Email manzilingizni kiriting:")


@dp.message_handler(state=CVForm.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await CVForm.next()
    await message.answer("Telefon raqamingizni kiriting:")


@dp.message_handler(state=CVForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)

    data = await state.get_data()
    cv_text = (
        f"👤 Ism: {data['name']}\n"
        f"🎂 Yosh: {data['age']}\n"
        f"💡 Ko‘nikmalar: {data['skills']}\n"
        f"💼 Tajriba: {data['experience']}\n"
        f"🏠 Yashash joyi: {data['location']}\n"
        f"📧 Email: {data['email']}\n"
        f"📞 Telefon: {data['phone']}"
    )

    # Avval sarlavha yuboramiz
    await message.answer("📄 Sizning CV'ingiz tayyor!\n\nQuyidagi matnni nusxalab ishlatishingiz mumkin 👇")

    # Keyin CV matnini alohida yuboramiz
    await message.answer(cv_text)

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
