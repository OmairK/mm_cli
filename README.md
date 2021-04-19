# Mail Management CLI (mm_cli)
A mail management cli tool to moves/marks emails to different labels and categories. The emails are fetched through gmail apis and processed locally and updated again via the gmail api.

## Setting up
1. Create a [google cloud platform project](https://developers.google.com/workspace/guides/create-project) and enable the gmail api.
2. Create a [oauth client secret](https://developers.google.com/workspace/guides/create-credentials) for this app with the appropriate scope i.e. `https://mail.google.com/` which gives it all the permissions over your inbox. This access could be granularised according to the need.
3. Save the credentials file as credentials.json at the root of the directory, this path is configurable via config or cli args.
4. Installing the requirements(in a virtual env)
```

$ pip install -r requirements/commont.txt

# Dev requirements
$ pip install -r requirements/dev.txt
```
5. Database setup
	* Create a user foo with password bar
	* Create a database testdb and grant the user foo all previlleges on that database.
	* All these settings are configurable in configs/db_config.py

```
# To get a list of cli args run
$ python main.py --help

# Run
$ python main.py
```
