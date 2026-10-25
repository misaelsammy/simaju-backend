const db = require('../config/db');

// Helper: checkScheduleConflict (Cek apakah jadwal bentrok)
async function hasConflict(userId, startTime, endTime, excludeEventId = null) {
  let queryStr = `
    SELECT event_id, title, start_time, end_time 
    FROM events 
    WHERE user_id = $1 
      AND is_skipped = FALSE
      AND NOT (end_time <= $2 OR start_time >= $3)
  `;
  const params = [userId, startTime, endTime];

  if (excludeEventId) {
    queryStr += ` AND event_id != $4`;
    params.push(excludeEventId);
  }

  const result = await db.query(queryStr, params);
  return result.rows;
}

// 1. getAllEvents (dengan filter user_id, start_date, end_date, group_id)
async function getAllEvents(req, res, next) {
  try {
    const { user_id, start_date, end_date, group_id } = req.query;

    let queryStr = `
      SELECT e.event_id, e.user_id, u.name AS user_name,
             e.group_id, g.group_name,
             e.pattern_id, rp.frequency AS recurring_frequency,
             e.title, e.description, e.start_time, e.end_time, e.is_skipped
      FROM events e
      LEFT JOIN users u ON e.user_id = u.user_id
      LEFT JOIN groups g ON e.group_id = g.group_id
      LEFT JOIN recurring_patterns rp ON e.pattern_id = rp.pattern_id
      WHERE 1=1
    `;
    const params = [];

    if (user_id) {
      params.push(user_id);
      queryStr += ` AND e.user_id = $${params.length}`;
    }

    if (group_id) {
      params.push(group_id);
      queryStr += ` AND e.group_id = $${params.length}`;
    }

    if (start_date) {
      params.push(start_date);
      queryStr += ` AND e.end_time >= $${params.length}`;
    }

    if (end_date) {
      params.push(end_date);
      queryStr += ` AND e.start_time <= $${params.length}`;
    }

    queryStr += ` ORDER BY e.start_time ASC`;

    const result = await db.query(queryStr, params);

    res.status(200).json({
      message: 'Berhasil mengambil daftar jadwal kegiatan',
      total: result.rows.length,
      data: result.rows
    });
  } catch (err) {
    next(err);
  }
}

// 2. getEventById
async function getEventById(req, res, next) {
  try {
    const { id } = req.params;

    const eventResult = await db.query(`
      SELECT e.event_id, e.user_id, u.name AS user_name, u.email AS user_email,
             e.group_id, g.group_name,
             e.pattern_id, rp.frequency AS recurring_frequency, rp.end_date AS recurring_end_date,
             e.title, e.description, e.start_time, e.end_time, e.is_skipped
      FROM events e
      LEFT JOIN users u ON e.user_id = u.user_id
      LEFT JOIN groups g ON e.group_id = g.group_id
      LEFT JOIN recurring_patterns rp ON e.pattern_id = rp.pattern_id
      WHERE e.event_id = $1
    `, [id]);

    if (eventResult.rows.length === 0) {
      return res.status(404).json({ error: `Jadwal dengan ID ${id} tidak ditemukan` });
    }

    // Ambil daftar reminders untuk event ini
    const remindersResult = await db.query(`
      SELECT reminder_id, remind_at, is_sent, notification_type
      FROM reminders
      WHERE event_id = $1
      ORDER BY remind_at ASC
    `, [id]);

    const eventData = eventResult.rows[0];
    eventData.reminders = remindersResult.rows;

    res.status(200).json({
      message: 'Berhasil mengambil detail jadwal',
      data: eventData
    });
  } catch (err) {
    next(err);
  }
}

