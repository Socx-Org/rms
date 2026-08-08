import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    // Makes apps/web/src/lib/api.js's relative '/api/v1' fallback actually
    // work in local dev -- no path rewriting (matches the platform's own
    // rule, reference/nginx: CS-INF-010 recorded a real outage from exactly
    // that), so the API sees the same paths it does in production.
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
  preview: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    allowedHosts: ['rms.socx.org.uk', 'socx.org.uk', 'localhost', '127.0.0.1'],
  },
});
