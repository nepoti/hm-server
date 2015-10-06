### /user/profile
<a href="#userprofileread">/user/profile/read</a><br/>
<a href="#userprofileupdate">/user/profile/update</a><br/>

###/user/profile/read
**Type:** POST<br/>
**Params:** id (optional)<br/>
**Response:** json<br/>
Позволяет получить профиль текущего пользователя<br/>
Если указано id, то позволит получить профиль пользователя с указаным id, если он существует<br/>

###/user/profile/update
**Type:** POST<br/>
**Params:** data (json)<br/>
**Response:** json<br/>
параметры для обновления задаются в словаре, при этом должны соблюдатся следующие правила:<br/><br/>
для обновления **birthday** передается массив размером 3: [year, month, day]<br/>
для удаления **birthday** передается пустой массив: []<br/><br/>
для обновления любых **остальных** значений (**achievements обновлять запрещено**) используются строки, при этом существуют ограничения на длину строк:
* name - 30
* profile_image (URL) - 200
* gender - 20
* country - 50
* сity - 200
* about - 100

в ответе словарь с полученными параметрами, каждому из них будет соответствовать булевое значение - успешно или нет<br/>
даже если все операции выполнены успешно, а какая-то из операций не удалась, получите 0 в status<br/>
пример словаря для отправки:<br/>
{"birthday": [1999,1,1], "about": "html programmer"}