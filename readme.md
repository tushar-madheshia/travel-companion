
# Travel Companion AI Assistant

This repository contains the source code for a travel assistant named **EMA** (Enhanced Multi-modal Assistant). EMA is designed to assist users with travel-related queries, including finding flights, hotels, and activities, as well as providing travel tips and recommendations. The assistant uses OpenAI's GPT-4o model and integrates with Amadeus APIs for real-time travel data.

---

## Features

- **Flight Search**: Search for flights based on origin, destination, travel class, and other parameters.
- **Hotel Search**: Find hotels based on city, amenities, and star ratings.
- **Activity Recommendations**: Suggest activities in a city or country based on user preferences.
- **Real-time Interaction**: Supports real-time voice and text-based interaction.
- **Visual Interface**: Displays a dynamic visual interface for user interaction.
- **Guardrails**: Ensures relevance and proper handling of user queries.

---

## Project Structure

```
companian/
├── ai/
│   ├── agents/                # AI agents for flights, hotels, and activities
│   ├── guardrail/             # Guardrails for query validation
│   ├── models/                # Model loader for GPT-4o
├── assistant_modules/         # Modules for audio, microphone, and visual interface
├── config.py                  # Configuration settings
├── enums.py                   # Enum definitions for statuses and types
├── runner.py                  # Main entry point for the assistant
├── requirements.txt           # Python dependencies
├── .env                       # Environment variable template
└── readme.md                  # Documentation
```

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repo/travel-companion.git
   cd travel-companion
   ```
2. **Set Up Environment**:

   - Add your API keys for OpenAI and Amadeus in the .env file:
     ```
     OPENAI_API_KEY=your_openai_api_key
     AMADEUS_API_KEY=your_amadeus_api_key
     AMADEUS_API_SECRET=your_amadeus_api_secret
     ```
3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Install Playwright (Optional)**:
   If using browser-based tools:

   ```bash
   playwright install
   ```

---

## Usage

1. **Run the Assistant**:

   ```bash
   python runner.py
   ```
2. **Interact with EMA**:

   - Speak or type queries such as:
     - "Find me a flight from New York to Los Angeles on 2025-05-01."
     - "Suggest activities in Paris for a family with kids."
     - "I want to book a hotel in Bengaluru with a swimming pool and at least a 4-star rating."
3. **Visual Interface**:

   - A dynamic visual interface will display the assistant's responses and audio visualization.

---

## Key Components

### 1. **Agents**

- **Amadeus Flight Agent**: Handles flight-related queries.
- **Amadeus Hotel Agent**: Handles hotel-related queries.
- **Amadeus Activities Agent**: Handles activity-related queries.

### 2. **Modules**

- **Audio**: Handles audio playback.
- **Microphone**: Captures user input via microphone.
- **Visual Interface**: Displays a graphical interface for interaction.

### 3. **Guardrails**

- Ensures the assistant only responds to travel-related queries.
- Provides fallback responses for irrelevant or unsupported queries.

---

## Configuration

- **Session Instructions**: Defined in `config.py` to guide the assistant's behavior.
- **API Integration**: Uses Amadeus APIs for real-time travel data.

---

## Logs

- **Runtime Logs**: Stored in `runtime_time_table.jsonl` for performance monitoring.
- **WebSocket Events**: Logs incoming and outgoing WebSocket messages.

---

## Dependencies

- Python 3.8+
- Key Libraries:
  - `websockets`
  - `langchain`
  - `pygame`
  - `pyaudio`
  - `numpy`
  - `python-dotenv`

---

## Environment Variables

- **OPENAI_API_KEY**: API key for OpenAI GPT-4o.
- **AMADEUS_API_KEY**: API key for Amadeus.
- **AMADEUS_API_SECRET**: API secret for Amadeus.

---

## Known Issues

- Ensure the `.env` file is properly configured with valid API keys.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [OpenAI](https://openai.com) for GPT-4o.
- [Amadeus](https://developers.amadeus.com) for travel APIs.
- [LangChain](https://langchain.com) for agent orchestration.

```

```
