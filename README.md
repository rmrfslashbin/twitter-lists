# twitter-lists
Manage Twitter lists, users, and other random things.

## Setup
### API Keys
Twitter API consumer and access tokens are required. Go to https://developer.twitter.com/en/apps and set up a new app with minimal defaults. The **Keys and tokens** pane will contain the required **Consumer API keys** and **Access token & access token secret**. Make note of these keys.
### Username and User ID
Finding your Twitter @username is easy. The User ID, not as obvious. Log into Twitter. Go to Settings And Privacy ==> Account ==> Your Twitter data ==> Account... Then under the "Username" field, find you User ID.
### Settings.json
With these three data points in hand, set up the the app by running ```./configure``` or ```cp settings.json.DIST settings.json``` and fill in the values manually.

## General Use
### Data
First things first: data. Run ```./fetchData``` to populate the local data store.

## Queries
Several scripts are provided to provide insights:
Script | Descr
------------ | -------------
list-lists | Listing of your Twitter lists and lists to which you follow
showUser | Listing of users to which your account follows
users-in-lists | Listing of the users your account follows and which lists of which they are members
users-not-in-a-list | Listing of users your account follows which are not a member of any of your lists
streamList | not-fully-baked stream of user or list
