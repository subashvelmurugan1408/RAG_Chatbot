import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: 'Hello! 👋 I\'m your AI assistant. Ask me anything about your documents!',
      timestamp: new Date()
    }
  ]);
  
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking');
  const messagesEndRef = useRef(null);
  const messageIdRef = useRef(2);

  // Check API status on mount
  useEffect(() => {
    checkApiStatus();
  }, []);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const checkApiStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/health');
      if (response.ok) {
        setApiStatus('connected');
      } else {
        setApiStatus('error');
      }
    } catch (error) {
      setApiStatus('error');
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    // Check API status
    if (apiStatus !== 'connected') {
      addMessage('bot', '❌ Error: Backend API is not connected. Make sure to run: python app.py');
      return;
    }

    // Add user message
    const userMessage = input;
    addMessage('user', userMessage);
    setInput('');
    setLoading(true);

    try {
      // Send to backend API
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        addMessage('bot', data.response);
      } else {
        addMessage('bot', `❌ Error: ${data.error}`);
      }
    } catch (error) {
      console.error('Error:', error);
      addMessage('bot', `❌ Error: ${error.message}. Make sure the backend is running on port 5000.`);
    } finally {
      setLoading(false);
    }
  };

  const addMessage = (type, content) => {
    const newMessage = {
      id: messageIdRef.current++,
      type: type,
      content: content,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const clearHistory = () => {
    setMessages([
      {
        id: 1,
        type: 'bot',
        content: 'Conversation cleared. How can I help you?',
        timestamp: new Date()
      }
    ]);
    messageIdRef.current = 2;
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="header-left">
            <h1>🤖 AI Assistant</h1>
            <span className={`status ${apiStatus}`}>
              {apiStatus === 'connected' ? '✓ Connected' : '⚠ Not Connected'}
            </span>
          </div>
          <button 
            className="clear-btn"
            onClick={clearHistory}
            title="Clear conversation"
          >
            🗑️ Clear
          </button>
        </div>
      </header>

      {/* Messages Container */}
      <div className="messages-container">
        <div className="messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`message message-${msg.type}`}>
              <div className="message-avatar">
                {msg.type === 'user' ? '👤' : '🤖'}
              </div>
              <div className="message-content">
                <p>{msg.content}</p>
                <span className="message-time">
                  {msg.timestamp.toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </span>
              </div>
            </div>
          ))}

          {loading && (
            <div className="message message-bot">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Form */}
      <form className="input-form" onSubmit={handleSendMessage}>
        <div className="input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything..."
            disabled={loading || apiStatus !== 'connected'}
            className="input-field"
            autoFocus
          />
          <button
            type="submit"
            disabled={loading || !input.trim() || apiStatus !== 'connected'}
            className="send-button"
            title="Send message"
          >
            {loading ? '⏳' : '➤'}
          </button>
        </div>
        <p className="help-text">
          Powered by Hugging Face API • Based on your documents
        </p>
      </form>
    </div>
  );
}

export default App;
