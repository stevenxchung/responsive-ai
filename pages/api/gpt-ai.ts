// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import { Configuration, OpenAIApi } from "openai";
import { ChatCompletionRequestMessage } from "openai/api";

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});

const openAI = new OpenAIApi(configuration);

type OpenAIResponse = {
  gptAI: string;
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<OpenAIResponse>
) {
  try {
    const chatGPTRequestMessage: ChatCompletionRequestMessage =
      req.body.chatGPTRequestMessage;
    const response = await openAI.createChatCompletion({
      model: "gpt-3.5-turbo",
      messages: [chatGPTRequestMessage],
    });
    res.status(200).json({
      gptAI: response.data.choices[0].message!.content,
    });
  } catch (error: any) {
    console.error(error);
    res.status(500).send(error || "My apologies, something went wrong!");
  }
}
