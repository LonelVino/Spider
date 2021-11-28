conn = new Mongo("127.0.0.1:27017");
db = conn.getDB('admin');

print('Create databse: ${db}, and then enter administration passwd');

db.createUser( 
    {
        user:"admin",
        pwd: passwordPrompt(),   // Instead of specifying the password in cleartext
        roles:[ 
            {role: 'root', db: 'admin'}
         ]
    } 
);
print();

print('Enter password to auth as admin');
db.auth('admin', passwordPrompt());
print();

db  = db.getSiblingDB('weibo');

print('Enter password for weibo database user');

db.createUser( 
    {
        user:"weibo",
        pwd: passwordPrompt(),   // Instead of specifying the password in cleartext
        roles:[ 
            {role: 'readWrite', db: 'weibo'}
         ]
    } 
);
print();

db.createCollection('user')
db.createCollection('post')
db.createCollection('error_log')
db.createCollection('longtext')
print('Successfully create collections.');

conn.close()
print('Mongdb initial finished!')