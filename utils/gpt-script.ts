import {
  ChatCompletionRequestMessage,
  ChatCompletionRequestMessageRoleEnum,
} from "openai/api";

let loadInterval: NodeJS.Timer;
const AI_SYSTEM_KEYWORD = "you are";

export function loader(e: Element) {
  e.textContent = "";
  loadInterval = setInterval(() => {
    e.textContent += ".";

    if (e.textContent === "....") {
      e.textContent = "";
    }
  }, 300);
}

export function typeText(e: Element, text: string) {
  let index = 0;
  let interval = setInterval(() => {
    if (index < text.length) {
      // Scroll to bottom
      e.scrollIntoView({ behavior: "smooth" });
      e.innerHTML += text.charAt(index);
      index++;
    } else {
      clearInterval(interval);
    }
  }, 10);
}

export function generateUniqueId(): string {
  const timestamp = Date.now();
  const randomNumber = Math.random();
  const hexadecimalString = randomNumber.toString(16);

  return `id-${timestamp}-${hexadecimalString}`;
}

export function chatStripe(isAi: boolean, value: string, uniqueId?: string) {
  return `
        <div class="wrapper ${isAi && "ai"}">
            <div class="chat">
                <div class="profile">
                    <img 
                      src="${isAi ? "assets/ai.png" : "assets/human.png"}"
                      alt="${isAi ? "bot" : "user"}" 
                    />
                </div>
                <div class="message" id=${uniqueId}>${value}</div>
            </div>
        </div>
    `;
}

export const handleSubmit = async (event: any) => {
  const form: HTMLFormElement = document.querySelector(".form")!;
  const chatContainer = document.querySelector(".chat_container");

  event.preventDefault();

  // User
  const data = new FormData(form);
  const content = data.get("prompt")!.toString();
  chatContainer!.innerHTML += chatStripe(false, content);
  form.reset();

  // AI
  const uniqueId = generateUniqueId();
  chatContainer!.innerHTML += chatStripe(true, " ", uniqueId);
  chatContainer!.scrollTop = chatContainer!.scrollHeight;

  const messageDiv = document.getElementById(uniqueId)!;
  loader(messageDiv);

  let chatGPTRequestMessage: ChatCompletionRequestMessage = {
    role: content.toLowerCase().includes(AI_SYSTEM_KEYWORD)
      ? ChatCompletionRequestMessageRoleEnum.System
      : ChatCompletionRequestMessageRoleEnum.User,
    content,
  };

  // API integration
  const response = await fetch(`${process.env.SERVER_URL!}/api/gpt-ai`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      chatGPTRequestMessage,
    }),
  });

  clearInterval(loadInterval);
  messageDiv.innerHTML = " ";

  if (response.ok) {
    // Response valid
    const data = await response.json();
    const parsedData = data.gptAI.trim(); // trims any trailing spaces/'\n'
    typeText(messageDiv, parsedData);
  } else {
    // Otherwise, error occurred
    const err = await response.text();
    messageDiv.innerHTML = "My apologies, something went wrong!";
    // alert(err);
  }
};
