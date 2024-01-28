# Responsive AI

Responsive AI app that leverages [OpenAI GPT](https://github.com/openai/gpt-3) to provide rich interactions with users.

## Problem

This used to be a Next.js app that connected to OpenAI's GPT API and offered users access to ChatGPT without having to register. However, since OpenAI added an expiration on my API key, the only way to further access their API is by signing up for the paid version 🙄.

## Architecture and Design

There are still ways to provide users an equivalent or even greater utility given that there are so many [LLM (large language model)](https://en.wikipedia.org/wiki/Large_language_model) options available now. There are several variations and approaches I will experiment with around the core functionality of having a responsive AI agent.

We want to create a responsive AI agent or app that:

1. Takes real-time speech and converts to text
   - We'll need to find a way to have the service listen to inputs from a microphone. Later we may expand to audio files, etc.
   - Speech-to-text or vice versa is one of the most common [NLP (natural language processing)](https://en.wikipedia.org/wiki/Natural_language_processing) tasks, we can leverage Python and various NLP libraries to create a speech-to-text service
2. Sends text to a service that communicates with an LLM (could be ChatGPT)
   - This part is just researching which LLM is most suitable for use and building around that. It should be a free model or service and easy to use
3. Takes response from LLM and converts back to speech in real-time
   - Similar to Part 1 above but in reverse (text-to-speech), there should be some libraries we could use for that

_Q: Paid versions of OpenAI's ChatGPT already has support for speech recognition so why reinvent the wheel?_

The catch is you have to pay and it takes the fun out of building our own custom solution which could extend to more functionalities native to your desktop or mobile device. More importantly, we want to build out the solution using as many free and open source resources as possible so that it is as accessible to as many people as possible which was [OpenAI's original mission they have since steered away from](https://www.lunasec.io/docs/blog/openai-not-so-open/).
