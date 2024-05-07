const express = require("express");
const cors = require("cors");
const getStrategyText = require("./strategy-guide/getStrategyText");
const getFormattedSummary = require("./strategy-guide/getFormattedSummary");
const iconv = require("iconv-lite");

const app = express();

// Serve static files from the "public" directory
app.use(express.static("public"));

// Enable CORS for all routes
app.use(cors());

// API endpoint to fetch instance strategy text
app.get("/api/strategy-text", async (req, res) => {
  try {
    const instanceName = normalizeEncoding(req.query.instanceName);
    const { strategyText } = await getStrategyText(instanceName);

    res.json({ strategyText });
    console.log(strategyText);
  } catch (error) {
    console.error("Error fetching strategy text:", error);
    res.status(500).json({ error: "Failed to fetch strategy text" });
  }
});

// API endpoint to get summary
app.get("/api/summary", async (req, res) => {
  try {
    const strategyText = normalizeEncoding(req.query.strategyText);
    const { summary } = await getFormattedSummary(strategyText, instanceName);

    res.json({ summary });
  } catch (error) {
    console.error("Error getting summary:", error);
    res.status(500).json({ error: "Failed to get summary" });
  }
});

// API endpoint to fetch instance strategy (combines strategy text and summary)
app.get("/api/instance-strategy", async (req, res) => {
  try {
    const instanceName = normalizeEncoding(req.query.instanceName);
    const { strategyText } = await getStrategyText(instanceName);
    const { formattedSummary } = await getFormattedSummary(
      strategyText,
      instanceName,
    );

    res.json({ summary: formattedSummary });
  } catch (error) {
    console.error("Error fetching instance strategy:", error);
    res.status(500).json({ error: "Failed to fetch instance strategy" });
  }
});

// Helper function to normalize encoding
function normalizeEncoding(text) {
  return iconv.decode(iconv.encode(text, "UTF-8"), "UTF-8");
}

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, "0.0.0.0", () => {
  console.log(`Server is running on port ${port}`);
});
