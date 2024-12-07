import random

HOROSCOPE = {
    "Овен": ["Сегодня отличный день для новых начинаний!", "Будьте осторожны с деньгами.", "Уделите внимание близким."],
    "Телец": ["День принесет вам приятные сюрпризы.", "Избегайте конфликтов на работе.", "Отдохните и восстановите силы."],
    "Близнецы": ["Идеальное время для общения!", "Постарайтесь завершить старые дела.", "Вечер будет полон вдохновения."],
    "Рак": ["Займитесь домашними делами.", "Возможно, вы получите хорошие новости.", "Будьте внимательны к своему здоровью."],
    "Лев": ["Сегодня вас ждут успехи в карьере!", "Не бойтесь рисковать.", "Заручитесь поддержкой друзей."],
    "Дева": ["Время для саморазвития.", "Сосредоточьтесь на работе.", "Избегайте ненужных трат."],
    "Весы": ["День гармонии и радости.", "Не торопитесь принимать важные решения.", "Уделите время себе."],
    "Скорпион": ["Ваши усилия будут вознаграждены.", "Не забывайте отдыхать.", "Будьте осторожны в общении."],
    "Стрелец": ["День подходит для путешествий.", "Не бойтесь мечтать.", "Возможны новые знакомства."],
    "Козерог": ["Будьте упорны, и всё получится.", "Составьте план действий.", "Сосредоточьтесь на долгосрочных целях."],
    "Водолей": ["Сегодня вы почувствуете прилив энергии.", "Идеальное время для творчества.", "Не забывайте о близких."],
    "Рыбы": ["Доверяйте своей интуиции.", "Время для романтики.", "Будьте внимательны к мелочам."],
}

def get_horoscope(sign: str) -> str:
    """Возвращает случайный гороскоп для указанного знака зодиака."""
    if sign in HOROSCOPE:
        return random.choice(HOROSCOPE[sign])
    else:
        return "Не удалось найти гороскоп для указанного знака. Проверьте правильность ввода."