const axios = require("axios");
const {
  summaryPrompt,
  cleanupScrapedTextPrompt,
} = require("../config/prompts.js");

async function callAnthropicAPI(systemPrompt, userMessage) {
  const apiUrl = "https://api.anthropic.com/v1/messages";
  const apiKey = process.env.ANTHROPIC_API_KEY;
  const payload = {
    model: "claude-3-opus-20240229",
    max_tokens: 1500,
    system: systemPrompt,
    temperature: 0.0,
    messages: [{ role: "user", content: userMessage }],
  };

  const anthropicResponse = await axios.post(apiUrl, payload, {
    headers: {
      "Content-Type": "application/json",
      "anthropic-version": "2023-06-01",
      "x-api-key": apiKey,
    },
  });

  return anthropicResponse.data.content[0].text;
}

async function generateSummary(strategyText) {
  const formattedSummary = await callAnthropicAPI(summaryPrompt, strategyText);
  return formattedSummary;
}

async function cleanScrapedText(scrapedText) {
  const formattedText = await callAnthropicAPI(
    cleanupScrapedTextPrompt,
    scrapedText,
  );
  return formattedText;
}

module.exports = {
  generateSummary,
  cleanScrapedText,
};
