# OKX Trading Bot

A Python-based trading bot for the OKX cryptocurrency exchange.

## Prerequisites

- Python 3.8 or higher
- Homebrew (for macOS users)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hungphambms/singapore-okx-bot.git
cd singapore-okx-bot
```

2. Install TA-Lib (Technical Analysis Library):

For macOS:
```bash
brew install ta-lib
```

For Ubuntu/Debian:
```bash
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
```

3. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your OKX API credentials and other configuration settings

## Running the Bot

1. Make sure your virtual environment is activated:
```bash
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

2. Start the bot:
```bash
python src/main.py
```

## Configuration

The bot can be configured through the following methods:
- Environment variables in `.env` file
- Command line arguments
- Configuration files in the `config` directory

## Features

- Real-time market data processing
- Technical analysis using TA-Lib
- Automated trading strategies
- Telegram and Discord notifications
- Performance monitoring

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## License

[Add your license information here]