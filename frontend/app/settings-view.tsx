'use client'

import { ChevronRight, LogOut, Trash2 } from 'lucide-react'

type SettingsViewProps = {
  userName: string
  email: string
  chatTitles: string[]
  onBack: () => void
  onLogout: () => void
}

export function SettingsView({ userName, email, chatTitles, onBack, onLogout }: SettingsViewProps) {
  return (
    <div className="settings-view">
      <div className="settings-heading-row">
        <button className="settings-back" onClick={onBack} aria-label="Back to chat">Back</button>
        <h1>Settings</h1>
      </div>
      <section className="settings-section" aria-labelledby="general-heading">
        <p className="settings-section-label" id="general-heading">General</p>
        <div className="settings-row"><span>Theme</span><span className="settings-value">Use app theme</span></div>
        <div className="settings-row"><span>Language</span><span className="settings-value">English <ChevronRight size={18} /></span></div>
      </section>
      <section className="settings-section" aria-labelledby="account-heading">
        <p className="settings-section-label" id="account-heading">Account</p>
        <div className="settings-row"><span>Name</span><span className="settings-value">{userName || 'Admin'}</span></div>
        <div className="settings-row"><span>Username</span><span className="settings-value">{userName ? userName.toLowerCase().replace(/\s+/g, '') : 'admin'} <ChevronRight size={18} /></span></div>
        <div className="settings-row"><span>Email</span><span className="settings-value">{email || 'Not provided'} <ChevronRight size={18} /></span></div>
        <div className="settings-row"><span>Delete account</span><button className="delete-account" type="button"><Trash2 size={16} />Delete</button></div>
      </section>
      <section className="settings-section" aria-labelledby="history-heading">
        <p className="settings-section-label" id="history-heading">Chat history</p>
        <div className="settings-history">{chatTitles.map((title) => <div className="settings-history-item" key={title}><span>{title}</span><ChevronRight size={17} /></div>)}</div>
      </section>
    </div>
  )
}
