from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

event = 'мероприятие'
question = 'вопрос'
suggestion = 'предложение'
redirection = 'перенаправление'
forward = 'рассылка'

TOKEN = '...'

NIKITA_ID = 1
EGOR_ID = 1
ANYA_ID = 1
GROUP_ID = 1

ID = {
    'никита': NIKITA_ID,
    'егор': EGOR_ID,
    'аня': ANYA_ID
}


def text_corrector(target, message_text, author):
    if target == event:
        text_to_send = f'{author} предложил следующую идею для мероприятия:\n{message_text}'
    elif target == question:
        text_to_send = f'{author} задаёт вопрос:\n{message_text}'
    elif target == suggestion:
        text_to_send = f'{author} предлагает следующее:\n{message_text}'
    elif target == redirection:
        text_to_send = f'{author} перенаправил вам сообщение:\n{message_text}'
    elif target == forward:
        text_to_send = f'{author} поделился:\n{message_text}'
    else:
        return ''
    return text_to_send


def main():
    bot = Bot(TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['help', 'start'])
    async def command_help_start(message: types.Message):
        await message.reply('Привет! Вот, что я могу:\n'
                            '1) мероприятие;; "текст" - отправка вашего мероприятия на расмотрение\n'
                            '2) вопрос;; "текст" - отправка вашего вопроса, вы получите ответ, как только замученный учебой человек достанет телефон ;(\n'
                            '3) предложение;; "текст" - задайте интерессуюший вас вопрос касательно любых волнующих моментов, ответ вы получите, как было указано в пункте выше')

    @dp.message_handler()
    async def redirect(message: types.Message):
        message_split = message.text.split(';;')

        if len(message_split) != 2:
            await message.reply('[!] Убедитесь в правильности введенного запроса!')
            return

        target = message_split[0].lower()
        author = ' '.join([message.from_user.first_name, message.from_user.last_name])

        resend_to = 1

        if target == redirection:
            message_text = message.reply_to_message.text
            try:
                resend_to = ID[message.text.split(' ')[1].lower()]
            except:
                await message.reply('[!] Убедитесь в правильности введённого адресата')
                return
        elif target == forward:
            message_text = message.reply_to_message.text
        else:
            message_text = message_split[1]

        target_id = {
            event: NIKITA_ID,
            question: NIKITA_ID,
            suggestion: ANYA_ID,
            redirection: resend_to,
            forward: GROUP_ID
        }

        final_text = text_corrector(target, message_text, author)

        if not final_text:
            await message.reply('[!] Убедитесь в правильности введенного запроса!')
            return

        await bot.send_message(target_id[target], final_text)

    executor.start_polling(dp, skip_updates=1)


if __name__ == '__main__':
    main()
