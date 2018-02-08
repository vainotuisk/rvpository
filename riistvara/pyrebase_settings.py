import pyrebase

config = {
    "apiKey": "AIzaSyBCmCIIxZ7pVEdQWvdM8WxmQv5LPb8yZak",
    "authDomain": "scorching-inferno-1325.firebaseapp.com",
    "databaseURL": "https://scorching-inferno-1325.firebaseio.com",
    "projectId": "scorching-inferno-1325",
    "storageBucket": "",
    "serviceAccount": "my_serviceAccount.json_file_path_is_here",
    "messagingSenderId": "333374404394"
}

# initialize app with config
firebase = pyrebase.initialize_app(config)

# authenticate a user
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("email@usedforauthentication.com", "FstrongPasswordHere")


db = firebase.database()

