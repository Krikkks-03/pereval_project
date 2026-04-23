-- 1. Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    fam VARCHAR(100),
    name VARCHAR(100),
    otc VARCHAR(100)
);

-- 2. Таблица координат
CREATE TABLE IF NOT EXISTS coords (
    id SERIAL PRIMARY KEY,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    height INTEGER
);

-- 3. Основная таблица перевалов (улучшенная, без JSON)
CREATE TABLE IF NOT EXISTS pereval (
    id SERIAL PRIMARY KEY,
    beauty_title VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    other_titles TEXT,
    connect TEXT,
    add_time TIMESTAMP DEFAULT NOW(),
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    coords_id INTEGER NOT NULL REFERENCES coords(id) ON DELETE CASCADE,
    level_winter VARCHAR(10),
    level_summer VARCHAR(10),
    level_autumn VARCHAR(10),
    level_spring VARCHAR(10),
    status VARCHAR(20) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT valid_status CHECK (status IN ('new', 'pending', 'accepted', 'rejected'))
);

-- 4. Таблица изображений
CREATE TABLE IF NOT EXISTS pereval_images (
    id SERIAL PRIMARY KEY,
    pereval_id INTEGER NOT NULL REFERENCES pereval(id) ON DELETE CASCADE,
    title VARCHAR(255),
    img_data TEXT
);

-- Индексы для производительности
CREATE INDEX IF NOT EXISTS idx_pereval_status ON pereval(status);
CREATE INDEX IF NOT EXISTS idx_pereval_user_id ON pereval(user_id);
CREATE INDEX IF NOT EXISTS idx_pereval_coords_id ON pereval(coords_id);
CREATE INDEX IF NOT EXISTS idx_images_pereval_id ON pereval_images(pereval_id);