#!/usr/bin/env node
// StratIQ AI Proxy — runs on Mac host, accepts requests from Docker container
// Docker can't reach api.anthropic.com (MDE blocks it), but Node on the host can.
// Usage: node aiproxy.js
// Listens on port 3001. Docker calls http://host.docker.internal:3001/proxy

const http = require('http');
const https = require('https');

const PORT = 3001;

const PROVIDER_ENDPOINTS = {
  anthropic: 'https://api.anthropic.com/v1/messages',
  openai: 'https://api.openai.com/v1/chat/completions',
  openrouter: 'https://openrouter.ai/api/v1/chat/completions',
};

const server = http.createServer((req, res) => {
  // CORS for localhost
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
  if (req.method !== 'POST' || req.url !== '/proxy') {
    res.writeHead(404); res.end('Not found'); return;
  }

  let body = '';
  req.on('data', chunk => body += chunk);
  req.on('end', () => {
    let parsed;
    try { parsed = JSON.parse(body); } catch(e) {
      res.writeHead(400); res.end(JSON.stringify({error: 'Invalid JSON'})); return;
    }

    const { provider, api_key, payload } = parsed;
    const url = new URL(provider === 'google'
      ? `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key=${api_key}`
      : PROVIDER_ENDPOINTS[provider] || PROVIDER_ENDPOINTS.anthropic);

    const bodyStr = JSON.stringify(payload);
    const headers = { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(bodyStr) };

    if (provider === 'anthropic') {
      headers['x-api-key'] = api_key;
      headers['anthropic-version'] = '2023-06-01';
    } else if (provider === 'openai' || provider === 'openrouter') {
      headers['Authorization'] = `Bearer ${api_key}`;
    }

    const options = { hostname: url.hostname, port: 443, path: url.pathname + url.search, method: 'POST', headers };

    const proxyReq = https.request(options, proxyRes => {
      let data = '';
      proxyRes.on('data', chunk => data += chunk);
      proxyRes.on('end', () => {
        res.writeHead(proxyRes.statusCode, { 'Content-Type': 'application/json' });
        res.end(data);
      });
    });

    proxyReq.on('error', err => {
      console.error('Proxy error:', err.message);
      res.writeHead(502); res.end(JSON.stringify({error: err.message}));
    });

    proxyReq.write(bodyStr);
    proxyReq.end();
  });
});

server.listen(PORT, () => console.log(`StratIQ AI Proxy running on port ${PORT}`));
