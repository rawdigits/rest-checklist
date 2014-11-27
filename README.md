rest-checklist
==============

A RESTful checklist API using Flask/Python with a text file backend. No state is kept by the server. Every operation is atomic. Why files? Because I can edit them in vim when I feel like it.

dependencies
------------
flask

configuration
------------
config.json

    {"tokens":  ["(secret for user id)"],  "key": "(signs sessions, unused currently)"}0

restful paths
-------------

Show all lists

    http://example.com/lists?token=(secret for user id)

Create a list

    http://example.com/lists/add?token=(secret for user id)

Show list contents

    http://example.com/lists/(list name)?token=(secret for user id)

Add a list item

    http://example.com/lists/(list name)/add?token=(secret for user id)

Mark a list item complete

    http://example.com/lists/(list name)/done/(list item)?token=(secret for user id)

Mark a list item incomplete

    http://example.com/lists/(list name)/undone/(list item)?token=(secret for user id)
