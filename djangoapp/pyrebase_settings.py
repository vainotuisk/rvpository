import pyrebase

config = {
    "apiKey": "AIzaSyBCmCIIxZ7pVEdQWvdM8WxmQv5LPb8yZak",
    "authDomain": "scorching-inferno-1325.firebaseapp.com",
    "databaseURL": "https://scorching-inferno-1325.firebaseio.com",
    "projectId": "scorching-inferno-1325",
    "storageBucket": "",
    "serviceAccount": "rvpository-7b59e0c3deda.json",
    "messagingSenderId": "333374404394"
}

# initialize app with config
firebase = pyrebase.initialize_app(config)

# authenticate a user
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("vainotuisk@gmail.com", "12T00likest")



db = firebase.database()

