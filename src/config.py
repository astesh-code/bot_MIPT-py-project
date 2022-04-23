#web block
URL = 'https://russia-edu.minobrnauki.gov.ru'
HEADERS={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
        }

#pathes_block
log_path='botlog.log'
base_path='stage_base.csv'

#button_texts
btn_input='✏️ Ввести данные'
btn_check='❓ Проверить'
btn_edit='✏️ Изменить'
btn_reload='🔄  Сбросить'

#period of user ban in seconds
ban_per=3600

#bot dictionary
phrases={
        'hello1':'Этот бот поможет остлеживать статус анкеты на сайте russia-edu.minobrnauki.gov.ru',
        'hello2': 'Для начала нужно ввести данные анкеты. Нажми кнопку на клавиатуре ниже',
        'input_number': 'Пожалуйста, введи номер анкеты в формате ABC-12345/21',
        'press_btn': f'Нажми кнопку « {btn_input} » на клавиатуре ниже',
        'input_email': 'Теперь введи почту',
        'check_number':'Проверь формат номера анкеты. Пример: ABC-12345/21',
        'data_updated': f'Данные записаны. Нажми кнопку  « {btn_check} »  для получения статуса или  « {btn_edit} »  для отслеживания другой заявки. \nМожно удалить данные, нажав на кнопку  « {btn_reload} »',
        'email_to_start': 'Для начала введи почту',
        'check_email': 'Похоже, введена несуществующая почта. Попробуй ещё',
        'ban_time': 'Бот возобновит работу через ',
        'erasing': 'Данные удалены',
        'waiting': 'Секунду...',
        'success': f'Нажми кнопку  « {btn_check} »,  чтобы получить статус снова, или  « {btn_edit} »  для отслеживания другой заявки. \nМожно удалить данные, нажав на кнопку  « {btn_reload} »',
        'fail': 'Похоже, были введены неправильные данные или возникла проблема с соединением. Проверь правильность ввода или повтори позднее',
        'get_ban': 'На сайте существует антибот-проверка, срабатывающая при многократном неправильным вводе. Бот возобновит работу через час'
        }