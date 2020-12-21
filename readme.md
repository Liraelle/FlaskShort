`FlaskShort` a test task REST API to generate short redirecting URL from original.
To realize that task I used Flask, Flask-RESTful, SQLite3.

The startup file is app.py. 
In db.py we creating SQLAlchemy object to easily put/get information in/from database.

For testing REST API I used Postman (v.7.36.1).

**Usage**
---

For testing this API need to run API (using developer server, localhost). Than in Postman use method GET and type in field "Enter request URL" localhost:5000 (default port). In option "Body" choose "raw" and JSON format. In text field type, for example:
```
{
    "URL": "https://stackoverflow.com/", 
    "URL_expiration": 5 
}
```

In "URL" can be any URL, in "URL_expiration" can be number from 1 to 365 (days). If you type:

```
{
    "URL": "https://stackoverflow.com/" 
}
```

"URL_expiration" will be 90 days by default. After that press "Send". In Response window will be showing:

```
{
    "short_link": "http://localhost:5000/Dm0K 
}
```

After that needs to copy that short URL, paste in "Enter request URL", in "Body" choose "None" and press "Send". After that in Response window choose "Body", then "Preview". It should show page from original URL after redirecting from short URL.

In API for simpler testing inside code I changed limit from 1 million to much less. (In link_resource.py, db_limit):
```
        db_limit = 1000000
```

For testing in case expired URL in database, I changing date on older (in link_resource.py, commented lines 33, 41), by commenting 32, 40 lines and uncomment 33, 41 lines:
```
            #exp_date = datetime.date(2020, 7, 12) + datetime.timedelta(days=90)
            exp_date = datetime.date.today() + datetime.timedelta(days=90)
```