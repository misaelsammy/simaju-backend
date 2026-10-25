const express = require('express');
const router = express.Router();
const eventController = require('../controllers/eventController');

// Resource Utama: Events (CRUD Lengkap)
router.get('/', eventController.getAllEvents);
router.get('/check-conflict', eventController.checkScheduleConflictEndpoint);
router.get('/:id', eventController.getEventById);
router.post('/', eventController.createEvent);
router.put('/:id', eventController.updateEvent);
router.delete('/:id', eventController.deleteEvent);

module.exports = router;
