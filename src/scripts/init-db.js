const { pool } = require('../config/db');

const initSQL = `
-- Drop existing tables if running with --fresh
DROP TABLE IF EXISTS reminders CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS recurring_patterns CASCADE;
DROP TABLE IF EXISTS group_members CASCADE;
DROP TABLE IF EXISTS groups CASCADE;
DROP TABLE IF EXISTS user_preferences CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. Table users
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    instansi VARCHAR(150) 
);

-- 2. Table user_preferences (One-to-One with users)
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    default_reminder_minutes INT DEFAULT 15,
    theme VARCHAR(50) DEFAULT 'light'
);

-- 3. Table groups
CREATE TABLE IF NOT EXISTS groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(150) NOT NULL,
    created_by INT REFERENCES users(user_id) ON DELETE SET NULL
);

-- 4. Table group_members (Many-to-Many pivot between users and groups)
CREATE TABLE IF NOT EXISTS group_members (
    group_id INT REFERENCES groups(group_id) ON DELETE CASCADE,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, user_id)
);

-- 5. Table recurring_patterns
CREATE TABLE IF NOT EXISTS recurring_patterns (
    pattern_id SERIAL PRIMARY KEY,
    frequency VARCHAR(50) NOT NULL,
    end_date DATE
);

-- 6. Table events (Main Resource)
CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    group_id INT REFERENCES groups(group_id) ON DELETE CASCADE, 
    pattern_id INT REFERENCES recurring_patterns(pattern_id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    is_skipped BOOLEAN DEFAULT FALSE 
);

-- 7. Table reminders
CREATE TABLE IF NOT EXISTS reminders (
    reminder_id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(event_id) ON DELETE CASCADE,
    remind_at TIMESTAMP NOT NULL,
    is_sent BOOLEAN DEFAULT FALSE,
    notification_type VARCHAR(50) 
);
`;

async function initializeDatabase() {
  if (!process.env.DATABASE_URL) {
    console.error('ERROR: DATABASE_URL is not defined in environment variables or .env');
    process.exit(1);
  }

  const client = await pool.connect();
  try {
    console.log('Connecting to PostgreSQL database...');
    console.log('Executing database schema initialization (7 tables)...');
    await client.query(initSQL);
    console.log('✅ Database schema initialized successfully:');
    console.log('   - users');
    console.log('   - user_preferences');
    console.log('   - groups');
    console.log('   - group_members');
    console.log('   - recurring_patterns');
    console.log('   - events');
    console.log('   - reminders');
  } catch (error) {
    console.error('❌ Failed to initialize database schema:', error.message);
    process.exit(1);
  } finally {
    client.release();
    await pool.end();
  }
}

if (require.main === module) {
  initializeDatabase();
}

module.exports = { initSQL, initializeDatabase };
