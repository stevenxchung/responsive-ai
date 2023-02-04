/** @type {import('next').NextConfig} */
const baseUrl = process.env.NEXT_PUBLIC_SERVER_URL || 'http://localhost:3000'

const nextConfig = {
  reactStrictMode: true,
  // Reference: https://frontend-digest.com/environment-variables-in-next-js-9a272f0bf655
  env: {
    SERVER_URL: baseUrl,
    OPENAI_API_KEY: process.env.OPENAI_API_KEY,
  },
  async rewrites() {
    return [
      {
        source: '/api/gpt-ai',
        destination: `${baseUrl}/api/gpt-ai`,
      },
    ]
  },
}

module.exports = nextConfig
