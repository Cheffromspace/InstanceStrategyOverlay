# FFXIV Instance Strategy Overlay

The FFXIV Instance Strategy Overlay is a tool that provides real-time strategy information for Final Fantasy XIV instances (trials, raids, and dungeons). It displays a concise summary of key mechanics and player actions for each phase of the encounter, allowing players to quickly reference the strategy without having to leave the game.

All strategy data is summarized by Anthropic's Claude 3(https://anthropic.com/claude). I have not checked the data for accuracy. If you find any errors, please let me know or open a pull request.

## Features

- Real-time display of instance strategy based on the current encounter
- Color-coded text for boss names, abilities, and mechanics
- Semi-transparent background for easy readability while in-game

## Prerequisites

Before running the project, ensure that you have the following installed:

- Node.js
- npm

## Installation

1. Clone the repository:
`git clone https://github.com/Cheffromspace/InstanceStrategyOverlay.git`

2. Navigate to the project directory:
   cd ffxiv-instance-strategy-overlay

3. Install the dependencies:
   npm install

## Usage

1. Start the server:
   npm start

2. Open the FFXIV game client.

3. Launch ACT (Advanced Combat Tracker) and ensure the OverlayPlugin is enabled.

4. In the OverlayPlugin settings, add a new overlay, using 'Custom' as the preset, and set the URL to the following:
   file://(absolute path to the parent installation folder)/ffxiv-instance-strategy-overlay/public/index.html

5. In the OverlayPlugin settings, add a new overlay, using 'Custom' as the preset, and set the URL as follows:

file:///[FULL_PATH_TO_PROJECT]/ffxiv-instance-strategy-overlay/public/index.html

Replace [FULL_PATH_TO_PROJECT] with the absolute path to the parent directory where you cloned the repository. For example, if you cloned the repository to C:\Projects\ffxiv-instance-strategy-overlay on Windows, the URL would be:

file:///C:/Projects/ffxiv-instance-strategy-overlay/public/index.html

5. Adjust the overlay size and position as desired.

6. Start an instance in FFXIV, and the strategy overlay will appear automatically when the encounter begins.

7. To enable strategy for unseen encounters, set an ANTHROPIC_API_KEY environment variable with a valid API key for the Anthropic Claude 3 API.

## Planned Features

- Remove the need for the local server and anthropic API key, store all strategy summaries locally.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
