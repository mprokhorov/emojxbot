from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from modules.liquidated import resize_and_overlay
from states.liquidated_states import Liquidated

router = Router()


@router.message(Command('liquidated'))
async def cmd_split(message: Message, state: FSMContext):
    await message.reply(text='Send one file with extension .png.')
    await state.set_state(Liquidated.choosing_image)


@router.message(Liquidated.choosing_image, F.document)
async def get_document(message: Message, state: FSMContext, bot: Bot):
    document = message.document
    path = f'images/liquidated_{message.from_user.id}.png'
    await bot.download(document.file_id, path)
    await state.update_data(image_path=path)
    resize_and_overlay(
        'images/text.png',
        f'images/liquidated_{message.from_user.id}.png',
        f'images/result_liquidated_{message.from_user.id}.png'
    )
    await state.set_state(Liquidated.done)
    await bot.send_photo(
        chat_id=message.from_user.id, photo=FSInputFile(f'images/result_liquidated_{message.from_user.id}.png')
    )


@router.message(Liquidated.choosing_image, ~F.document)
async def multiple_documents_error(message: Message, state: FSMContext, bot: Bot):
    await message.answer(
        'Make sure you have sent one file with extension .png or .jpeg.'
    )