// 3. createEvent
async function createEvent(req, res, next) {
  try {
    const { user_id, group_id, title, description, start_time, end_time, allow_conflict, recurring } = req.body;

    if (!user_id || !title || !start_time || !end_time) {
      return res.status(400).json({
        error: 'Field user_id, title, start_time, dan end_time wajib diisi'
      });
    }

    if (new Date(start_time) >= new Date(end_time)) {
      return res.status(400).json({
        error: 'Waktu selesai (end_time) harus setelah waktu mulai (start_time)'
      });
    }

    // Validasi apakah user ada
    const userCheck = await db.query('SELECT user_id FROM users WHERE user_id = $1', [user_id]);
    if (userCheck.rows.length === 0) {
      return res.status(404).json({ error: `Pengguna dengan ID ${user_id} tidak ditemukan` });
    }

    // Deteksi Bentrok Jadwal (Conflict Check)
    if (!allow_conflict) {
      const conflicts = await hasConflict(user_id, start_time, end_time);
      if (conflicts.length > 0) {
        return res.status(400).json({
          error: 'Jadwal bentrok dengan kegiatan yang sudah ada',
          conflicts: conflicts
        });
      }
    }

    // Jika membuat recurring event sekaligus
    let patternId = null;
    if (recurring && recurring.frequency) {
      const patternRes = await db.query(
        `INSERT INTO recurring_patterns (frequency, end_date)
         VALUES ($1, $2)
         RETURNING pattern_id`,
        [recurring.frequency, recurring.end_date || null]
      );
      patternId = patternRes.rows[0].pattern_id;
    }

    const result = await db.query(
      `INSERT INTO events (user_id, group_id, pattern_id, title, description, start_time, end_time, is_skipped)
       VALUES ($1, $2, $3, $4, $5, $6, $7, false)
       RETURNING *`,
      [user_id, group_id || null, patternId, title, description || null, start_time, end_time]
    );

    res.status(201).json({
      message: 'Jadwal berhasil ditambahkan',
      data: result.rows[0]
    });
  } catch (err) {
    next(err);
  }
}

// 4. updateEvent (PUT)
async function updateEvent(req, res, next) {
  try {
    const { id } = req.params;
    const { title, description, start_time, end_time, group_id, is_skipped, allow_conflict } = req.body;

    const existingRes = await db.query('SELECT * FROM events WHERE event_id = $1', [id]);
    if (existingRes.rows.length === 0) {
      return res.status(404).json({ error: `Jadwal dengan ID ${id} tidak ditemukan` });
    }

    const current = existingRes.rows[0];
    const newStart = start_time || current.start_time;
    const newEnd = end_time || current.end_time;

    if (new Date(newStart) >= new Date(newEnd)) {
      return res.status(400).json({
        error: 'Waktu selesai (end_time) harus setelah waktu mulai (start_time)'
      });
    }

    if (!allow_conflict && (start_time || end_time)) {
      const conflicts = await hasConflict(current.user_id, newStart, newEnd, id);
      if (conflicts.length > 0) {
        return res.status(400).json({
          error: 'Perubahan waktu menyebabkan bentrok dengan jadwal lain',
          conflicts: conflicts
        });
      }
    }

    const result = await db.query(
      `UPDATE events
       SET title = COALESCE($1, title),
           description = COALESCE($2, description),
           start_time = COALESCE($3, start_time),
           end_time = COALESCE($4, end_time),
           group_id = COALESCE($5, group_id),
           is_skipped = COALESCE($6, is_skipped)
       WHERE event_id = $7
       RETURNING *`,
      [title, description, start_time, end_time, group_id, is_skipped, id]
    );

    res.status(200).json({
      message: 'Jadwal berhasil diperbarui',
      data: result.rows[0]
    });
  } catch (err) {
    next(err);
  }
}

// 5. deleteEvent (DELETE)
async function deleteEvent(req, res, next) {
  try {
    const { id } = req.params;

    const check = await db.query('SELECT event_id, title FROM events WHERE event_id = $1', [id]);
    if (check.rows.length === 0) {
      return res.status(404).json({ error: `Jadwal dengan ID ${id} tidak ditemukan` });
    }

    await db.query('DELETE FROM events WHERE event_id = $1', [id]);

    res.status(200).json({
      message: `Jadwal '${check.rows[0].title}' berhasil dihapus`,
      deleted_id: parseInt(id)
    });
  } catch (err) {
    next(err);
  }
}

// 6. checkScheduleConflict endpoint
async function checkScheduleConflictEndpoint(req, res, next) {
  try {
    const { user_id, start_time, end_time, exclude_event_id } = req.query;

    if (!user_id || !start_time || !end_time) {
      return res.status(400).json({
        error: 'Query parameter user_id, start_time, dan end_time wajib diisi'
      });
    }

    const conflicts = await hasConflict(user_id, start_time, end_time, exclude_event_id);

    res.status(200).json({
      has_conflict: conflicts.length > 0,
      total_conflicts: conflicts.length,
      conflicts: conflicts
    });
  } catch (err) {
    next(err);
  }
}

module.exports = {
  getAllEvents,
  getEventById,
  createEvent,
  updateEvent,
  deleteEvent,
  checkScheduleConflictEndpoint
};
