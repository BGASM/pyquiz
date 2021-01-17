DROP TABLE IF EXISTS quiz;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS mcq;
DROP TABLE IF EXISTS user;


CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT
);

CREATE TABLE quiz(
    quiz_ID INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    course TEXT NOT NULL,
    no_questions INTEGER,
    user TEXT NOT NULL,
    ranking INTEGER NOT NULL
);

CREATE TABLE question(
    quiz_ID TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    course TEXT NOT NULL,
    PRIMARY KEY (quiz_ID, question)
);

CREATE TABLE mcq(
    q_ID TEXT NOT NULL,
    mcq TEXT NOT NULL,
    PRIMARY KEY (q_ID, mcq)
)

