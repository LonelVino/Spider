/*
    create connection to initial mongodb container
*/

// create mongo connection
conn = new Mongo("127.0.0.1:27018");
// use database
db = conn.getDB('admin');

// to initial administrator
print(`Create datatabse: ${db}, and then enter administator passwd.`);

// create administrator
db.createUser(
    {
        user: "admin",
        pwd: passwordPrompt(),
        roles: [
            { role: "root", db: "admin" }
        ]
    }
);
print();
// Connect: mongosh --port 27017 --authenticationDatabase "admin" -u "admin" -p

// auth as admin
print("Enter passwd to auth as admin.");
db.auth("admin", passwordPrompt());
print();

// change database to weibo
db = db.getSiblingDB('weibo');

// create user for weibo database
print("Enter passwd to for weibo database user.");
db.createUser(
    {
        user: "weibo",
        pwd: passwordPrompt(),
        roles: [
            { role: "readWrite", db: "weibo" }
        ]
    }
);
print();


/*
db.createCollection(): Creates a new collection or view. 
A collection is a grouping of MongoDB documents.
A collection is the equivalent of a table in a relational database system.  
*/

// create target collection
db.createCollection('user');
db.createCollection('user_post');
db.createCollection('tag_post');
db.createCollection('longtext');
db.createCollection('error_log');
print("Successfully create collections.");

conn.close();
print("Mongodb initial finished.");
