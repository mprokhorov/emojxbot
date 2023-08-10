from aiogram import Router, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.test_states import Test

router = Router()


@router.message(Command('test'))
async def cmd_test(message: Message, state: FSMContext):
    await state.set_state(Test.testing)


@router.message(Test.testing)
async def print_test(message: Message, bot: Bot):
    attrs = vars(message)
    await message.answer('\n'.join('%s: %s' % item for item in attrs.items()))
