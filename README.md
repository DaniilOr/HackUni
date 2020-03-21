# HackUni
POST запросы:
/login: получает password, email. Вернет {'Result': 'Failed, password missmatch'} с кодом 404, если не совпали почта и пароль, {'Result': 'Logged in'}), 200 если все ок
/change_priority: получает id пользователя. Вернет либо сообщение о том, что такого юзера нет, либо поменяет ему приоритет (с высокого на низкий и назад)
/register: получает username, password, role, distance, description, price, email. Вернет инфу об ошибке, если почта занята или ОК
Get запросы:
/get_all: просто вернет всех пользователей
/get_users: получает roles - массив с ролями, которые выбрал пользователь. Получает массив людей по этим ролям. Они уже отсортированы по рейтингу, расстоянию и приоритету
/get_specific_role - получает role, возвращает отсортированных людей по этой роли
