# FaceCheck ID Scraper README

## Overview

The FaceCheck ID Scraper is a Python-based tool that utilizes Selenium for web scraping and bypasses captchas using a VPN. The tool is designed to upload an image to the FaceCheck ID website, handle captchas, and extract URLs where the image appears. Additionally, it includes a REST API using Flask and a Telegram bot for easy interaction.

## Features

- Bypass captchas using a VPN (accuracy of bypass is approximately 50%).
- Upload images to the FaceCheck ID website.
- Extract URLs of sites where the image appears.
- REST API for uploading images and retrieving results.
- Telegram bot for easy interaction and image processing.

## Setup

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver
- VPN extension (`VPN-extension.crx`)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/adilsameer/Facecheck_scraper_vpn.git
   cd Facecheck_scraper_vpn
   ```

2. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add VPN Extension**
   Place the VPN extension (`VPN-extension.crx`) in the project directory.

4. **Setup Environment Variables**
   Set up the Telegram bot token as an environment variable.
   ```bash
   export TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   ```

## Usage

### Running the Scraper

To run the scraper, execute the following script:

```python
from scraper import Scraper

image_path = r"absolute_path_to_your_image.jpg"
scraper = Scraper()
scraper.main(image_path)
```

### REST API

#### Starting the Flask Server

```bash
python api.py
```

#### API Endpoints

1. **Upload Image**
   - **Endpoint**: `/upload`
   - **Method**: POST
   - **Description**: Uploads an image and starts the scraping process.
   - **Parameters**: Form-data with key `image` (file)

   Example:
   ```bash
   curl -X POST -F "image=@absolute_path_to_your_image.jpg" http://127.0.0.1:5000/upload
   ```

2. **Get Results**
   - **Endpoint**: `/results/<image_id>`
   - **Method**: GET
   - **Description**: Retrieves URLs where the image appears.
   - **Parameters**: `image_id` (string)

   Example:
   ```bash
   curl http://127.0.0.1:5000/results/your_image_id
   ```

### Telegram Bot

#### Starting the Telegram Bot

```bash
python bot.py
```

#### Commands

- **/start**: Initializes the bot and shows options.
- **🔍 Find Person from Image**: Prompts the user to upload an image.
- **🔗 APIs**: Provides information about available APIs.
- **ℹ️ Learn More**: Provides more information about the bot.

#### Uploading an Image

Send an image through the Telegram bot to start the scraping process. The bot will process the image and return URLs where the image appears.

## Captcha Handling

For scraping data, Selenium and a VPN are used to bypass captchas with an accuracy of approximately 50%. The tool attempts to handle captchas using a VPN by toggling it on and off. Captcha handling is challenging due to the website using a remote URL to verify captcha IDs, which cannot be reused.

Currently, OpenCV is being integrated to improve captcha-solving accuracy. This README will be updated once OpenCV implementation is completed.
