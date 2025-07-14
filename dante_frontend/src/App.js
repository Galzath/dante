import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    // This is a placeholder for a real auth check.
    // In a real app, you'd check for a cookie or token.
    useEffect(() => {
        // For now, we'll just assume the user is not authenticated
        // until they are redirected back from the backend.
        // A simple way to check is to see if a certain cookie is set.
        if (document.cookie.includes('dante-auth')) {
            setIsAuthenticated(true);
        }
    }, []);

    return (
        <div className="App">
            {isAuthenticated ? <Dashboard /> : <Login />}
        </div>
    );
}

export default App;
