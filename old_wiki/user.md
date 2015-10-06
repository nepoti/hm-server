<a href="user-profile">/user/profile</a><br/>
<a href="#userremove">/user/remove</a>,<br/>
<a href="#userposts">/user/posts</a><br/>
<a href="#userfollow">/user/follow</a><br/>
<a href="#userfollowers">/user/followers</a><br/>
<a href="#userfollowing">/user/following</a><br/>
<a href="#userimgupload">/user/imgupload</a><br/>
<a href="#usersearch">/user/search</a><br/>


###/user/remove
**Type:** POST<br/>
**Params:** password<br/>
**Response:** json<br/>
Позволяет удалить аккаунт текущего пользователя<br/>
Для удаления требуется передать текущий пароль, а также куку авторизации<br/>
Это сделано для того, чтобы никто, случайно получивший доступ к устройству пользователя, не удалил аккаунт без его разрешения<br/>

###/user/posts
**Type:** POST<br/>
**Params:** id (optional), offset(optional), limit (optional)<br/>
**Response:** json<br/>
получает данные постов, авторами которых является пользователь с заданным id или текущий пользователь<br/>
выдача постраничная аналогично /user/followers<br/>
limit - максимальное количество постов на странице, 1<=limit<=10<br/>
Пример ответа:<br/>
{"status": 1, "result": [{"count": 3, "data": [{"photos": [], "text": "Hello2", "likes": 0, "author": 7, "timestamp": "2015-07-15T18:41:23.471Z", "id": 8, "comments": 0, "locations": []}, {"photos": [], "text": "Hello2", "likes": 0, "author": 7, "timestamp": "2015-07-15T18:41:10.035Z", "id": 7, "comments": 0, "locations": []}, {"photos": [], "text": "Hello, world!", "likes": 3, "author": 7, "timestamp": "2015-07-14T20:55:25.778Z", "id": 6, "comments": 1, "locations": []}], "limit": 10, "offset": 0}], "error": 0}<br/>

###/user/follow
**Type:** POST, DELETE<br/>
**Params:** id<br/>
**Response:** <br/>
в зависимости от типа запроса добавляет/удаляет подписки для текущего пользователя<br/>
попытки добавления существующей подписки или удаления несуществующей будут успешны<br/><br/>

###/user/followers
**Type:** POST, DELETE<br/>
**Params:** id (optional), offset (optional, default=0), limit (optional)<br/>
**Response:** json (if POST)<br/>
при **POST** запросе возвращает **постранично** список подписчиков текущего пользователя или пользователя с заданным id<br/>
result в случае успеха имеет вид - **{"limit":int, "count":int, "offset":int, "data":array}**<br/>
limit - количество элементов на странице<br/>
data - массив id, name, username, profile_image подписчиков<br/>
data=[{"name":string, "profile_image":string, "username":string, "id":int},...]<br/>
при **DELETE** запросе позволяет удалить заданный id из подписчиков<br/>

###/user/following
**Type:** POST<br/>
**Params:** id (optional), offset (optional, default=0), limit (optional)<br/>
**Response:** json<br/>
возвращает **постранично** список подписок текущего пользователя или пользователя с заданным id<br/>
result в случае успеха имеет вид - **{"limit":int, "count":int, "offset":int, "data":array}**<br/>
limit - количество элементов на странице<br/>
data - массив id, name, username, profile_image подписчиков<br/>
data=[{"name":string, "profile_image":string, "username":string, "id":int},...]<br/>

###/user/imgupload
**Type:** POST<br/>
**Params:** length<br/>
**Response:** json<br/>
обязательный параметр length обозначает длину файла и она используется для генерации урла<br/>
если length>max_size, то в ответ придет invalid_data<br/>
max_size=5 MB состоянием на 24.07<br/>
возвращает единственную строку в массиве result в случае успеха<br/>
если сгенерировать урл не удалось или если 10 попыток генерации имени изображения провалились, то возвращает task_error<br/>
при этом по полученному url можно загрузить только jpg<br/>
при загрузке обязательно передать заголовки:
* Content-Type: image/jpg
* Content-Length: length (такая же длина как и передается серверу)<br/>

загрузка происходит по полученному url PUT запросом, где данными является картинка<br/>

###/user/search 
(не реализован)<br/>
**Type:** POST<br/>
**Params:** q, offset=0, limit=10<br/>
**Response:** json<br/>
обязательный параметр q (query)<br/>
возврат постраничный, в порядке убывания релевантности<br/>
при этом нельзя получить записи с offset>=100 or limit>10<br/>