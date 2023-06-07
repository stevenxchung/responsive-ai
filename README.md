# Responsive AI

Responsive Next.js app that leverages [Open AI GPT](https://github.com/openai/gpt-3) to provide rich interactions with users.

## Local run

### Prerequisites

1. You must have an `OPENAI_API_KEY` provided by https://openai.com/api/
2. Create `.env.local` in the root project directory with variables from `.env.example`
3. Replace `<YOUR API KEY>` with your API key
4. Install packages with `npm i`

### Run application

1. In the `next.config.js` file, ensure the following is true:

```javascript
const baseUrl = process.env.NEXT_PUBLIC_SERVER_URL || "http://localhost:3000";
// const baseUrl = 'http://localhost:3000';
```

2. Run `npm run dev` (client will automatically open a new window)
