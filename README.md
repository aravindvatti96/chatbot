# Gen Project - AI Co-Founder Chatbot

## Overview
The AI Co-Founder Chatbot is a web application designed to assist startup founders by providing expert feedback on their startup ideas, evaluating pitches, and offering motivational advice. The application leverages a generative AI model to deliver insights from various expert roles, including Product Manager, Investor, Growth Hacker, Technical Advisor, and Marketing Expert.

## Features
- **Role Analysis**: Get feedback on your startup idea from different expert perspectives.
- **Idea Builder**: Structure your startup idea and receive a comprehensive analysis.
- **Pitch Judge**: Submit your pitch for evaluation and receive a score along with detailed feedback.
- **Motivation**: Share your challenges and receive motivational advice and success stories.

## Requirements
- Python 3.x
- Gradio
- Google Generative AI SDK
- dotenv

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd Gen-project
   ```

2. Create a `.env` file in the project root directory and add your API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your web browser and navigate to `http://localhost:7861` (or the port displayed in the console) to access the chatbot.

## Usage
- Select an expert role to analyze your startup idea.
- Fill in the structured fields to build a comprehensive analysis.
- Submit your pitch for feedback.
- Share your challenges for motivational advice.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.