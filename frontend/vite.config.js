import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/register": "http://127.0.0.1:8000",
      "/login": "http://127.0.0.1:8000",
      "/me": "http://127.0.0.1:8000",
      "/projects": "http://127.0.0.1:8000",
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
});
