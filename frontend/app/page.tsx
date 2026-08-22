'use client'

import { useMemo, useRef, useState } from 'react'
import {
  ArrowUp,
  Check,
  ChevronDown,
  ChevronRight,
  FileText,
  FolderOpen,
  Headphones,
  Laptop,
  Menu,
  MessageSquare,
  Mic,
  Moon,
  Paperclip,
  Search,
  Send,
  Settings,
  Sparkles,
  SquarePen,
  Sun,
  User,
  X,
} from 'lucide-react'
import { SettingsView } from './settings-view'

 type Message = { role: 'user' | 'assistant'; content: string }
 type Chat = { id: number; title: string; time: string; messages: Message[] }
 const RAG_LOGO = 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/rag%20logo-it6z8xhpX54Vo7RZuKijIEgMupspwO.avif'
 const initialChats: Chat[] = [
  { id: 1, title: 'Welcome to RAG', time: 'Just now', messages: [{ role: 'user', content: 'What can you help me with?' }, { role: 'assistant', content: "I'm RAG, your retrieval-augmented AI companion. I can help you brainstorm, write, learn, analyze information, and turn rough thoughts into clear next steps." }] },
  { id: 2, title: 'Plan a product launch', time: 'Yesterday', messages: [{ role: 'user', content: 'Help me plan a product launch.' }] },
  { id: 3, title: 'Explain quantum computing', time: 'Yesterday', messages: [{ role: 'user', content: 'Explain quantum computing simply.' }] },
  { id: 4, title: 'Write a birthday message', time: 'Jun 12', messages: [{ role: 'user', content: 'Write a warm birthday message.' }] },
 ]
 const suggestions = [{ icon: Sparkles, title: 'Brainstorm ideas', prompt: 'Help me brainstorm ideas for a new project.' }, { icon: FileText, title: 'Write something', prompt: 'Help me write a clear and engaging introduction.' }, { icon: Headphones, title: 'Learn a topic', prompt: 'Teach me something interesting in a simple way.' }, { icon: FolderOpen, title: 'Analyze files', prompt: 'How should I organize and analyze a project file?' }]

 export default function Page() {
  const [userName, setUserName] = useState('Admin')
  const [chats, setChats] = useState(initialChats), [activeId, setActiveId] = useState(1), [draft, setDraft] = useState(''), [isTyping, setIsTyping] = useState(false), [sidebarOpen, setSidebarOpen] = useState(false), [listening, setListening] = useState(false), [darkMode, setDarkMode] = useState(false), [profileOpen, setProfileOpen] = useState(false), [settingsOpen, setSettingsOpen] = useState(false)
  const fileRef = useRef<HTMLInputElement>(null)
  const activeChat = useMemo(() => chats.find((chat) => chat.id === activeId) ?? chats[0], [activeId, chats])
  function logout() { setSettingsOpen(false); setProfileOpen(false) }
  function newChat() { const next = { id: Date.now(), title: 'New conversation', time: 'Just now', messages: [] }; setChats((current) => [next, ...current]); setActiveId(next.id); setProfileOpen(false); setSettingsOpen(false); setSidebarOpen(false) }
  async function sendMessage(text = draft) {
  const clean = text.trim()

  if (!clean || isTyping) return

  const nextTitle =
    clean.length > 28 ? `${clean.slice(0, 28)}…` : clean

  setDraft('')

  // Add user's message immediately
  setChats((current) =>
    current.map((chat) =>
      chat.id === activeId
        ? {
            ...chat,
            title: chat.messages.length
              ? chat.title
              : nextTitle,
            messages: [
              ...chat.messages,
              {
                role: 'user',
                content: clean,
              },
            ],
          }
        : chat
    )
  )

  setIsTyping(true)

  try {
    const response = await fetch(
  `/api/chat`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: clean,
        }),
      }
    )

    const data = await response.json()

    if (!response.ok || !data.success) {
      throw new Error(
        data.error || 'Failed to get response from RAG API'
      )
    }

    setChats((current) =>
      current.map((chat) =>
        chat.id === activeId
          ? {
              ...chat,
              messages: [
                ...chat.messages,
                {
                  role: 'assistant',
                  content: data.response,
                },
              ],
            }
          : chat
      )
    )
  } catch (error) {
    console.error('RAG API error:', error)

    setChats((current) =>
      current.map((chat) =>
        chat.id === activeId
          ? {
              ...chat,
              messages: [
                ...chat.messages,
                {
                  role: 'assistant',
                  content:
                    'Sorry, I could not connect to the RAG backend. Please make sure the Flask server is running on port 5000.',
                },
              ],
            }
          : chat
      )
    )
  } finally {
    setIsTyping(false)
  }
}
  function toggleMic() { const Recognition = (window as Window & { SpeechRecognition?: any; webkitSpeechRecognition?: any }).SpeechRecognition || (window as Window & { webkitSpeechRecognition?: any }).webkitSpeechRecognition; if (!Recognition) { setDraft((current) => current || 'Tell me about '); return } const recognition = new Recognition(); recognition.lang = 'en-US'; recognition.onresult = (event: any) => setDraft((current) => `${current} ${event.results[0][0].transcript}`.trim()); recognition.onend = () => setListening(false); setListening(true); recognition.start() }
  return <main className={`app-shell ${darkMode ? 'theme-dark' : 'theme-light'}`}><div className="mobile-backdrop" data-open={sidebarOpen} onClick={() => setSidebarOpen(false)} /><aside className="sidebar" data-open={sidebarOpen}><div className="sidebar-top"><div className="brand-lockup"><img className="brand-logo" src={RAG_LOGO} alt="RAG logo" /><span>RAG</span></div><button className="icon-button mobile-close" onClick={() => setSidebarOpen(false)} aria-label="Close sidebar"><X size={18} /></button></div><button className="new-chat-button" onClick={newChat}><SquarePen size={16} />New conversation <span>⌘ K</span></button><div className="history-label"><span>RECENT</span><button className="icon-button" aria-label="Search history"><Search size={15} /></button></div><nav className="history-list" aria-label="Conversation history">{chats.map((chat) => <button key={chat.id} className="history-item" data-active={chat.id === activeId} onClick={() => { setActiveId(chat.id); setSidebarOpen(false); setSettingsOpen(false) }}><MessageSquare size={15} /><span>{chat.title}</span><small>{chat.time}</small></button>)}</nav><div className="sidebar-bottom"><button className="sidebar-link"><Sparkles size={16} />Explore prompts</button><button className="sidebar-link" onClick={() => { setSettingsOpen(true); setProfileOpen(false); setSidebarOpen(false) }}><Settings size={16} />Settings</button><button className="profile" onClick={() => setProfileOpen(!profileOpen)}><div className="avatar">{(userName || 'AD').slice(0, 2).toUpperCase()}</div><div><strong>{userName || 'Admin'}</strong><span>Admin user</span></div><ChevronRight size={17} className="profile-more" /></button></div></aside><section className="chat-area"><header className="chat-header"><button className="icon-button menu-button" onClick={() => setSidebarOpen(true)} aria-label="Open sidebar"><Menu size={19} /></button><div className="model-select"><span className="status-dot" /><strong>RAG 2.0</strong><ChevronDown size={14} /></div><div className="header-actions"><button className="icon-button" onClick={() => setDarkMode((mode) => !mode)} aria-label="Toggle theme">{darkMode ? <Sun size={18} /> : <Moon size={18} />}</button><button className="icon-button" onClick={() => setSettingsOpen(true)} aria-label="Open settings"><Settings size={18} /></button></div></header>{settingsOpen ? <SettingsView userName={userName} email={""} chatTitles={chats.map((chat) => chat.title)} onBack={() => setSettingsOpen(false)} onLogout={logout} /> : <><main className="conversation">{activeChat.messages.length === 0 ? <div className="empty-state"><img src={RAG_LOGO} alt="RAG logo" /><p className="eyebrow">RAG 2.0</p><h1>What&apos;s on your mind?</h1><p>Ask a question, start a project, or explore an idea.</p><div className="suggestion-grid">{suggestions.map(({ icon: Icon, title, prompt }) => <button key={title} className="suggestion-card" onClick={() => sendMessage(prompt)}><Icon size={17} /><span>{title}</span><ChevronRight size={15} /></button>)}</div></div> : <div className="message-stack">{activeChat.messages.map((message, index) => <article key={`${message.role}-${index}`} className={`message ${message.role}`}><div className="message-avatar">{message.role === 'assistant' ? <img src={RAG_LOGO} alt="RAG" /> : <User size={16} />}</div><div><p className="message-role">{message.role === 'assistant' ? 'RAG' : userName || 'You'}</p><p className="message-copy">{message.content}</p></div></article>)}{isTyping && <article className="message assistant"><div className="message-avatar"><img src={RAG_LOGO} alt="RAG" /></div><div><p className="message-role">RAG</p><p className="typing-dots">● ● ●</p></div></article>}</div>}</main><div className="composer-wrap"><div className="composer"><textarea value={draft} onChange={(event) => setDraft(event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter' && !event.shiftKey && !event.nativeEvent.isComposing && event.keyCode !== 229) { event.preventDefault(); sendMessage() } }} placeholder="Message RAG" rows={1} aria-label="Message RAG" /><div className="composer-actions"><input ref={fileRef} type="file" hidden /><button className="icon-button" onClick={() => fileRef.current?.click()} aria-label="Attach file"><Paperclip size={18} /></button><button className={`icon-button ${listening ? 'is-active' : ''}`} onClick={toggleMic} aria-label="Use microphone"><Mic size={18} /></button><button className="send-button" onClick={() => sendMessage()} aria-label="Send message"><Send size={16} /></button></div></div><p className="composer-note">RAG can make mistakes. Check important information.</p></div></>}</section></main>
 }
