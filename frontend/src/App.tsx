import { useState } from 'react'
import Chat from './components/Chat'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-900">Rag Cosense</h1>
        </div>
      </header>
      <main className="max-w-5xl mx-auto px-4 py-8">
        <Chat />
      </main>
    </div>
  )
}

export default App
