# Foster Care Policy Assistant - Frontend

A modern React chat interface for researchers to query foster care policies using the AI-powered backend API.

## Features

- **Modern Chat Interface**: Clean, responsive design with real-time message streaming
- **Research-Focused**: Designed specifically for foster care policy researchers
- **Real-time Streaming**: Messages stream in real-time from the AI assistant
- **Mobile Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- **Beautiful UI**: Modern gradient design with smooth animations and transitions

## Prerequisites

- Node.js (version 16 or higher)
- npm or yarn
- The FastAPI backend running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The application will open in your browser at `http://localhost:3000`.

## Usage

1. **Start the Backend**: Make sure your FastAPI backend is running on port 8000
2. **Open the Frontend**: Navigate to `http://localhost:3000` in your browser
3. **Ask Questions**: Type your foster care policy questions in the chat interface
4. **Get Responses**: The AI will search through state policies and provide relevant answers with sources

## Example Questions

- "What are the adoption requirements in California?"
- "How do Colorado and Texas differ in their foster care policies?"
- "What are the requirements for becoming a foster parent in New York?"
- "Show me policies related to sibling placement in foster care"

## Development

### Project Structure

```
frontend/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── App.js              # Main React component
│   ├── App.css             # Component styles
│   ├── index.js            # React entry point
│   └── index.css           # Global styles
├── package.json            # Dependencies and scripts
└── README.md              # This file
```

### Available Scripts

- `npm start`: Runs the app in development mode
- `npm build`: Builds the app for production
- `npm test`: Launches the test runner
- `npm eject`: Ejects from Create React App (not recommended)

### Key Features

- **Streaming Responses**: Uses the Fetch API with ReadableStream to handle real-time message streaming
- **Auto-scroll**: Messages automatically scroll to the bottom as new content arrives
- **Loading States**: Visual feedback during API calls
- **Error Handling**: Graceful error handling with user-friendly messages
- **Responsive Design**: Optimized for all screen sizes

## API Integration

The frontend communicates with the FastAPI backend at `/api/chat` endpoint:

- **Method**: POST
- **Content-Type**: application/json
- **Body**: `{ "user_message": "your question here" }`
- **Response**: Streaming text response

## Styling

The application uses:
- **CSS Grid & Flexbox**: For responsive layouts
- **CSS Custom Properties**: For consistent theming
- **Modern CSS Features**: Backdrop filters, gradients, and animations
- **Mobile-First Design**: Responsive breakpoints for all devices

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

1. **Backend Connection Issues**: Ensure the FastAPI server is running on port 8000
2. **CORS Errors**: The backend includes CORS middleware, but check if it's properly configured
3. **Streaming Issues**: Some browsers may not support streaming responses - check browser compatibility

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the AI Makerspace Certification Challenge. 