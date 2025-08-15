import { useEffect, useState } from 'react'

export default function Home() {
    const [message, setMessage] = useState('')

    useEffect(() => {
        fetch('http://localhost:8000')
        .then((res) => res.json())
        .then((data) => setMessage(data.message))
        .catch((err) => console.error('Error:', err))
    }, [])

  return (
    <div className="home-page">
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <h1 className="text-3xl font-bold text-blue-600">{message || 'Loading...'}</h1>
        </div>
    </div>
  );
}