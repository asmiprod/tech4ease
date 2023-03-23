# Для начала импортируем необходимые модули:
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Здесь мы импортируем модули logging для логирования событий, Updater для работы с API Telegram, CommandHandler для обработки команд пользователя, MessageHandler для обработки сообщений пользователя и Filters для фильтрации сообщений.

# Далее, создадим функцию для обработки команды /start
def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот для обучения.")

# Теперь нужно создать объект Updater и передать ему токен доступа:
updater = Updater(token='YOUR_TOKEN', use_context=True)


#Далее, создадим диспетчер и зарегистрируем обработчик команды /start:

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))

# Теперь можно запустить бота:
updater.start_polling()

#После запуска бот будет ожидать сообщений от пользователей.
#Например, для обработки текстовых сообщений можно создать функцию message_handler и зарегистрировать её как обработчик сообщений	
#scss

def message_handler(update, context):
	text = update.message.text
	response = "Вы написали: " + text
	context.bot.send_message(chat_id=update.effective_chat.id, text=response)
	
dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

# Затем мы можем настроить соединение с базой данных:
# Подключение к базе данных
conn = sqlite3.connect('database.db')
cur = conn.cursor()


# Мы можем использовать этот объект соединения и курсора для выполнения запросов к базе данных.
# Далее мы можем создать объект Updater для нашего бота и настроить обработчики команд и сообщений:
	# python


# Создание объекта Updater и передача токена бота
updater = Updater(token='TOKEN', use_context=True)

# Получение диспетчера обработчиков команд и сообщений
dispatcher = updater.dispatcher

# Обработчик команды /start
def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот для обучения.")
	
# Обработчик текстовых сообщений
def echo(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
	
# Добавление обработчиков команд и сообщений
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

#В этом примере мы создали два обработчика: один для команды /start и один для текстовых сообщений. Обработчик команды /start просто отправляет приветственное сообщение, а обработчик текстовых сообщений просто повторяет текст сообщения.

# Наконец, мы можем запустить нашего бота:


# Далее мы можем продолжить с написания функций для обработки команд пользователей и реализации функционала нашего бота. Например, мы можем написать функцию для добавления нового пользователя в базу данных:
def add_user(update, context):
	# Получение аргументов команды
	args = context.args
	
	# Проверка наличия аргументов
	if not args:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Введите имя пользователя.")
		return
	
	# Извлечение аргументов
	name = ' '.join(args)
	telegram_id = update.message.from_user.id
	
	# Добавление пользователя в базу данных
	cur.execute("INSERT INTO users (telegram_id, name) VALUES (?, ?)", (telegram_id, name))
	conn.commit()
	
	context.bot.send_message(chat_id=update.effective_chat.id, text=f"Пользователь {name} добавлен в базу данных.")
	
	# Эта функция принимает аргументы команды (в нашем случае - имя пользователя) и добавляет нового пользователя в таблицу users базы данных.
	
	# Для того чтобы наш бот мог обрабатывать эту команду, мы можем добавить соответствующий обработчик в наш диспетчер:
	
	add_user_handler = CommandHandler('adduser', add_user)
	dispatcher.add_handler(add_user_handler)
	
	#Таким же образом мы можем написать функции для обработки других команд, например, команды для просмотра списка курсов и покупки курса:
	
def list_courses(update, context):
	# Получение списка курсов из базы данных
	cur.execute("SELECT id, name, description, price FROM courses")
	courses = cur.fetchall()
	
	# Отправка списка курсов пользователю
	for course in courses:
		course_info = f"{course[1]} ({course[3]} руб.)\n{course[2]}"
		context.bot.send_message(chat_id=update.effective_chat.id, text=course_info)
		
def buy_course(update, context):
	# Получение аргументов команды
	args = context.args
	
	# Проверка наличия аргументов
	if not args:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Введите идентификатор курса.")
		return
	
	# Извлечение аргументов
	course_id = int(args[0])
	user_id = update.message.from_user.id
	
	# Получение информации о курсе из базы данных
	cur.execute("SELECT name, price FROM courses WHERE id=?", (course_id,))
	course_info = cur.fetchone()
	
	# Проверка наличия курса с заданным идентификатором
	if not course_info:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Курс не найден.")
		return
	
	# Проверка наличия пользователя в базе данных
	cur.execute("SELECT id FROM users WHERE telegram_id=?", (user_id,))
	user_id = cur.fetchone()
	
	if not user_id:
		context.bot.send_message(chat_id=update.effective_chat.id, text="Пользователь не найден.")
	else:
		# Создание таблицы purchases, если она не существует
		cur.execute("""CREATE TABLE IF NOT EXISTS purchases (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			course_id INTEGER NOT NULL,
			user_id INTEGER NOT NULL,
			amount INTEGER NOT NULL,
			token TEXT NOT NULL,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
		)""")
		conn.commit()
import stripe
			
# Установка ключа API Stripe
stripe.api_key = "YOUR_API_KEY"
			
# Создание формы оплаты и получение токена
def create_payment_form(course_id, user_id):
	# Получение информации о курсе из базы данных
	# ...
			
	# Создание формы оплаты
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'name': course.name,
			'description': course.description,
			'amount': course.price * 100,
			'currency': 'usd',
			'quantity': 1,
		}],
		mode='payment',
		success_url='https://example.com/success',
		cancel_url='https://example.com/cancel',
	)
			
	# Сохранение информации о платеже в базе данных
	cur.execute(
		"INSERT INTO purchases (course_id, user_id, amount, token) VALUES (?, ?, ?, ?)",
		(course_id, user_id, course.price, session.id)
	)
	conn.commit()
			
	# Возвращение токена для отправки формы оплаты пользователю
	return session.id
			
