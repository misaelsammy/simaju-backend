const db = require('../config/db');

// 1. getAllGroups
async function getAllGroups(req, res, next) {
  try {
    const result = await db.query(`
      SELECT g.group_id, g.group_name, g.created_by, u.name AS creator_name,
             COUNT(gm.user_id)::INT AS total_members
      FROM groups g
      LEFT JOIN users u ON g.created_by = u.user_id
      LEFT JOIN group_members gm ON g.group_id = gm.group_id
      GROUP BY g.group_id, g.group_name, g.created_by, u.name
      ORDER BY g.group_id ASC
    `);

    res.status(200).json({
      message: 'Berhasil mengambil daftar grup',
      total: result.rows.length,
      data: result.rows
    });
  } catch (err) {
    next(err);
  }
}

// 2. getGroupById (dengan daftar anggota)
async function getGroupById(req, res, next) {
  try {
    const { id } = req.params;

    const groupRes = await db.query(`
      SELECT g.group_id, g.group_name, g.created_by, u.name AS creator_name
      FROM groups g
      LEFT JOIN users u ON g.created_by = u.user_id
      WHERE g.group_id = $1
    `, [id]);

    if (groupRes.rows.length === 0) {
      return res.status(404).json({ error: `Grup dengan ID ${id} tidak ditemukan` });
    }

    const membersRes = await db.query(`
      SELECT gm.user_id, u.name, u.email, u.instansi, gm.joined_at
      FROM group_members gm
      JOIN users u ON gm.user_id = u.user_id
      WHERE gm.group_id = $1
      ORDER BY gm.joined_at ASC
    `, [id]);

    const groupData = groupRes.rows[0];
    groupData.members = membersRes.rows;

    res.status(200).json({
      message: 'Berhasil mengambil detail grup',
      data: groupData
    });
  } catch (err) {
    next(err);
  }
}

// 3. createGroup
async function createGroup(req, res, next) {
  try {
    const { group_name, created_by } = req.body;

    if (!group_name || !created_by) {
      return res.status(400).json({ error: 'Field group_name dan created_by wajib diisi' });
    }

    const userCheck = await db.query('SELECT user_id FROM users WHERE user_id = $1', [created_by]);
    if (userCheck.rows.length === 0) {
      return res.status(404).json({ error: `Pengguna dengan ID ${created_by} tidak ditemukan` });
    }

    const groupRes = await db.query(
      `INSERT INTO groups (group_name, created_by)
       VALUES ($1, $2)
       RETURNING *`,
      [group_name, created_by]
    );

    const newGroup = groupRes.rows[0];

    // Otomatis masukkan pembuat grup sebagai anggota pertama
    await db.query(
      `INSERT INTO group_members (group_id, user_id)
       VALUES ($1, $2)`,
      [newGroup.group_id, created_by]
    );

    res.status(201).json({
      message: 'Grup berhasil dibuat',
      data: newGroup
    });
  } catch (err) {
    next(err);
  }
}

// 4. addGroupMember
async function addGroupMember(req, res, next) {
  try {
    const { id } = req.params;
    const { user_id } = req.body;

    if (!user_id) {
      return res.status(400).json({ error: 'Field user_id wajib diisi' });
    }

    const groupCheck = await db.query('SELECT group_id FROM groups WHERE group_id = $1', [id]);
    if (groupCheck.rows.length === 0) {
      return res.status(404).json({ error: `Grup dengan ID ${id} tidak ditemukan` });
    }

    const userCheck = await db.query('SELECT user_id FROM users WHERE user_id = $1', [user_id]);
    if (userCheck.rows.length === 0) {
      return res.status(404).json({ error: `Pengguna dengan ID ${user_id} tidak ditemukan` });
    }

    const memberCheck = await db.query(
      'SELECT * FROM group_members WHERE group_id = $1 AND user_id = $2',
      [id, user_id]
    );
    if (memberCheck.rows.length > 0) {
      return res.status(400).json({ error: 'Pengguna sudah menjadi anggota grup ini' });
    }

    await db.query(
      `INSERT INTO group_members (group_id, user_id)
       VALUES ($1, $2)`,
      [id, user_id]
    );

    res.status(201).json({
      message: 'Anggota berhasil ditambahkan ke dalam grup',
      data: { group_id: parseInt(id), user_id: parseInt(user_id) }
    });
  } catch (err) {
    next(err);
  }
}

// 5. removeGroupMember
async function removeGroupMember(req, res, next) {
  try {
    const { id, userId } = req.params;

    const result = await db.query(
      'DELETE FROM group_members WHERE group_id = $1 AND user_id = $2 RETURNING *',
      [id, userId]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Anggota tidak ditemukan di grup tersebut' });
    }

    res.status(200).json({
      message: 'Anggota berhasil dikeluarkan dari grup',
      removed: { group_id: parseInt(id), user_id: parseInt(userId) }
    });
  } catch (err) {
    next(err);
  }
}

// 6. getGroupEvents
async function getGroupEvents(req, res, next) {
  try {
    const { id } = req.params;

    const groupCheck = await db.query('SELECT group_name FROM groups WHERE group_id = $1', [id]);
    if (groupCheck.rows.length === 0) {
      return res.status(404).json({ error: `Grup dengan ID ${id} tidak ditemukan` });
    }

    const eventsRes = await db.query(`
      SELECT e.event_id, e.title, e.description, e.start_time, e.end_time,
             u.name AS author_name
      FROM events e
      JOIN users u ON e.user_id = u.user_id
      WHERE e.group_id = $1
      ORDER BY e.start_time ASC
    `, [id]);

    res.status(200).json({
      message: `Berhasil mengambil daftar jadwal untuk grup ${groupCheck.rows[0].group_name}`,
      total: eventsRes.rows.length,
      data: eventsRes.rows
    });
  } catch (err) {
    next(err);
  }
}

module.exports = {
  getAllGroups,
  getGroupById,
  createGroup,
  addGroupMember,
  removeGroupMember,
  getGroupEvents
};
