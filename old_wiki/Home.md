### Новости
появилось восстановление пароля по почте<br/>

### API
Тестовый сервер висит пока что на dev.it-open.com порт 8037<br/>
**Внимание!**<br/>
Любой метод api при неправильном типе запроса или отсутствии хотя бы 1 параметра ответит 404<br/><br/>

Общий вид ответа:
{status: int, result: [data (optional)], error: int}<br/><br/>

**<a href="Коды-ошибок">Коды ошибок</a>**<br/><br/>

**<a href="auth">/auth</a>**<br/>
**<a href="user">/user</a>**<br/>
**<a href="post">/post</a>**<br/><br/>

**Внимание!**<br/>
Теперь также нужно отсылать заголовки<br/>
X-Platform:web|ios|android|java|symbian|wp7|vk|fb|win|mobile|osx<br/>
X-Platform-Version: x.x<br/>
X-Client-Version: x.x<br/>

### Как поднять сервак
Заходим в tmux attach -t server<br/>
Если сессия есть, то ./manage.py runserver 0.0.0.0:8037<br/>
Если не открылась сессия, то надо tmux new -s server<br/>
Дальше cd /home/hm<br/>
export PYTHONPATH="$PYTHONPATH:/home/hm";<br/>
export DJANGO_SETTINGS_MODULE=hm.settings;<br/>
./manage.py runserver 0.0.0.0:8037<br/>
В случае неудачи где-либо гуглить, но код сервака не менять<br/>