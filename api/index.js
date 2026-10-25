const express = require('express');
const cors = require('cors');
require('dotenv').config();

const userRoutes = require('../src/routes/userRoutes');
const eventRoutes = require('../src/routes/eventRoutes');
const groupRoutes = require('../src/routes/groupRoutes');
const reminderRoutes = require('../src/routes/reminderRoutes');
const { notFoundHandler, errorHandler } = require('../src/middlewares/errorHandler');

const app = express();

app.use(cors());
app.use(express.json());

// Root & Health Check Endpoint
app.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'SIMAJU (Sistem Informasi Manajemen Jadwal Terpadu) REST API is running successfully',
    version: '1.0.0',
    endpoints: {
      users: '/api/users',
      events: '/api/events',
      groups: '/api/groups',
      reminders: '/api/reminders'
    },
    timestamp: new Date().toISOString()
  });
});

// Mount Resource Routes
app.use('/api/users', userRoutes);
app.use('/api/events', eventRoutes);
app.use('/api/groups', groupRoutes);
app.use('/api/reminders', reminderRoutes);

// Error Handling Middlewares
app.use(notFoundHandler);
app.use(errorHandler);

const PORT = process.env.PORT || 3000;

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`SIMAJU REST API server is running on port ${PORT}`);
  });
}

module.exports = app;