@app.route('/webhook/stripe', methods=['POST'])
def handle_stripe_webhook():
	# Получение данных из запроса
	payload = request.get_data()
	sig_header = request.headers.get('Stripe-Signature')
	event = None
	
	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, stripe_webhook_secret
		)
	except ValueError as e:
		# Ошибка в теле запроса
		return 'Invalid payload', 400
	except stripe.error.SignatureVerificationError as e:
		# Неверный Stripe-Signature заголовок
		return 'Invalid signature', 400
	
	if event['type'] == 'checkout.session.completed':
		# Обработка уведомления о завершении платежа
		session = event['data']['object']
		customer_id = session['customer']
		amount = session['amount_total'] / 100
		
		# Обновление статуса оплаты в базе данных
		cur.execute(
			"UPDATE payments SET status='completed' WHERE stripe_session_id=?", (session['id'],)
		)
		conn.commit()
		
	
		
	# Отправка сообщения пользователю о завершении оплаты
	context.bot.send_message(chat_id=customer_id, text=f"Платеж на сумму {amount} руб. успешно завершен.")
			
return 'OK', 200

stripe_webhook_secret = 'WEBHOOK_SECRET'

# Регистрация webhook
endpoint_secret = stripe.WebhookEndpoint.create(
url='https://example.com/webhook/stripe',
enabled_events=['checkout.session.completed']
).secret
			
# Установка webhook
stripe.WebhookEndpoint.modify(
endpoint_secret,
enabled_events=['checkout.session.completed']
)
#В этом примере мы зарегистрировали webhook и установили его для события checkout.session.completed. Мы также получили секретный ключ для нашего webhook, который мы будем использовать для проверки подписи уведомлений от Stripe.
	
#Добавление пользователя в базу данных
def add_user(telegram_id, name, email, phone):
	cur.execute("INSERT INTO users (telegram_id, name, email, phone) VALUES (?, ?, ?, ?)", (telegram_id, name, email, phone))
	conn.commit()
	

		
		
			
	#Добавление курса в базу данных
def add_course(name, description, level, price, image):
	cur.execute("INSERT INTO courses (name, description, level, price, image) VALUES (?, ?, ?, ?, ?)", (name, description, level, price, image))
	conn.commit()
			
	#Получение списка курсов
def get_courses():
	cur.execute("SELECT * FROM courses")
	return cur.fetchall()
			
	#Получение списка пользователей
def get_users():
	cur.execute("SELECT * FROM users")
	return cur.fetchall()
	#В этих функциях мы используем методы execute и fetchall объекта курсора для выполнения запросов к базе данных.
			
	#Мы также можем написать обработчики команд для добавления пользователей и курсов, а также для просмотра списка курсов и пользователей:
			

			
	# Обработчик команды /adduser
	def add_user_handler(update, context):
		# Получение аргументов команды
		args = context.args
		telegram_id = args[0]
		name = args[1]
		email = args[2]
		phone = args[3]
		
		# Добавление пользователя в базу данных
		add_user(telegram_id, name, email, phone)
		
		context.bot.send_message(chat_id=update.effective_chat.id, text="Пользователь добавлен в базу данных.")
		
	# Обработчик команды /addcourse
	def add_course_handler(update, context):
		# Получение аргументов команды
		args = context.args
		name = args[0]
		description = args[1]
		level = args[2]
		price = args[3]
		image = args[4]
		
		# Добавление курса в базу данных
		add_course(name, description, level, price, image)
		
		context.bot.send_message(chat_id=update.effective_chat.id, text="Курс добавлен в базу данных.")
		
	# Обработчик команды /courses
	def courses_handler(update, context):
		# Получение списка курсов
		courses = get_courses()
		
		# Формирование списка курсов в виде текстового сообщения
		message = "Список курсов:\n"
		for course in courses:
			message += f"{course[0]}. {course[1]} ({course[2]}) - {course[4]} руб.\n"
			
		context.bot.send_message(chat_id=update.effective_chat.id, text=message)
		
	# Обработчик команды /users
	def users_handler(update, context):
		# Получение списка пользователей
		users = get_users()
		
		# Формирование списка пользователей в виде текстового сообщения
		message = "Список пользователей:\n"
		for user in users:
			message += f"{user[0]}. {user[2]} ({user[3]})\n"
			
		context.bot.send_message(chat_id=update.effective_chat.id, text=message)
		

			#Обработчик команды /users
		def users_handler(update, context):
			# Получение списка пользователей
			users = get_users()
			
