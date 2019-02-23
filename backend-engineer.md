# Backend Developer Challenge

## Problem Statement

You have to create a django application that allows users to add new notes
through an API. When a note is added or updated, trigger a translation of
some fields into a particular language.

## Specifications

The API should have the following endpoints:

1. Create a new note.
2. Update a note.
3. Read a note.
4. Delete a note, in which case, all translations should be removed, too.
5. Find translations of a note. This part of the task is optional.

A note may have the following fields: `name`, `description`, `creator`, `id`.
You can add more fields if you want.

Whenever a new note is added, or updated, trigger a translation of `name` and
`description` fields using the Google Translate API. Store the translation.

**IMPORTANT**: You must NOT use any database to store the notes. All notes must be
stored on the filesystem, and accessible through the API.

AUTHORIZATION: All users of the API must authenticate using an API key that
is provided to them by making a POST request to an endpoint served by your app.

## Example implementation

### GET Request (all notes)

```
Headers: Authorization: <some_api_key>
GET /api/note/
```

```
{
  "meta": {
    "objects": 1,
    "page": 1,
    "next": null
  },
  
  "objects": [
    {
      "name": "Awesome note",
      "description": "This is an awesome note.",
      "creator": "<some_api_key>",
      "id": 1
    }
  ]
}
```

### GET Request (one note)

```
Headers: Authorization: <some_api_key>
GET /api/note/1
```

```
{
  "name": "Awesome note",
  "description": "This is an awesome note.",
  "creator": "<some_api_key>",
  "id": 1
}
```

### POST Request

REQUEST:
```
Headers: Authorization: <some_api_key>
POST /api/note/

{
  "name": "Another awesome note",
  "description": "This is an awesome note too.",
}
```

RESPONSE:
```
{
  "name": "Another awesome note",
  "description": "This is an awesome note too.",
  "creator": "<some_api_key>",
  "id": 2
}
```

### PATCH Request

REQUEST:
```
Headers: Authorization: <some_api_key>
PATCH /api/note/

{
  "name": "Edited another awesome note",
  "description": "This is an edited awesome note too.",
}
```

RESPONSE:
```
{
  "name": "Edited another awesome note",
  "description": "This is an edited awesome note too.",
  "creator": "<some_api_key>",
  "id": 2
}
```

### Generate the API key

```
POST /api/generate_key
```

```
{
  "api_key": "<some_api_key>"
}
```

### Get translations of a note (optional)

```
Headers: Authorization: <some_api_key>
GET /api/note/1/translations/<language>
```

NOTE: For the sake of simplicity, add translation support for Hindi only.

```
{
  "name": "कमाल का नोट",
  "description": "यह एक कमाल का नोट है।"
  "creator": "<some_api_key>",
  "id": 1
}
```
