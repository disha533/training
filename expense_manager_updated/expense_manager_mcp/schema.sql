

CREATE TABLE expenses (
    id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    amount        NUMBER(10,2) NOT NULL,
    category      VARCHAR2(100) NOT NULL,
    description   VARCHAR2(500),
    expense_date  DATE NOT NULL
);

