import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { sendChatMessage } from "../services/api";
import "../styles/Chat.css";

function Chat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! 👋 I'm SchemeSetu AI. I can help you understand government schemes, eligibility, subsidies and application-related information.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();

    const question = input.trim();

    if (!question || loading) {
      return;
    }

    const userMessage = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendChatMessage(question);

      const aiResponse =
        data.response ||
        data.message ||
        data.answer ||
        data.reply ||
        data.content ||
        "I couldn't generate a response.";

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: aiResponse,
        },
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the AI service. Please make sure the backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestion = (question) => {
    setInput(question);
  };

  return (
    <div className="chat-page">

      {/* HEADER */}
      <header className="chat-header">
        <div className="chat-brand">

          <div className="chat-logo">
            SS
          </div>

          <div>
            <h1>SchemeSetu AI</h1>
            <p>Government Scheme Assistant</p>
          </div>

        </div>

        <div className="ai-status">
          <span className="status-dot"></span>
          AI Online
        </div>
      </header>


      {/* CHAT AREA */}
      <main className="chat-container">

        <div className="chat-welcome">

          <div className="welcome-icon">
            ✦
          </div>

          <h2>How can I help you?</h2>

          <p>
            Ask me about government schemes, eligibility,
            benefits and financial assistance.
          </p>

          <div className="suggestions">

            <button
              onClick={() =>
                handleSuggestion(
                  "Which government schemes are suitable for me?"
                )
              }
            >
              🔎 Find suitable schemes
            </button>

            <button
              onClick={() =>
                handleSuggestion(
                  "How does government subsidy work?"
                )
              }
            >
              💰 Understand subsidies
            </button>

            <button
              onClick={() =>
                handleSuggestion(
                  "What documents are generally required for schemes?"
                )
              }
            >
              📄 Required documents
            </button>

          </div>

        </div>


        {/* MESSAGES */}
        <div className="messages">

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message-row ${message.role}`}
            >

              {/* AI AVATAR */}
              {message.role === "assistant" && (
                <div className="message-avatar">
                  SS
                </div>
              )}


              {/* MESSAGE */}
              <div className="message-bubble">

                {message.role === "assistant" ? (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      a: ({ node, ...props }) => (
                        <a
                          {...props}
                          target="_blank"
                          rel="noopener noreferrer"
                        />
                      ),
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>
                ) : (
                  message.content
                )}

              </div>

            </div>
          ))}


          {/* TYPING */}
          {loading && (
            <div className="message-row assistant">

              <div className="message-avatar">
                SS
              </div>

              <div className="message-bubble typing">
                <span></span>
                <span></span>
                <span></span>
              </div>

            </div>
          )}

        </div>

      </main>


      {/* INPUT AREA */}
      <div className="chat-input-area">

        <form
          onSubmit={handleSend}
          className="chat-form"
        >

          <input
            type="text"
            placeholder="Ask SchemeSetu AI anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />

          <button
            type="submit"
            disabled={!input.trim() || loading}
          >
            ➤
          </button>

        </form>

        <p className="chat-disclaimer">
          SchemeSetu AI provides informational assistance.
          Always verify scheme details with the official source.
        </p>

      </div>

    </div>
  );
}

export default Chat;