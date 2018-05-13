CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY, 
    name TEXT NOT NULL,
    date DATE NOT NULL,
    estimate FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS budget_rules (
    id INTEGER PRIMARY KEY, 
    sentence TEXT NOT NULL,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    new BOOLEAN,
    account_date DATE,
    operation_date DATE,
    details TEXT,
    account_no TEXT,
    title TEXT,
    amount FLOAT,
    currency TEXT,
    ref_number TEXT,
    operation_type TEXT,
    note TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
);