function notFoundHandler(req, res, next) {
  res.status(404).json({
    error: `Endpoint ${req.method} ${req.originalUrl} tidak ditemukan`
  });
}

function errorHandler(err, req, res, next) {
  console.error('Unhandled Server Error:', err);
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    error: err.message || 'Terjadi kesalahan internal pada server'
  });
}

module.exports = {
  notFoundHandler,
  errorHandler
};
