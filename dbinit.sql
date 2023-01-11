CREATE TABLE users (
    id SERIAL PRIMARY KEY NOT NULL,
    email VARCHAR(100),
    password VARCHAR(100),
    name VARCHAR(1000),
    UNIQUE(email)
);

CREATE TABLE todos (
    id SERIAL PRIMARY KEY NOT NULL,
    task VARCHAR(250) NOT NULL,
    date TIMESTAMP,
    is_completed BOOLEAN,
    description VARCHAR(250),
    date_created TIMESTAMP,
    user_id INTEGER, 
    FOREIGN KEY(user_id) REFERENCES users (id)
);

