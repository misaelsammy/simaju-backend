const express = require('express');
const router = express.Router();
const reminderController = require('../controllers/reminderController');

// Daftar endpoint reminders
router.get('/', reminderController.getAllReminders);
router.post('/', reminderController.createReminder);
router.patch('/:id/sent', reminderController.markReminderAsSent);
router.delete('/:id', reminderController.deleteReminder);

module.exports = router;
