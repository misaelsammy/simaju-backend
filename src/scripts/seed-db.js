const { pool } = require('../config/db');

async function seedDatabase() {
  if (!process.env.DATABASE_URL) {
    console.error('ERROR: DATABASE_URL is not defined in environment variables or .env');
    process.exit(1);
  }

  const client = await pool.connect();
  try {
    console.log('Seeding initial test data into SIMAJU database...');
    await client.query('BEGIN');

    // 1. Insert Users
    const userRes = await client.query(`
      INSERT INTO users (name, email, password_hash, instansi)
      VALUES 
        ('Misael Sammy Gideon', 'misael@simaju.ac.id', '$2b$10$SampleHashedPasswordForDemo1234567890', 'Universitas Dian Nuswantoro'),
        ('Budi Santoso', 'budi.santoso@simaju.ac.id', '$2b$10$SampleHashedPasswordForDemo1234567890', 'Politeknik Negeri')
      RETURNING user_id, name, email;
    `);
    const user1 = userRes.rows[0];
    const user2 = userRes.rows[1];
    console.log(`Inserted ${userRes.rows.length} users.`);

    // 2. Insert User Preferences
    await client.query(`
      INSERT INTO user_preferences (user_id, default_reminder_minutes, theme)
      VALUES 
        ($1, 15, 'dark'),
        ($2, 30, 'light');
    `, [user1.user_id, user2.user_id]);
    console.log('Inserted user preferences.');

    // 3. Insert Groups
    const groupRes = await client.query(`
      INSERT INTO groups (group_name, created_by)
      VALUES 
        ('Tim Pengembang SIMAJU', $1),
        ('Divisi Riset & Proyek', $2)
      RETURNING group_id, group_name;
    `, [user1.user_id, user2.user_id]);
    const group1 = groupRes.rows[0];
    const group2 = groupRes.rows[1];
    console.log(`Inserted ${groupRes.rows.length} groups.`);

    // 4. Insert Group Members
    await client.query(`
      INSERT INTO group_members (group_id, user_id)
      VALUES 
        ($1, $2),
        ($1, $3),
        ($4, $3);
    `, [group1.group_id, user1.user_id, user2.user_id, group2.group_id]);
    console.log('Inserted group members.');

    // 5. Insert Recurring Pattern
    const patternRes = await client.query(`
      INSERT INTO recurring_patterns (frequency, end_date)
      VALUES ('weekly', '2026-12-31')
      RETURNING pattern_id;
    `);
    const pattern1 = patternRes.rows[0];
    console.log('Inserted recurring pattern.');

    // 6. Insert Events
    const eventRes = await client.query(`
      INSERT INTO events (user_id, group_id, pattern_id, title, description, start_time, end_time, is_skipped)
      VALUES 
        ($1, $2, NULL, 'Sprint Planning SIMAJU', 'Rapat mingguan pembahasan backlog dan arsitektur API', '2026-11-01 09:00:00', '2026-11-01 11:00:00', false),
        ($1, NULL, $3, 'Evaluasi Proyek Mingguan', 'Review berkala pencapaian deliverable', '2026-11-03 14:00:00', '2026-11-03 15:30:00', false),
        ($4, $5, NULL, 'Diskusi Riset Backend', 'Pembahasan arsitektur serverless di Vercel', '2026-11-05 10:00:00', '2026-11-05 12:00:00', false)
      RETURNING event_id, title;
    `, [user1.user_id, group1.group_id, pattern1.pattern_id, user2.user_id, group2.group_id]);
    const event1 = eventRes.rows[0];
    const event2 = eventRes.rows[1];
    console.log(`Inserted ${eventRes.rows.length} events.`);

    // 7. Insert Reminders
    await client.query(`
      INSERT INTO reminders (event_id, remind_at, is_sent, notification_type)
      VALUES 
        ($1, '2026-11-01 08:45:00', false, 'email'),
        ($2, '2026-11-03 13:45:00', false, 'push_notification');
    `, [event1.event_id, event2.event_id]);
    console.log('Inserted reminders.');

    await client.query('COMMIT');
    console.log('✅ Seeding completed successfully!');
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('❌ Failed to seed database:', error.message);
    process.exit(1);
  } finally {
    client.release();
    await pool.end();
  }
}

if (require.main === module) {
  seedDatabase();
}

module.exports = { seedDatabase };
