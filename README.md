# Responsive AI

Responsive Next.js app that leverages [Open AI GPT](https://github.com/openai/gpt-3) to provide rich interactions with users.

## Local run

### Prerequisites

1. You must have an `OPENAI_API_KEY` provided by https://openai.com/api/
2. Create a `.env` file in the `/server` folder with `OPENAI_API_KEY=<YOUR KEY>`
3. Install packages with `npm i` in both `/client` and `/server` folders

### Run application

1. Open two terminals, one for `/client` and one for `/server`
2. `npm run dev` in both directories (client will automatically open a new window)
