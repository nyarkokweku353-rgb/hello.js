
const express = require('express');
const dotenv = require('dotenv');
const path = require('path');

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Built-in JSON body parser
app.use(express.json());

// Custom request logging middleware
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
});

// Serve static files from /public (index.html will be served at GET /)
app.use(express.static(path.join(__dirname, 'public')));

// Root endpoint
app.get('/api', (req, res) => {
  res.send('My Week 2 API!');
});

// Create user
app.post('/user', (req, res) => {
  const { name, email } = req.body || {};
  if (!name || !email) {
    return res.status(400).json({ error: 'Name and email are required.' });
  }
  return res.status(201).send(`Hello, ${name}!`);
});

// Get user profile (placeholder)
app.get('/user/:id', (req, res) => {
  const { id } = req.params;
  res.send(`user(${id}) profile`);
});

// Generic 404 for unknown API routes
app.use((req, res, next) => {
  if (req.path.startsWith('/user') || req.path.startsWith('/api')) {
    return res.status(404).json({ error: 'Not Found' });
  }
  next();
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
