from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


def text_corrector(target, message_text, author):
    if target == 'мероприятие':
        text_to_send = f'{author} предложил следующую идею для мероприятия:\n' + message_text
    elif target == 'вопрос':
        text_to_send = f'{author} задаёт вопрос:\n' + message_text
    elif target == 'предложение':
        text_to_send = f'{author} предлагает следующее:\n' + message_text
    elif target == 'перенаправление':
        text_to_send = f'{author} перенаправил вам сообщение:\n' + message_text
    else:
        return ''
    return text_to_send


def main():
    TOKEN = '5797780733:AAFlU1EkmrPkVm2H8-zX9O8fRsC3YpSlaCU'

    NIKITA_ID = 1
    EGOR_ID = 1
    ANYA_ID = 1
    GROUP_ID = 1

    ID = {
        'никита': NIKITA_ID,
        'егор': EGOR_ID,
        'аня': ANYA_ID
    }

    bot = Bot(TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler()
    async def redirect(message: types.Message):
        message_split = message.text.split(';;')

        if len(message_split) != 2:
            await message.reply('[!] Убедитесь в правильности введенного запроса!')
            return

        target = message_split[0].lower()
        author = ' '.join([message.from_user.first_name, message.from_user.last_name])

        resend_to = 1

        if target == 'перенаправление':
            message_text = message.reply_to_message.text
            try:
                resend_to = ID[message.text.split(' ')[1].lower()]
            except:
                await message.reply('[!] Убедитесь в правильности введённого адресата')
                return

        else:
            message_text = message_split[1]

        target_id = {
            'мероприятие': NIKITA_ID,
            'вопрос': NIKITA_ID,
            'предложение': ANYA_ID,
            'перенаправление': resend_to,
            'рассылка': 1
        }

        final_text = text_corrector(target, message_text, author)

        if not final_text:
            await message.reply('[!] Убедитесь в правильности введенного запроса!')
            return

        await bot.send_message(target_id[target], final_text)

    executor.start_polling(dp, skip_updates=1)


if __name__ == '__main__':
    main()