# Формирование списка пользователей в виде текстового сообщения
message = "Список пользователей:\n"
for user in users:
	message += f"{user[0]}. {user[2]} ({user[3]})\n"
			
context

# Обработчик команды /courses
def courses(update, context):
# Получение списка курсов из базы данных
	cur.execute("SELECT * FROM courses")
	rows = cur.fetchall()

# Формирование списка курсов в виде кнопок
buttons = []
for row in rows:
	buttons.append([InlineKeyboardButton(text=row[1], callback_data=f"buy_course_{row[0]}")])
			
# Отправка сообщения с кнопками курсов
reply_markup = InlineKeyboardMarkup(buttons)
update.message.reply_text("Доступные курсы:", reply_markup=reply_markup)
			
			
			# Добавление обработчика команды /courses
courses_handler = CommandHandler('courses', courses)
dispatcher.add_handler(courses_handler)
			
			# В этом примере мы получаем список курсов из базы данных и формируем список кнопок в виде InlineKeyboardButton. При нажатии на кнопку курса, мы будем использовать callback_query_handler для обработки выбора курса пользователем и предложения ему купить этот курс.
			# Для реализации оплаты курса мы можем добавить обработчик callback_query_handler, который будет обрабатывать выбор курса пользователем и предлагать ему оплатить этот курс. Например, так:
			
		# 	Обработчик callback-запросов для оплаты курса
