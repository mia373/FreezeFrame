import { defineConfig } from 'vite';
import path from 'path';
import fs from 'fs';

const COMMONTHREADS = path.resolve(__dirname, '..', 'commonthreads');

function precomputedAlias() {
  return {
    name: 'precomputed-alias',
    configureServer(server) {
      server.middlewares.use('/precomputed', (req, res, next) => {
        const filePath = path.join(COMMONTHREADS, req.url);
        if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
          const ext = path.extname(filePath).toLowerCase();
          const types = { '.json': 'application/json', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png' };
          res.setHeader('Content-Type', types[ext] || 'application/octet-stream');
          fs.createReadStream(filePath).pipe(res);
        } else {
          next();
        }
      });
    },
  };
}

export default defineConfig({
  plugins: [precomputedAlias()],
  server: {
    port: 5173,
    open: true,
    fs: {
      allow: [path.resolve(__dirname, '..')],
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
