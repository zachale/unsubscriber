### Unsubscriber (unscriber for short)

This is a simple tool that scrapes your Gmail inbox for unsubscribe links and formats them for you in a list within a React App.
This tool requires a some technical skill to get working, so beware. 

This will be turned into a web app in the future,

### MANDATORY DEPENDENCIES

You must have python 3.10.11 or NEWER installed and useable
You must have node.js 20.11.0 or NEWER installed and useable

### Setup

This is a bring your own credentials tool, so make sure you are set up with the Gmail API.

you will need to follow these guys if you arent already familiar:
https://developers.google.com/workspace/guides/create-project -> create the project
https://developers.google.com/workspace/guides/enable-apis -> enable your api access (select the Gmail API)


Once you get your credentials, put the json given to you with your credentials in a file named "credentials.json" in the data folder.

optional: go to scraper.py, tweak the DATE constant to your liking

Run these commands:
```pip install -r requirements.txt``` 
```python data/scraper.py``` 
This should install all nessascary libraries and run the script

Sign in with your google acount on the website that should pop up,

Wait until "done!" is printed to the terminal before continuing, you may have to wait several minutes

Run these commands
```cd unscriber/unscriber```
```npm start```

You are all done!
Explore the opened react app!



### Wishlist (TODO)

- Convert python script into a true webserver (allowing for a simple setup process)
- Implement a more efficient search algorithm for the final check
- Streamline the number of API calls needed
- Make date default to 7 days in the past