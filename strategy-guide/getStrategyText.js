const axios = require("axios");
const { JSDOM } = require("jsdom");
const fs = require("fs").promises;
const path = require("path");
const anthropicApis = require("./anthropicApis");

async function getStrategyText(instanceName) {
  const filePath = path.join(__dirname, "strategies", `${instanceName}.txt`);

  try {
    // Check if the strategy file already exists
    await fs.access(filePath);
    console.log("File exists");
    // If the file exists, read its contents and return
    const strategyText = await fs.readFile(filePath, "utf8");
    return { strategyText };
  } catch (error) {
    // If the file doesn't exist, fetch the strategy text from the web
    const encodedInstanceName = encodeURIComponent(instanceName);
    // const url = `https://ffxiv.consolegameswiki.com/wiki/${encodedInstanceName}`;
    const url = `https://ffxiv.gamerescape.com/wiki/${encodedInstanceName}#Dialogue`;
    console.log("Fetching from", url);

    const response = await axios.get(url, {
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    });

    const html = response.data;
    const dom = new JSDOM(html);
    const document = dom.window.document;
    const strategyElement = document.querySelector(".mw-parser-output");
    const rawStrategyText = strategyElement
      ? strategyElement.textContent
      : "Strategy not found";

    // const strategyText = await anthropicApis.cleanScrapedText(rawStrategyText);
    const strategyText = rawStrategyText;

    // Save the strategy text to a file
    await fs.mkdir(path.join(__dirname, "strategies"), { recursive: true });
    await fs.writeFile(filePath, strategyText, "utf8");

    return { strategyText };
  }
}

module.exports = getStrategyText;
