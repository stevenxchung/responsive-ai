/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Reference: https://frontend-digest.com/environment-variables-in-next-js-9a272f0bf655
  env: {
    SERVER_URL: process.env.NEXT_PUBLIC_SERVER_URL || 'http://localhost:5000/',
  },
}

module.exports = nextConfig
