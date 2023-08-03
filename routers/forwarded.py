from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendAnimation
from aiogram.types import Message, FSInputFile

from modules.forwarded_from import resize_forwarded_from
from states.forwarded_states import Forwarded

router = Router()


@router.message(Command('forwarded'))
async def cmd_split(message: Message, state: FSMContext):
    await message.reply(text='Send one file with extension .png.')
    await state.set_state(Forwarded.choosing_image)


@router.message(Forwarded.choosing_image, F.document)
async def get_document(message: Message, state: FSMContext, bot: Bot):
    document = message.document
    path = f'images/forwarded_from_{message.from_user.id}.png'
    await bot.download(document.file_id, path)
    await state.update_data(image_path=path)
    resize_forwarded_from(path, f'images/forwarded_from_{message.from_user.id}.gif')
    await state.set_state(Forwarded.done)
    await SendAnimation(chat_id=message.from_user.id,
                        animation=FSInputFile(f'images/forwarded_from_{message.from_user.id}.gif'))


@router.message(Forwarded.choosing_image, ~F.document)
async def get_document(message: Message, state: FSMContext, bot: Bot):
    await message.answer(
        'Make sure you have sent one file with extension .png or .jpeg.'
    )
