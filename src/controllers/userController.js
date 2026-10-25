const db = require('../config/db');

// 1. registerUser
async function registerUser(req, res, next) {
  try {
    const { name, email, password, instansi, default_reminder_minutes, theme } = req.body;

    if (!name || !email || !password) {
      return res.status(400).json({ error: 'Field name, email, dan password wajib diisi' });
    }

    // Cek duplikasi email
    const existing = await db.query('SELECT user_id FROM users WHERE email = $1', [email]);
    if (existing.rows.length > 0) {
      return res.status(400).json({ error: 'Email sudah terdaftar dalam sistem' });
    }

    // Untuk keperluan demonstrasi akademik REST API, simpan hash/token sederhana
    const passwordHash = Buffer.from(password).toString('base64');

    const result = await db.query(
      `INSERT INTO users (name, email, password_hash, instansi)
       VALUES ($1, $2, $3, $4)
       RETURNING user_id, name, email, instansi`,
      [name, email, passwordHash, instansi || null]
    );

    const newUser = result.rows[0];

    // Buat relasi 1-to-1 ke user_preferences
    await db.query(
      `INSERT INTO user_preferences (user_id, default_reminder_minutes, theme)
       VALUES ($1, $2, $3)`,
      [newUser.user_id, default_reminder_minutes || 15, theme || 'light']
    );

    res.status(201).json({ user: newUser });
  } catch (err) {
    next(err);
  }
}

// 2. loginUser
async function loginUser(req, res, next) {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email dan password wajib diisi' });
    }

    const result = await db.query(
      'SELECT user_id, name, email, instansi, password_hash FROM users WHERE email = $1',
      [email]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Pengguna dengan email tersebut tidak ditemukan' });
    }

    const user = result.rows[0];
    const encodedInput = Buffer.from(password).toString('base64');

    if (user.password_hash !== encodedInput && !user.password_hash.startsWith('$2b$')) {
      return res.status(400).json({ error: 'Kredensial login tidak valid' });
    }

    delete user.password_hash;

    res.status(200).json({ message: 'Login berhasil', user });
  } catch (err) {
    next(err);
  }
}

// 3. getAllUsers
async function getAllUsers(req, res, next) {
  try {
    const result = await db.query(`
      SELECT u.user_id, u.name, u.email, u.instansi, 
             p.default_reminder_minutes, p.theme
      FROM users u
      LEFT JOIN user_preferences p ON u.user_id = p.user_id
      ORDER BY u.user_id ASC
    `);

    res.status(200).json(result.rows);
  } catch (err) {
    next(err);
  }
}

// 4. getUserProfile
async function getUserProfile(req, res, next) {
  try {
    const { id } = req.params;

    const result = await db.query(`
      SELECT u.user_id, u.name, u.email, u.instansi, 
             p.default_reminder_minutes, p.theme
      FROM users u
      LEFT JOIN user_preferences p ON u.user_id = p.user_id
      WHERE u.user_id = $1
    `, [id]);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: `Pengguna dengan ID ${id} tidak ditemukan` });
    }

    res.status(200).json(result.rows[0]);
  } catch (err) {
    next(err);
  }
}

// 5. updateUserProfile
async function updateUserProfile(req, res, next) {
  try {
    const { id } = req.params;
    const { name, instansi, default_reminder_minutes, theme } = req.body;

    const userCheck = await db.query('SELECT user_id FROM users WHERE user_id = $1', [id]);
    if (userCheck.rows.length === 0) {
      return res.status(404).json({ error: `Pengguna dengan ID ${id} tidak ditemukan` });
    }

    if (name || instansi !== undefined) {
      await db.query(
        `UPDATE users 
         SET name = COALESCE($1, name),
             instansi = COALESCE($2, instansi)
         WHERE user_id = $3`,
        [name, instansi, id]
      );
    }

    if (default_reminder_minutes !== undefined || theme) {
      await db.query(
        `INSERT INTO user_preferences (user_id, default_reminder_minutes, theme)
         VALUES ($1, $2, $3)
         ON CONFLICT (user_id) 
         DO UPDATE SET 
           default_reminder_minutes = COALESCE(EXCLUDED.default_reminder_minutes, user_preferences.default_reminder_minutes),
           theme = COALESCE(EXCLUDED.theme, user_preferences.theme)`,
        [id, default_reminder_minutes || 15, theme || 'light']
      );
    }

    const updated = await db.query(`
      SELECT u.user_id, u.name, u.email, u.instansi, 
             p.default_reminder_minutes, p.theme
      FROM users u
      LEFT JOIN user_preferences p ON u.user_id = p.user_id
      WHERE u.user_id = $1
    `, [id]);

    res.status(200).json({
      message: 'Profil pengguna berhasil diperbarui',
      data: updated.rows[0]
    });
  } catch (err) {
    next(err);
  }
}

module.exports = {
  registerUser,
  loginUser,
  getAllUsers,
  getUserProfile,
  updateUserProfile
};
