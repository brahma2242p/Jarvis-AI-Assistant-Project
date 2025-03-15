const {
  GoogleGenerativeAI,
  HarmCategory,
  HarmBlockThreshold,
} = require("@google/generative-ai");

const apiKey = process.env.GEMINI_API_KEY;
const genAI = new GoogleGenerativeAI(apiKey);

const model = genAI.getGenerativeModel({
  model: "gemini-1.5-flash",
});

const generationConfig = {
  temperature: 1,
  topP: 0.95,
  topK: 40,
  maxOutputTokens: 8192,
  responseMimeType: "text/plain",
};

// Speech Recognition Setup
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;

const speakButton = document.getElementById("speakButton");
const responseBox = document.getElementById("responseBox");

speakButton.addEventListener("click", () => {
  recognition.start();
  speakButton.innerText = "Listening...";
});

recognition.onresult = async (event) => {
  const transcript = event.results[0][0].transcript;
  speakButton.innerText = "Click here to speak";
  responseBox.innerText = "You said: " + transcript;
  
  // Send input to Gemini API
  try {
      const result = await model.generateContent({ prompt: transcript });
      const responseText = await result.response.text();
      responseBox.innerText += "\nJarvis: " + responseText;
  } catch (error) {
      responseBox.innerText += "\nError: " + error.message;
  }
};

recognition.onerror = (event) => {
  speakButton.innerText = "Click here to speak";
  responseBox.innerText = "Error: " + event.error;
};
