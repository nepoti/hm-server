<a href="#post-post">/post/ (POST)</a><br/>
<a href="#post-post-with-id">/post/ (POST with id)</a><br/>
<a href="#post-delete">/post/ (DELETE)</a><br/>
<a href="#postread">/post/read</a><br/>
<a href="#postcomment-post">/post/comment (POST)</a><br/>
<a href="#postcomment-post-with-id">/post/comment (POST with id)</a><br/>
<a href="#postcomment-delete">/post/comment (DELETE)</a><br/>
<a href="#postcommentread">/post/comment/read</a><br/>
<a href="#postlike">/post/like</a><br/>
<a href="#postlikes">/post/likes</a><br/>
<a href="#postcomments">/post/comments</a><br/>

### /post/ (POST)
**Type:** POST<br/>
**Params:** data (json)<br/>
**Response:** json<br/>
Создает пост на стене текущего пользователя<br/>
Можно указать до 1000 символов текста, до 10 фотографий, до 10 меток местоположения<br/>
data={"text":string, "photos":array of string, "locations":array of (float,float)}<br/>
В случае успеха в result возвращает id поста и дату/время создания поста.<br/>
Возможные ошибки, кроме стандартных: task_error, invalid_data<br/>

### /post/ (POST with id)
**Type:** POST<br/>
**Params:** id, data (json)<br/>
**Response:** json<br/>
Редактирует пост на стене текущего пользователя<br/>
Аналогично /post/create, но также нужно указать id изменяемого поста<br/>
Возможные ошибки, кроме стандартных: task_error, invalid_data, access_error<br/>

### /post/ (DELETE)
**Type:** DELETE<br/>
**Params:** id<br/>
**Response:** json<br/>
Удаляет пост на стене текущего пользователя<br/>
Нужно указать id удаляемого поста<br/>
Возможные ошибки, кроме стандартных: invalid_data, access_error<br/>

### /post/read
**Type:** POST<br/>
**Params:** id<br/>
**Response:** json<br/>
Получает информацию о посте с заданным id<br/>
Если пост не существует, то invalid_data<br/>
Пример ответа:<br/>
{"status": 1, "result": [{"author": 7, "timestamp": "2015-07-14T10:26:48.112Z", "locations": [\[53.5, 42.234325]], "photos": ["http://google.com/favicon.ico"], "text": "", "likes": 0, "id": 5}], "error": 0}<br/>

### /post/comment (POST)
**Type:** POST<br/>
**Params:** post_id, data (json)<br/>
**Response:** json<br/>
создает комментарий к заданному посту<br/>
аналогично /post/ (POST)<br/>

### /post/comment (POST with id)
**Type:** POST<br/>
**Params:** id, data (json)<br/>
**Response:** json<br/>
id комментария и данные<br/>
позволяет редактировать существующий комментарий<br/>
аналогично /post/ (POST with id)<br/>

### /post/comment (DELETE)
**Type:** POST<br/>
**Params:** id<br/>
позволяет удалить существующий комментарийч<br/>
удалить комментарий может только автор поста и автор комментария<br/>
аналогично /post/ (DELETE)<br/>

### /post/comment/read
**Type:** POST<br/>
**Params:** id<br/>
**Response:** json<br/>
Получает информацию о комментарии с заданным id<br/>
Если комментарий не существует, то invalid_data<br/>
Пример ответа:<br/>
{"status": 1, "result": [{"author": 8, "timestamp": "2015-07-14T17:32:46.311Z", "locations": [], "photos": [], "text": "Hello, comment!", "post": 5, "likes": 0, "id": 2}], "error": 0}<br/>

### /post/like
**Type:** POST, DELETE<br/>
**Params:** id<br/>
**Response:** json<br/>
Позволяет добавить/удалить like к заданному посту<br/>
В ответ возвращает новое количество likes<br/>

### /post/likes
**Type:** POST<br/>
**Params:** id [,offset, limit]<br/>
**Response:** json<br/>
Получить список тех, кто поставил like заданному посту в порядке возрастания времени установки лайка<br/>
Выдача постраничная, аналогично /user/followers<br/>
Пример ответа:<br/>
{"status": 1, "result": [{"count": 3, "data": [{"username": "Torvalds", "profile_image": "", "id": 7, "name": "noob"}, {"username": "testerer", "profile_image": "", "id": 8, "name": "testerer"}], "limit": 2, "offset": 0}], "error": 0}<br/>

### /post/comments
**Type:** POST<br/>
**Params:** id [,offset, limit]<br/>
**Response:** json<br/>
Получить список комментариев к заданному посту в порядке возрастания timestamp коммента<br/>
Выдача постраничная, аналогично /post/likes<br/>
Пример ответа:<br/>
{"status": 1, "result": [{"count": 1, "data": [{"author_profile_image": "", "author_username": "testerer", "likes": 0, "text": "Hello, world!", "timestamp": "2015-07-14T21:52:08.392Z", "author_id": 8, "photos": [], "id": 3, "author_name": "testerer", "locations": []}], "limit": 10, "offset": 0}], "error": 0}<br/>