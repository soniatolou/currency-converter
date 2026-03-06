# Currency Converter

An object-oriented Python application for currency conversion. The program utilizes the Open Exchange Rates API to fetch real-time exchange rates and manage historical data.

## Features

- Real-time conversion between USD and over 160 currencies.
- Conversion between any currency pairs using USD as a base.
- Smart caching with a one-hour TTL to optimize API usage and performance.
- Fetch historical exchange rates for specific dates.
- Export current rate data to JSON files for external use.

## Installation and Usage

1. Clone the repository:
   git clone https://github.com/YOUR-USERNAME/currency-handler.git

2. Install dependencies:
   pip install -r requirements.txt

3. Create a .env file in the root directory and add your API key:
   APP_ID=your_api_key_here

4. Run the application:
   python main.py

## Code Structure

The project is divided into two files to separate logic from the user interface:

- currencyhandler.py: Handles API requests, calculations, and caching.
- main.py: Contains the application menu and handles user interaction.
