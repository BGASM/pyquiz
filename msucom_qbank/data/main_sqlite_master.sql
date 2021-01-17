INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'quiz', 'quiz', 2, 'CREATE TABLE quiz(
    quiz_ID INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    course TEXT NOT NULL,
    no_questions INTEGER,
    ranking INTEGER NOT NULL
)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'question', 'question', 3, 'CREATE TABLE question(
    quiz_ID TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    course TEXT NOT NULL,
    PRIMARY KEY (quiz_ID, question)
)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('index', 'sqlite_autoindex_question_1', 'question', 4, null);
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('table', 'mcq', 'mcq', 5, 'CREATE TABLE mcq(
    q_ID TEXT NOT NULL,
    mcq TEXT NOT NULL,
    PRIMARY KEY (q_ID, mcq)
)');
INSERT INTO sqlite_master (type, name, tbl_name, rootpage, sql) VALUES ('index', 'sqlite_autoindex_mcq_1', 'mcq', 6, null);