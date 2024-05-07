const axios = require("axios");
const fs = require("fs").promises;
const path = require("path");
const { anthropicApis } = require("./anthropicApis");
const { generateSummary } = require("./anthropicApis");

async function getFormattedSummary(strategyText, instanceName) {
  const filePath = path.join(__dirname, "summaries", `${instanceName}.txt`);

  try {
    console.log("Checking for cached summary");
    // Check if the summary file already exists
    await fs.access(filePath);
    // If the file exists, read its contents and return
    const formattedSummary = await fs.readFile(filePath, "utf8");
    console.log("formattedSummary", formattedSummary);
    console.log("Using cached summary");
    return { formattedSummary };
  } catch (error) {
    const summaryText = await generateSummary(strategyText);
    const formattedSummary = summaryText.replace(/\n/g, "<br>");
    //   .replace(/- /g, "<li>");
    // Save the formatted summary to a file
    await fs.mkdir(path.join(__dirname, "summaries"), { recursive: true });
    await fs.writeFile(filePath, formattedSummary, "utf8");

    return { formattedSummary };
  }
}

module.exports = getFormattedSummary;