def buy_course_callback(update, context):
			query = update.callback_query
			
			# Получение информации о курсе из базы данных
			cur.execute("SELECT * FROM courses WHERE id=?", (query.data.split("_")[2],))
			row = cur.fetchone()
			
			# Создание сессии оплаты и получение ссылки на оплату
			session = stripe.checkout.Session.create(
				payment_method_types=['card'],
				line_items=[{
					'price_data': {
						'currency': 'usd',
						'product_data': {
							'name': row[1],
						},
						'unit_amount': row[4],
					},
					'quantity': 1,
				}],
				mode='payment',
				success_url='https://example.com/success',
				cancel_url='https://example.com/cancel',
			)
			
			# Сохранение информации о платеже в базе данных
			cur.execute("INSERT INTO payments (user_id, course_id, session_id) VALUES (?, ?, ?)",
						(query.from_user.id, row[0], session.id))
			conn.commit()
			
			# Отправка ссылки на оплату
			query.message.reply_text(f"Оплатите курс '{row[1]}' по ссылке:\n{session.url}")
			
			# Добавление обработчика callback-запросов для оплаты курса
			dispatcher.add_handler(CallbackQueryHandler(buy_course_callback, pattern=r"buy_course_"))
			#В этом примере мы используем метод CallbackQueryHandler, чтобы добавить обработчик для callback-запросов, которые начинаются со строки "buy_course_". Когда пользователь нажимает на кнопку "Купить курс", Telegram отправляет callback-запрос с соответствующим идентификатором курса, который мы можем извлечь из запроса и передать в функцию buy_course_callback.
			
		#	Функция buy_course_callback создает сессию оплаты с помощью Stripe API, создает кнопку оплаты и отправляет ее пользователю.
			
			# Для обработки ответов от Stripe API мы также добавляем обработчик в наш объект updater:
			
			# Обработчик оповещений об оплате от Stripe
		def stripe_webhook(update, context):
			# Получение данных о событии
			event = json.loads(update.message.to_dict()['text'])
			# Обработка события
			if event['type'] == 'checkout.session.completed':
			session_id = event['data']['object']['id']
			# Получение данных о сессии оплаты из базы данных
			cur.execute("SELECT * FROM payments WHERE session_id=?", (session_id,))
			payment = cur.fetchone()
			if payment:
			# Обновление записи в базе данных о статусе оплаты
			cur.execute("UPDATE payments SET status=? WHERE id=?", ('paid', payment[0]))
			conn.commit()
			
			# Добавление обработчика оповещений об оплате
			updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'/stripe_webhook.*'), stripe_webhook))
			# Здесь мы создаем обработчик для команды /stripe_webhook, которая используется для тестирования обработки уведомлений о платежах от Stripe. Когда Stripe отправляет уведомление о платеже, мы обрабатываем его в функции stripe_webhook, извлекаем соответствующую запись о платеже из базы данных и обновляем ее статус оплаты.
			# Обработчик команды /courses
			def courses(update, context):
			# Получение списка доступных курсов
			courses = get_courses(context.user_data['user_id'])
			
			# Получение информации о курсе
			course = get_course(course_id)
			
			# Отправка сообщения с информацией о курсе
			update.callback_query.message.reply_text(course['description'])
			
			# Добавление обработчиков команды /courses и callback-запросов для выбора курса
			dispatcher.add_handler(CommandHandler('courses', courses))
			dispatcher.add_handler(CallbackQueryHandler(select_course_callback, pattern=r"course_"))
			# В этом примере мы создали обработчик команды /courses, который получает список доступных курсов и отправляет кнопки для каждого курса. При нажатии на кнопку, бот отправляет информацию о курсе.
			
			# Мы также создали обработчик callback-запросов для выбора курса, который извлекает идентификатор курса из запроса, получает информацию о курсе и отправляет его описание.
			
			# Для работы с уроками мы можем создать команду /lessons для просмотра доступных уроков в рамках выбранного курса. Когда пользователь выбирает курс, мы можем сохранить его идентификатор в пользовательских данных, чтобы затем использовать его при запросе уроков.
			
			# Для реализации этой функциональности мы можем использовать следующий код:
			
			# Добавление обработчика команды /lessons и callback-запросов для выбора урока
			
			dispatcher.add_handler(CommandHandler('lessons', lessons))
			dispatcher.add_handler(CallbackQueryHandler(select_lesson_callback, pattern=r"lesson_"))
			# Обработчик команды /lesson
			def lesson(update, context):
			user_id = update.effective_user.id
			course_id = context.user_data.get('course_id')
			lesson_id = context.user_data.get('lesson_id')
			
			if not course_id or not lesson_id:
				context.bot.send_message(chat_id=user_id, text='Пожалуйста, выберите курс и урок с помощью команд /courses и /lessons.')
				return
			
			# Получение информации о текущем уроке
			cur.execute("SELECT * FROM lessons WHERE id=?", (lesson_id,))
			lesson = cur.fetchone()
			
			if not lesson:
				context.bot.send_message(chat_id=user_id, text='Урок не найден.')
				return
			
			# Отправка информации о текущем уроке
			text = f'Урок: {lesson[2]}\n\n{lesson[3]}'
			
			if lesson[4]:
				text += f'\n\nСодержание: {lesson[4]}'
			
			if lesson[5]:
				text += f'\n\nВидеоурок: {lesson[5]}'
			
			context.bot.send_message(chat_id=user_id, text=text)
			
			# Обработчик сообщений для получения домашнего задания
			def homework(update, context):
			user_id = update.effective_user.id
			course_id = context.user_data.get('course_id')
			lesson_id = context.user_data.get('lesson_id')
			
			if not course_id or not lesson_id:
				context.bot.send_message(chat_id=user_id, text='Пожалуйста, выберите курс и урок с помощью команд /courses и /lessons.')
				return
			
			# Получение информации о домашнем задании
			cur.execute("SELECT * FROM homework WHERE lesson_id=?", (lesson_id,))
			homework = cur.fetchone()
			
			if not homework:
				context.bot.send_message(chat_id=user_id, text='Домашнее задание не найдено.')
				return
			
			# Сохранение домашнего задания в базе данных
			cur.execute("INSERT INTO homework_users (lesson_id, user_id, deadline) VALUES (?, ?, ?)", (lesson_id, user_id, homework[4]))
			conn.commit()
			
			context.bot.send

	cur.execute('''CREATE TABLE IF NOT EXISTS questions (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id INTEGER,
			course_id INTEGER,
			question TEXT,
			expert_id INTEGER,
			expert_reply TEXT,
			asked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			replied_at TIMESTAMP)''')
			
			# Обработчик команды для отправки вопроса эксперту
			def ask_expert(update, context):
				# Получаем идентификатор пользователя и курса из пользовательских данных
				user_id = update.effective_user.id
				course_id = context.user_data.get('selected_course_id')
			
				# Получаем текст вопроса от пользователя
				question_text = update.message.text
			
				# Добавляем вопрос в базу данных
				cur.execute('''INSERT INTO questions (user_id, course_id, question)
								VALUES (?, ?, ?)''', (user_id, course_id, question_text))
				conn.commit()
			
				# Отправляем уведомление эксперту
				expert_id = 123456 # Заменить на реальный идентификатор эксперта
				context.bot.send_message(chat_id=expert_id, text=f"Новый вопрос:\n\n{question_text}")
			
				# Отправляем пользователю сообщение о том, что вопрос отправлен
				context.bot.send_message(chat_id=update.effective_chat.id, text="Ваш вопрос отправлен эксперту.")
			
			# Обработчик команды для просмотра ответа на вопрос
			def view_answer(update, context):
				# Получаем идентификатор пользователя и курса из пользовательских данных
				user_id = update.effective_user.id
				course_id = context.user_data.get('selected_course_id')
			
				# Ищем ответ на вопрос в базе данных
				cur.execute('''SELECT expert_reply
								FROM questions
								WHERE user_id = ? AND course_id = ? AND expert_reply IS NOT NULL
								ORDER BY replied_at DESC
								LIMIT 1''', (user_id, course_id))
				result = cur.fetchone()
			
				if result is not None:
					# Если ответ найден, отправляем его пользователю
					expert_reply = result[0]
					context.bot.send_message(chat_id=update.effective_chat.id, text=
						
					#Обработчик команды /support
						def support(update, context):
						context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Сообщение от пользователя {update.effective_user.username}: {update.message.text}")
						context.bot.send_message(chat_id=update.effective_chat.id, text="Ваше сообщение отправлено администраторам бота. Мы свяжемся с вами в ближайшее время.")
						
						# Добавление обработчика команды /support
						support_handler = CommandHandler('support', support)
						dispatcher.add_handler(support_handler)
						
						# Обработчик callback-запросов от эксперта
						
						def expert_answer_callback(update, context):
						# Извлекаем идентификатор вопроса из callback-запроса
						question_id = int(update.callback_query.data.replace('answer_', ''))
						
						# Получаем текст ответа от эксперта
						expert_reply = update.callback_query.message.text
						
						# Обновляем запись в базе данных с ответом эксперта
						cur.execute('''UPDATE questions
								SET expert_reply = ?, replied_at = ?
								WHERE id = ?''', (expert_reply, datetime.now(), question_id))
						conn.commit()
						
						# Отправляем пользователю сообщение с ответом
						question = get_question(question_id)
						context.bot.send_message(chat_id=question['user_id'], text=f"Ваш вопрос:\n\n{question['question']}\n\nОтвет эксперта:\n\n{expert_reply}")
						
						# Отправляем уведомление эксперту о том, что ответ отправлен
						context.bot.send_message(chat_id=update.effective_user.id, text="Ответ отправлен пользователю.")
						
					#	Добавляем обработчик callback-запросов эксперта
						dispatcher.add_handler(CallbackQueryHandler(expert_answer_callback, pattern=r"answer_.*"))
						# В этом примере мы извлекаем идентификатор вопроса из callback-запроса и сохраняем текст ответа эксперта в базе данных. Затем мы отправляем уведомление пользователю о том, что его вопрос был отвечен, и уведомление эксперту о том, что ответ отправлен.
						
					# 	Обработчик команды для просмотра списка заданных вопросов
						def view_questions(update, context):
						# Получаем идентификатор пользователя и курса из пользовательских данных
						user_id = update.effective_user.id
						course_id = context.user_data.get('selected_course_id')
						
						# Ищем все вопросы пользователя по выбранному курсу
						cur.execute('''SELECT id, question, expert_reply, replied_at
										FROM questions
										WHERE user_id = ? AND course_id = ?
										ORDER BY asked_at DESC''', (user_id, course_id))
						results = cur.fetchall()
						
						if len(results) == 0:
							# Если вопросов нет, отправляем сообщение об этом
							context.bot.send_message(chat_id=update.effective_chat.id, text="У вас пока нет заданных вопросов.")
						else:
							# Если вопросы найдены, отправляем список вопросов
							message = "Список заданных вопросов:\n\n"
							for result in results:
								question_id = result[0]
								question_text = result[1]
								expert_reply = result[2]
								replied_at = result[3]
						
								status = "Ответ не получен"
								if expert_reply is not None:
									status = "Ответ получен"
						
								message += f"#{question_id}: {question_text}\nСтатус: {status}\n\n"
						
							context.bot.send_message(chat_id=update.effective_chat.id, text=message)
							
						# Обработчик callback-запросов для ответа на вопрос эксперту
						def answer_question_callback(update, context):
						# Получаем идентификатор вопроса и ответа из запроса
						query = update.callback_query
						question_id = int(query.data.split("_")[1])
						answer_text = query.message.reply_to_message.text
						
						# Ищем вопрос в базе данных
						cur.execute('''SELECT user_id
										FROM questions
										WHERE id = ?''', (question_id,))
						result = cur.fetchone()
						
						if result is not None:
							# Если вопрос найден, отправляем ответ пользователю
							user_id = result[0]
							context.bot.send_message(chat_id=user_id, text=f"Ответ эксперта:\n\n{answer_text}")
						
							# Сохраняем ответ в базе данных
							cur.execute('''UPDATE questions
											SET expert_reply = ?, replied_at = ?
											WHERE id = ?''', (answer_text, datetime.now(), question_id))
							conn.commit()
						
							# Отправляем эксперту уведомление о том, что ответ отправлен
							expert_id = query.from_user.id
							context.bot.send_message(chat_id=expert_id, text=f"Ответ на вопрос отправлен пользователю.")
						
							# Обновляем сообщение с кнопкой ответа на вопрос
							query.edit_message
							
						cur.execute('''CREATE TABLE IF NOT EXISTS reviews (
								id INTEGER PRIMARY KEY AUTOINCREMENT,
								user_id INTEGER,
								course_id INTEGER,
								rating INTEGER,
								review TEXT,
								created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
						# Обработчик команды для отправки отзыва на курс
						def leave_review(update, context):
							# Получаем идентификатор пользователя и курса из пользовательских данных
							user_id = update.effective_user.id
							course_id = context.user_data.get('selected_course_id')
						
							# Получаем оценку и текст отзыва от пользователя
							rating = int(context.args[0])
							review_text = ' '.join(context.args[1:])
						
							# Добавляем отзыв в базу данных
							cur.execute('''INSERT INTO reviews (user_id, course_id, rating, review)
											VALUES (?, ?, ?, ?)''', (user_id, course_id, rating, review_text))
							conn.commit()
						
							# Отправляем пользователю сообщение о том, что отзыв отправлен
							context.bot.send_message(chat_id=update.effective_chat.id, text="Ваш отзыв отправлен.")
						
						# Обработчик команды для просмотра отзывов на курс
						def view_reviews(update, context):
							# Получаем идентификатор курса из пользовательских данных
							course_id = context.user_data.get('selected_course_id')
						
							# Ищем отзывы на курс в базе данных
							cur.execute('''SELECT rating, review
											FROM reviews
											WHERE course_id = ?
											ORDER BY created_at DESC''', (course_id,))
							results = cur.fetchall()
						
							if len(results) > 0:
								# Если есть отзывы, отправляем их пользователю
								message = 'Отзывы на курс:\n\n'
								for rating, review_text in results:
									message += f'Оценка: {rating}\n{review_text}\n\n'
								context.bot.send_message(chat_id=update.effective_chat.id, text=message)
							else:
								# Если отзывов нет, отправляем сообщение об этом
								context.bot.send_message(chat_id=update.effective_chat.id, text="Нет отзывов на этот курс.")
								
						#Обработчик команды /search
						def search(update, context):
						# Получаем список уроков для выбранного курса
						course_id = context.user_data.get('selected_course_id')
						cur.execute('''SELECT id, title, description
FROM lessons
WHERE course_id = ?''', (course_id,))
						lessons = cur.fetchall()
						
						# Получаем ключевые слова от пользователя
						keywords = update.message.text.split()[1:]
						
						# Список уроков, содержащих совпадения с ключевыми словами
						matched_lessons = []
						
						for lesson in lessons:
							# Обрабатываем каждый урок и ищем совпадения с ключевыми словами
							lesson_id, title, description = lesson
							match = False
						
							for keyword in keywords:
								if keyword.lower() in title.lower() or keyword.lower() in description.lower():
									match = True
									break
						
							if match:
								matched_lessons.append((lesson_id, title, description))
						
						# Отправляем пользователю список уроков, содержащих совпадения с ключевыми словами
						if len(matched_lessons) > 0:
							message = "Уроки, содержащие ключевые слова:\n\n"
						
							for lesson in matched_lessons:
								message += f"{lesson[1]}\n{lesson[2]}\n\n"
						
							context.bot.send_message(chat_id=update.effective_chat.id, text=message)
						else:
							context.bot.send_message(chat_id=update.effective_chat.id, text="Уроки, содержащие ключевые слова, не найдены.")
						# Создание таблицы пользователей
						cur.execute('''CREATE TABLE IF NOT EXISTS users (
						id INTEGER PRIMARY KEY,
						username TEXT,
						first_name TEXT,
						last_name TEXT,
						is_admin INTEGER)''')
						conn.commit()
						
						# В этой таблице мы будем хранить информацию о каждом пользователе, включая идентификатор, имя пользователя, имя, фамилию и признак того, является ли пользователь администратором.
						
					#	Далее мы можем создать обработчик команды /users, который будет извлекать данные пользователей из базы данных и отправлять их администратору. Вот примерный код для обработчика:
						
					#	Обработчик команды /users
						def list_users(update, context):
						# Получаем список пользователей из базы данных
						cur.execute('SELECT * FROM users')
						results = cur.fetchall()
						# Создаем сообщение с данными пользователей
						message = "Список пользователей:\n\n"
						for result in results:
							message += f"ID: {result[0]}\nUsername: {result[1]}\nFirst name: {result[2]}\nLast name: {result[3]}\nAdmin: {'Да' if result[4] else 'Нет'}\n\n"
						
						# Отправляем сообщение администратору
						context.bot.send_message(chat_id=update.effective_chat.id, text=message)
						
						# Обработчик команды /make_admin
						def make_admin(update, context):
						# Получаем идентификатор пользователя, которому нужно сделать администратором
						user_id = int(context.args[0])
						
						# Обновляем запись в таблице пользователей
						cur.execute('UPDATE users SET is_admin = 1 WHERE id = ?', (user_id,))
						conn.commit()
						
						# Отправляем сообщение об успешном изменении статуса
						context.bot.send_message(chat_id=update.effective_chat.id, text=f"Пользователь
							
		# оценки курсов				
cur.execute('''CREATE TABLE IF NOT EXISTS course_ratings (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		user_id INTEGER,
		course_id INTEGER,
		rating INTEGER,
		comment TEXT,
		rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
							
						#	В этой таблице мы будем хранить информацию о каждой оценке курса, включая идентификатор пользователя, идентификатор курса, оценку (число от 1 до 5) и комментарий. Также мы будем сохранять дату оценки.
							
							cur.execute('''CREATE TABLE IF NOT EXISTS expert_ratings (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									user_id INTEGER,
									expert_id INTEGER,
									rating INTEGER,
									comment TEXT,
									rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
							
							#В этой таблице мы будем хранить информацию о каждой оценке эксперта, включая идентификатор пользователя, идентификатор эксперта, оценку (число от 1 до 5) и комментарий. Также мы будем сохранять дату оценки.
							
							#Для добавления обработчиков команд для оценки курса и эксперта, мы можем использовать следующий код:
							
							# Обработчик команды для оценки курса
							def rate_course(update, context):
								# Получаем идентификатор пользователя и курса из пользовательских данных
								user_id = update.effective_user.id
								course_id = context.user_data.get('selected_course_id')
							
								# Получаем оценку и комментарий от пользователя
								rating = int(context.args[0])
								comment = " ".join(context.args[1:])
							
								# Добавляем оценку курса в базу данных
								cur.execute('''INSERT INTO course_ratings (user_id, course_id, rating, comment)
												VALUES (?, ?, ?, ?)''', (user_id, course_id, rating, comment))
								conn.commit()
							
								# Отправляем пользователю сообщение о том, что оценка сохранена
								context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша оценка курса сохранена.")
							
							# Обработчик команды для оценки эксперта
							def rate_expert(update, context):
								# Получаем идентификатор пользователя и эксперта из пользовательских данных
								user_id = update.effective_user.id
								expert_id = context.user_data.get('selected_expert_id')
							
								# Получаем оценку и комментарий от пользователя
								rating = int(context.args[0])
								comment = " ".join(context.args[1:])
							
								# Добавляем оценку эксперта в базу данных
								cur.execute('''INSERT INTO expert_ratings (user_id, expert_id, rating, comment)
												VALUES (?, ?, ?, ?)''', (user_id, expert_id, rating, comment))
								conn.commit
							
							
							# Следующим шагом может быть добавление возможности просмотра списка заказов и их статусов для администратора. Для этого мы можем создать отдельную команду /orders и обработчик для нее:
							
							# Обработчик команды для просмотра списка заказов и их статусов
							def orders(update, context):
								# Получаем список заказов из базы данных
								cur.execute('''SELECT orders.*, courses.title, users.username
												FROM orders
												JOIN courses ON orders.course_id = courses.id
												JOIN users ON orders.user_id = users.id
												ORDER BY created_at DESC''')
								result = cur.fetchall()
							
								if result:
									# Если заказы найдены, отправляем их пользователю
									message = "Список заказов:\n\n"
									for row in result:
										message += f"Заказ #{row[0]}:\n"
										message += f"Курс: {row[8]}\n"
										message += f"Пользователь: @{row[9]}\n"
										message += f"Статус: {row[5]}\n"
										message += f"Дата создания: {row[3]}\n\n"
								else:
									# Если заказы не найдены, отправляем сообщение об этом
									message = "Заказы не найдены."
							
								context.bot.send_message(chat_id=update.effective_chat.id, text=message)
							
							#В этом примере мы получаем список заказов из базы данных и отправляем их пользователю в виде сообщения.
							
							#Также мы можем добавить возможность изменения статуса заказа администратором. Для этого мы можем использовать обработчик callback-запросов, который будет вызываться при нажатии на кнопку изменения статуса заказа:
							
							# Обработчик callback-запросов для изменения статуса заказа
							def change_order_status_callback(update, context):
								query = update.callback_query
								order_id = int(query.data.split('_')[2])
								new_status = query.data.split('_')[3]
							
								# Изменяем статус заказа в базе данных
								cur.execute('''UPDATE orders SET status = ? WHERE id = ?''', (new_status, order_id))
								conn.commit()
							
								# Отправляем сообщение пользователю о изменении статуса заказа
								message = f"Статус вашего заказа #{order_id} изменен на {new_status}."
								context.bot.send_message(chat_id=query.message.chat_id, text=message)
								
								# Обработчик команды для просмотра списка вопросов и ответов экспертов
								def questions(update, context):
								# Получаем все вопросы и ответы экспертов из базы данных
								cur.execute('''SELECT q.id, u.username, c.title, q.question, e.username, q.expert_reply
								FROM questions q
								JOIN users u ON u.id = q.user_id
								JOIN courses c ON c.id = q.course_id
								LEFT JOIN users e ON e.id = q.expert_id
								ORDER BY q.asked_at DESC''')
								results = cur.fetchall()
								
								# Отправляем список вопросов и ответов экспертов администратору
								if results:
									message = "Список вопросов и ответов экспертов:\n\n"
									for result in results:
										question_id, username, course_title, question_text, expert_username, expert_reply = result
										message += f"ID вопроса: {question_id}\nПользователь: {username}\nКурс: {course_title}\nВопрос: {question_text}\n"
										if expert_reply is not None:
											message += f"Ответ эксперта ({expert_username}): {expert_reply}\n"
										else:
											message += "Ответ эксперта: -\n"
										message += "\n"
									context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
								else:
									context.bot.send_message(chat_id=ADMIN_CHAT_ID, text="Список вопросов и ответов экспертов пуст.")
				import pandas as pd
				
			#	Обработчик команды для создания отчета о продажах за определенный период
				def sales_report(update, context):
				# Получаем даты начала и конца периода из сообщения
				start_date = pd.to_datetime(context.args[0])
				end_date = pd.to_datetime(context.args[1])
				
				# Запрашиваем данные из базы данных
				cur.execute('''SELECT DATE(created_at), SUM(amount)
						FROM orders
						WHERE created_at BETWEEN ? AND ?
						GROUP BY DATE(created_at)''', (start_date, end_date))
				results = cur.fetchall()
							
				# Создаем объект DataFrame из результатов запроса
				df = pd.DataFrame(results, columns=['date', 'amount'])
				df['date'] = pd.to_datetime(df['date'])
				df.set_index('date', inplace=True)
							
				# Создаем график и сохраняем его в файл
				ax = df.plot(kind='bar', figsize=(10, 6))
				ax.set_xlabel('Date')
				ax.set_ylabel('Sales Amount')
				ax.set_title('Sales Report')
							
				filename = f'sales_report_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.png'
				plt.savefig(filename)
							
				# Отправляем файл с отчетом пользователю
				context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(filename, 'rb'))
							
							#Мы создаем обработчик команды /sales_report, который принимает два аргумента - даты начала и конца периода. Затем мы запрашиваем данные о продажах из базы данных, создаем объект DataFrame из результатов запроса, создаем график и сохраняем его в файл. Наконец, мы отправляем файл с отчетом пользователю.
							
						#	Мы можем добавить и другие типы отчетов, например, отчеты о количестве заказов, отчеты о продажах по категориям товаров и т.д.
							
						#	Таким образом, мы можем создать полнофункциональный бот для онлайн-курсов с возможностью оплаты, задания вопросов экспертам, просмотра уроков и создания отчетов для администратора.
							
						
							# дальше мы можем добавить возможность редактирования информации о курсах и уроках администратором. Для этого мы можем создать команды для добавления, удаления и редактирования курсов и уроков.
							
							cur.execute('''CREATE TABLE IF NOT EXISTS courses (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									title TEXT,
									description TEXT,
									price INTEGER)''')
							
							cur.execute('''CREATE TABLE IF NOT EXISTS lessons (
									id INTEGER PRIMARY KEY AUTOINCREMENT,
									course_id INTEGER,
									title TEXT,
									description TEXT,
									video_url TEXT)''')
							#Для добавления, удаления и редактирования курсов мы можем создать следующие команды:
							
							# Обработчик команды для добавления курса
							def add_course(update, context):
								# Получаем информацию о курсе от пользователя
								title = context.args[0]
								description = context.args[1]
								price = int(context.args[2])
							
								# Добавляем курс в базу данных
								cur.execute('''INSERT INTO courses (title, description, price)
												VALUES (?, ?, ?)''', (title, description, price))
								conn.commit()
							
								# Отправляем пользователю сообщение о том, что курс добавлен
								context.bot.send_message(chat_id=update.effective_chat.id, text="Курс добавлен.")
							
							# Обработчик команды для удаления курса
							def delete_course(update, context):
								# Получаем идентификатор курса от пользователя
								course_id = int(context.args[0])
							
								# Удаляем курс из базы данных
								cur.execute('''DELETE FROM courses WHERE id = ?''', (course_id,))
								conn.commit()
							
								# Отправляем пользователю сообщение о том, что курс удален
								context.bot.send_message(chat_id=update.effective_chat.id, text="Курс удален.")
							
							# Обработчик команды для редактирования курса
							def edit_course(update, context):
								# Получаем информацию о курсе от пользователя
								course_id = int(context.args[0])
								title = context.args[1]
								description = context.args[2]
								price = int(context.args[3])
							
								# Обновляем информацию о курсе в базе данных
								cur.execute('''UPDATE courses SET title = ?, description = ?, price = ?
												WHERE id = ?''', (title, description, price, course_id))
								conn.commit()
							
								# Отправляем пользователю сообщение о том, что курс отредактирован
								context.bot.send_message(chat_id=update.effective_chat.id, text="Курс отредактирован.")
							# Обработчик команды для добавления урока
							def add_lesson(update, context):
							# Получаем информацию об уроке от пользователя
							course_id = int(context.args[0])
							title = context.args[1]
							description = context.args[2]
							video_url = context.args[3]
							
							# Добавляем урок в базу данных
							cur.execute('''INSERT INTO lessons (course_id, title, description, video_url)
									VALUES (?, ?, ?, ?)''', (course_id, title, description, video_url))
							conn.commit()
							
							# Отправляем пользователю сообщение о том, что урок добавлен
							context.bot.send_message(chat_id=update.effective_chat.id, text="Урок успешно добавлен.")
							
						#	Обработчик команды для удаления урока
							def delete_lesson(update, context):
							# Получаем информацию об уроке от пользователя
							lesson_id = int(context.args[0])
							
							# Удаляем урок из базы данных
							cur.execute('''DELETE FROM lessons WHERE id = ?''', (lesson_id,))
							conn.commit()
							
							# Отправляем пользователю сообщение о том, что урок удален
							context.bot.send_message(chat_id=update.effective_chat.id, text="Урок успешно удален.")
							
							# Обработчик команды для редактирования урока
							def edit_lesson(update, context):
							# Получаем информацию об уроке от пользователя
							lesson_id = int(context.args[0])
							title = context.args[1]
							description = context.args[2]
							video_url = context.args[3]
							
							# Обновляем информацию об уроке в базе данных
							cur.execute('''UPDATE lessons SET title = ?, description = ?, video_url = ?
									WHERE id = ?''', (title, description, video_url, lesson_id))
							conn.commit()
							
							# Отправляем пользователю сообщение о том, что урок изменен
							context.bot.send_message(chat_id=update.effective_chat.id, text="Урок успешно изменен.")
							
							#В этом примере мы создали три обработчика команд: для добавления, удаления и редактирования уроков. Каждый обработчик получает информацию об уроке от пользователя и обновляет соответствующую запись в базе данных. После этого бот отправляет сообщение пользователю о результате операции.
							
						#	Крc