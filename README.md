This repository contains the Backend Assignment and solution to the assignment.

# API Link

URL : https://note--api.herokuapp.com/

```
POST /api/signup 
```
Here you can pass your username and password and confirmation password .
This will create a new user and will create two files ("username.json" , "username_translate".json) for storing all notes of a particular user and the translation respectively.

```
POST /api/generate/

This request will create a token key for authentication .
You can use this key for viewing all the notes and performing 
all operations . You cannot authenticate the user without the token key
 
Response

{"api-key" : <some_api_key>}
```
