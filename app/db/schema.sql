CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE expense_category (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE expense (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    category_id UUID REFERENCES expense_category(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    amount FLOAT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE saving_category (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    goal FLOAT NOT NULL,
    is_goal_achieved BOOLEAN DEFAULT FALSE
);

CREATE TABLE saving (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    category_id UUID REFERENCES saving_category(id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);