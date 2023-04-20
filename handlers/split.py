import math
import os

from PIL import Image
from aiogram import Router, F, Bot, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputSticker, BufferedInputFile
from aiogram.types import ReplyKeyboardRemove

from keyboards.inline_keyboard import make_inline_keyboard
from scripts.crop import split_static_image
from states.split_states import Split

router = Router()


@router.message(Command('split'))
async def cmd_split(message: Message, state: FSMContext):
    await message.reply(text='Send one file with extension .png or .jpeg. Note that'
                             'the number of tiles should not exceed 200.')
    await state.set_state(Split.choosing_image)


@router.message(Split.choosing_image, F.document)
async def get_document(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    document = message.document
    path = f'images/{message.from_user.id}:{document.file_name}'
    await bot.download(document.file_id, path)
    await state.update_data(image_path=path)
    await state.set_state(Split.choosing_set)
    builder = make_inline_keyboard(data['is_empty'].keys())
    await message.answer(
        "Select the emoji set to which the tiles will be added:",
        reply_markup=builder.as_markup()
    )


@router.message(Split.choosing_image, ~F.document)
async def get_document(message: Message, state: FSMContext, bot: Bot):
    await message.answer(
        "Make sure you have sent one file with extension .png or .jpeg."
    )


@router.callback_query(Split.choosing_set)
async def delete_set(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    set_name = callback.data
    is_empty = data['is_empty']
    set_names = is_empty.keys()
    if set_name not in set_names:
        await callback.answer(
            text="This emoji set doen't exist.",
            show_alert=True
        )
        return
    progress_message = await callback.message.answer("Splitting started...")
    if is_empty[set_name]:
        current_emoji_set = await bot.get_sticker_set(set_name)
        sticker_to_delete = current_emoji_set.stickers[0].file_id
        await bot.delete_sticker_from_set(sticker_to_delete)
        is_empty[set_name] = False
        await state.update_data(is_empty=is_empty)
    image_path = data['image_path']
    img_to_split = Image.open(image_path)
    tiles_to_add = split_static_image(img_to_split)
    last_progress = -5
    for i, buf in enumerate(tiles_to_add):
        current_progress = math.ceil(((i + 1) / len(tiles_to_add)) * 20) * 5
        if current_progress > last_progress:
            await progress_message.edit_text(text=f"Splitting: {current_progress}%")
            last_progress = current_progress
        text_file = BufferedInputFile(buf, filename=f"pic{i}.png")
        current_emoji = InputSticker(sticker=text_file, emoji_list=['✂️'])
        await bot.add_sticker_to_set(callback.from_user.id, set_name, current_emoji)
    await callback.message.reply("Done.", reply_markup=ReplyKeyboardRemove())
    os.remove(image_path)
    await state.set_state(Split.done)
