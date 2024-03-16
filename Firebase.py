import firebase_admin
from firebase_admin import db
cred = firebase_admin.credentials.Certificate("comp7940-797cf-firebase-adminsdk-k9zfo-457c0104e5.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://comp7940-797cf-default-rtdb.firebaseio.com/'
})
class firebase():
    def submit_data(self,record):
        db_ref = db.reference('/')
        data = db_ref.child('comp7940_group').get()
        data_count = 0
        if data:
            for key in data.keys():
                data_count = data_count + 1
            db_ref.child("comp7940_group").child('record' + str(data_count)).set(record)
        else:
            db_ref.child("comp7940_group").child('record' + str(data_count)).set(record)