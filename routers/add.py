import io
import os

from PIL import Image
from aiogram import Router, F, Bot, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputSticker, BufferedInputFile
from aiogram.types import ReplyKeyboardRemove

from keyboards.inline_keyboard import make_inline_keyboard
from states.add_states import Add

router = Router()


@router.message(Command('add'))
async def cmd_add(message: Message, state: FSMContext):
    await message.reply(text='Send one image which will be used to make an emoji.')
    await state.set_state(Add.choosing_image)


@router.message(Add.choosing_image, F.sticker)
async def add_sticker(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    sticker = message.sticker
    path = f'images/{message.from_user.id}.webp'
    await bot.download(sticker.file_id, path)
    await state.update_data(image_path=path)
    await state.set_state(Add.choosing_set)
    builder = make_inline_keyboard(data['is_empty'].keys())
    await message.answer('Select the emoji set to which the tiles will be added:', reply_markup=builder.as_markup())


@router.message(Add.choosing_image, F.document)
async def add_document(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    document = message.document
    path = f'images/{document.file_name}'
    await bot.download(document.file_id, path)
    await state.update_data(image_path=path)
    await state.set_state(Add.choosing_set)
    builder = make_inline_keyboard(data['is_empty'].keys())
    await message.answer('Select the emoji set to which the tiles will be added:', reply_markup=builder.as_markup())


@router.message(Add.choosing_image, F.photo)
async def add_photo(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    photo = message.photo[-1]
    path = f'images/{message.from_user.id}.png'
    await bot.download(photo.file_id, path)
    await state.update_data(image_path=path)
    await state.set_state(Add.choosing_set)
    builder = make_inline_keyboard(data['is_empty'].keys())
    await message.answer('Select the emoji set to which the tiles will be added:', reply_markup=builder.as_markup())


@router.message(Add.choosing_image)
async def multiple_images_error(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Make sure you have sent one image.')


@router.callback_query(Add.choosing_set)
async def finalize(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    set_name = callback.data
    is_empty = data['is_empty']
    set_names = is_empty.keys()
    if set_name not in set_names:
        await callback.answer(text='This emoji set doen\'t exist.', show_alert=True)
        return
    await callback.answer()
    if is_empty[set_name]:
        current_emoji_set = await bot.get_sticker_set(set_name)
        sticker_to_delete = current_emoji_set.stickers[0].file_id
        await bot.delete_sticker_from_set(sticker_to_delete)
        is_empty[set_name] = False
        await state.update_data(is_empty=is_empty)
    image_path = data['image_path']
    image_for_emoji = Image.open(image_path)
    w, h = image_for_emoji.size
    if w < h:
        img = Image.new('RGBA', (h, h), (255, 0, 0, 0))
        back_im = img.copy()
        back_im.paste(image_for_emoji, ((h - w) // 2, 0))
        resized_image = back_im
        resized_image = resized_image.resize((100, 100))
    elif w > h:
        img = Image.new('RGBA', (w, w), (255, 0, 0, 0))
        back_im = img.copy()
        back_im.paste(image_for_emoji, (0, (w - h) // 2))
        resized_image = back_im
        resized_image = resized_image.resize((100, 100))
    else:
        resized_image = image_for_emoji.resize((100, 100))
    buf = io.BytesIO()
    resized_image.save(buf, format='PNG')
    buf.seek(0)
    text_file = BufferedInputFile(buf.getvalue(), filename=f'pic1.png')
    current_emoji = InputSticker(sticker=text_file, emoji_list=['✂️'])
    await bot.add_sticker_to_set(callback.from_user.id, set_name, current_emoji)
    await callback.message.reply('Done.', reply_markup=ReplyKeyboardRemove())
    os.remove(image_path)
    await state.set_state(Add.done)
