CREATE TABLE poasts (KEY SERIAL PRIMARY KEY,
  ID CHAR(9) UNIQUE NOT NULL,
  CONTENT TEXT NOT NULL,
  TITLE VARCHAR(30),
  DELETED TIMESTAMP,
  DATE_UPLOADED TIMESTAMP NOT NULL,
  VIEWS INT DEFAULT 1
);

INSERT INTO poasts (ID, CONTENT, TITLE, DELETED, DATE_UPLOADED, VIEWS)
VALUES ('NieWFn23g', 'this is a test insert into the table', 'test title', null, '2018-10-18 22:20:46', '1');

INSERT INTO poasts (ID, CONTENT, TITLE, DELETED, DATE_UPLOADED, VIEWS)
VALUES ('meI9120NN', 'OPWEIFJWPOEIJFWPOFIJEPOIFJWPOIFWPOIFJPWOEIFJWOPFJWOPJIOFJ', 'test title NUMBER 2', null, '2018-10-18 22:24:08', '1');
