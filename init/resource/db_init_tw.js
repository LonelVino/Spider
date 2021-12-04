/*
    create connection to initial mongodb container
*/

// create mongo connection
conn = new Mongo("127.0.0.1:27019");
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
// Connect: mongosh --port 27019 --authenticationDatabase "admin" -u "admin" -p

// auth as admin
print("Enter passwd to auth as admin.");
db.auth("admin", passwordPrompt());
print();

// change database to twitter
db = db.getSiblingDB('twitter');

// create user for twitter database
print("Enter passwd to for twitter database user.");
db.createUser(
    {
        user: "twitter",
        pwd: passwordPrompt(),
        roles: [
            { role: "readWrite", db: "twitter" }
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
db.createCollection('tag_tweet');
db.createCollection('error_log');
print("Successfully create collections.");

conn.close();
print("Twitter Mongodb initial finished.");
