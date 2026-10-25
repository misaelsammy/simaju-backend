const express = require('express');
const router = express.Router();
const groupController = require('../controllers/groupController');

// Daftar endpoint groups
router.get('/', groupController.getAllGroups);
router.get('/:id', groupController.getGroupById);
router.post('/', groupController.createGroup);
router.post('/:id/members', groupController.addGroupMember);
router.delete('/:id/members/:userId', groupController.removeGroupMember);
router.get('/:id/events', groupController.getGroupEvents);

module.exports = router;
