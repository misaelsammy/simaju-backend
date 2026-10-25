const db = require('../config/db');

// 1. getAllReminders (bisa filter upcoming=true atau is_sent)
async function getAllReminders(req, res, next) {
  try {
    const { is_sent, upcoming } = req.query;

    let queryStr = `
      SELECT r.reminder_id, r.event_id, e.title AS event_title, 
             e.start_time AS event_start_time,
             r.remind_at, r.is_sent, r.notification_type,
             u.user_id, u.name AS user_name, u.email AS user_email
      FROM reminders r
      JOIN events e ON r.event_id = e.event_id
      JOIN users u ON e.user_id = u.user_id
      WHERE 1=1
    `;
    const params = [];

    if (is_sent !== undefined) {
      params.push(is_sent === 'true');
      queryStr += ` AND r.is_sent = $${params.length}`;
    }

    if (upcoming === 'true') {
      queryStr += ` AND r.remind_at >= NOW() AND r.is_sent = FALSE`;
    }

    queryStr += ` ORDER BY r.remind_at ASC`;

    const result = await db.query(queryStr, params);

    res.status(200).json(result.rows);
  } catch (err) {
    next(err);
  }
}

// 2. createReminder
async function createReminder(req, res, next) {
  try {
    const { event_id, remind_at, notification_type } = req.body;

    if (!event_id || !remind_at) {
      return res.status(400).json({ error: 'Field event_id dan remind_at wajib diisi' });
    }

    const eventCheck = await db.query('SELECT event_id FROM events WHERE event_id = $1', [event_id]);
    if (eventCheck.rows.length === 0) {
      return res.status(404).json({ error: `Jadwal dengan ID ${event_id} tidak ditemukan` });
    }

    const result = await db.query(
      `INSERT INTO reminders (event_id, remind_at, is_sent, notification_type)
       VALUES ($1, $2, false, $3)
       RETURNING *`,
      [event_id, remind_at, notification_type || 'email']
    );

    res.status(201).json(result.rows[0]);
  } catch (err) {
    next(err);
  }
}

// 3. markReminderAsSent (PATCH)
async function markReminderAsSent(req, res, next) {
  try {
    const { id } = req.params;

    const result = await db.query(
      `UPDATE reminders
       SET is_sent = TRUE
       WHERE reminder_id = $1
       RETURNING *`,
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: `Pengingat dengan ID ${id} tidak ditemukan` });
    }

    res.status(200).json({
      message: 'Pengingat berhasil ditandai sebagai terkirim',
      data: result.rows[0]
    });
  } catch (err) {
    next(err);
  }
}

// 4. deleteReminder (DELETE)
async function deleteReminder(req, res, next) {
  try {
    const { id } = req.params;

    const result = await db.query('DELETE FROM reminders WHERE reminder_id = $1 RETURNING *', [id]);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: `Pengingat dengan ID ${id} tidak ditemukan` });
    }

    res.status(200).json({
      message: 'Pengingat berhasil dihapus',
      deleted_id: parseInt(id)
    });
  } catch (err) {
    next(err);
  }
}

module.exports = {
  getAllReminders,
  createReminder,
  markReminderAsSent,
  deleteReminder
};
