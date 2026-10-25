const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

// Daftar endpoint user
router.get('/', userController.getAllUsers);
router.post('/register', userController.registerUser);
router.post('/login', userController.loginUser);
router.get('/:id', userController.getUserProfile);
router.put('/:id', userController.updateUserProfile);

module.exports = router;
