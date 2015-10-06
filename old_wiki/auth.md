<a href="#authregister">/auth/register</a>,<br/>
<a href="#authlogin">/auth/login</a>,<br/>
<a href="#authlogout">/auth/logout</a>,<br/>
<a href="#authreset">/auth/reset(веб)</a>,<br/>
<a href="#authedit">/auth/edit</a>,<br/>
<a href="#authrestore">/auth/restore</a>,<br/>

### /auth/register
**Type:** POST<br/>
**Params:** username, password, email<br/>
**Response:** json {"status": int_code, "error": int_code}<br/>
При успешной регистрации status=1 error=0<br/>
Иначе status=0 error=код_ошибки<br/>
<br/>

###/auth/login
**Type:** POST<br/>
**Params:** username, password или cookies<br/>
**Response:** json {"status": int_code, "result": dictionary, "error": int_code}<br/>
result содержит инфу о пользователе, на данный момент это email.<br/>
<br/>

Также при успешном входе по логину/паролю кроме json возвращает в заголовках токен/куку, которая собственно и есть идентификатором<br/>
Поэтому важно ее сохранить<br/>
Также возможен вход по cookies, для этого нужно:<br/>
отправить в запросе cookies<br/>
также должен присутствовать post-параметр cookies равный true<br/>
Ответы при входе по cookies точно также в json<br/>

###/auth/logout
**Type:** GET (возможно, работает на другие, но не стоит пробовать)<br/>
**Params:** <br/>
**Response:** json<br/>
Работает для всех, в т.ч. для тех, кто не залогинен<br/>
Нужно передать cookies как обычно и тогда будет нормальный выход из системы<br/>

###/auth/reset
Веб-морда сброса пароля, планируется подключение к api (впрочем, сброс все равно переходом по ссылке из письма, так что можно и сделать через веб)<br/>
Абсолютно рабочая, но могут быть задержки в отсылке письма<br/>
Плюс морда сугубо тестовая и поэтому интерфейс совершенно не продумывался (привет дизайнерам)<br/>

###/auth/edit
**Type:** POST<br/>
**Params:** password, optional: username, new_password, email<br/>
**Response:** json<br/>
Требует текущий пароль - password, иначе **auth_error**<br/>
<br/>
Позволяет сменить юзернейм/пароль/email текущего пользователя<br/>
Для каждого из 3 возможных ключей возвращает булевое значение результата<br/>
Если хотя бы 1 из операций не удалась, в ответе будет сообщение об ошибке task_error
Внимание: При этом в случае успешной смены пароля возвращает **новые cookies**, а старые становятся недействительными.<br/>
Также возможны ответы username_not_valid, email_not_valid, email_already_exist<br/>

###/auth/restore
**Type:** POST<br/>
**Params:** email<br/>
**Response:** json<br/>
Отправляет на email письмо с ссылкой для восстановления пароля<br/>
В случайно успешного постановления в очередь возвращает status_ok<br/>
Может вернуть email_not_valid<br/>
Однако не проверяет, есть ли user с такой почтой<br/>
Задание будет выполнено в отдельной очереди, поэтому успешный ответ не гарантирует, что письмо было отправлено<br/>