# Simple CRUD REST implementation

The purpose of this project is to explore different implementations of a REST server providing CRUD operations on "notes".

The notes have the following attributes:
* `id`: auto-increment primary key.
* `text`: a string.
* `created_at`: datetime automatically set when a note is created.
* `updated_at`: datetime automatically set when a note is updated.

The data is stored in an SQLite database.

The server provides the following REST routes:
* Create a note: `POST /notes/`
* List notes: `GET /notes/`
* Get a note: `GET /notes/<note id>`
* Update a note: `PUT /notes/<note id>` 
* Delete a note: `DELETE /notes/<note id>`

## Implementations
Currently implementations for FastAPI, Flask, and Django REST Framework are done.

The goal is to be able to compare the different frameworks and learn about their trade-offs.

## Running


In each of the implementations, the server can be run as follows:

Change directory into the implementation folder:
```
cd fastapi
```


Run the server with `./scripts/run.sh`.

Then, you can use the server:


*Create a note*:
```
curl -X POST -H "content-type: application/json"  localhost:8000/notes/ -d '{"text": "some note text"} '
```

*List all notes*:
```
curl localhost:8000/notes/
```

*Read a note with id 1*:
```
curl localhost:8000/notes/1
```

*Modify the note with id 1*:
```
curl -X PUT -H "content-type: application/json"  localhost:8000/notes/1 -d '{"text": "some note text"} '
```

*Delete the note with id 1*:
```
curl -X DELETE localhost:8000/notes/1
```


## Limitations
* No user account management is implemented. Any client can modify and read all the notes.
* The project isn't currently Dockerized.
* No work has been done for deploying the servers in a production environment.


