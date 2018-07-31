- 理解werkzeug.security中generate_password_hash算法的原理


{
"email":"ssgx",
"password":"hangzhou"
}

{
  "title":"add task",
  "due_date":"2018-02-28",
  "description":"add task test",
  "assignees": [8,28]
}

# add comment

/m/task/<task_id>/comments POST
{
	"content": "add comment test",
	"attachments": [1, 2]
}

# add reply

/m/task/<task_id>/comment/<comment_id>/replies POST
{
	"content": "add reply",
	"to_uid": 3,
	"at": "Leo"
}