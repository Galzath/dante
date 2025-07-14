import React, { useState, useEffect } from 'react';
import CategoryCard from './CategoryCard';

const Dashboard = () => {
    const [categories, setCategories] = useState({});

    useEffect(() => {
        const eventSource = new EventSource("http://localhost:8000/dashboard-stream");

        eventSource.addEventListener('update', (event) => {
            const data = JSON.parse(event.data);
            setCategories(data);
        });

        eventSource.onerror = () => {
            // Handle errors, e.g., show a reconnecting message
            eventSource.close();
        };

        return () => {
            eventSource.close();
        };
    }, []);

    const handleMarkAsRead = (category) => {
        setCategories(prevCategories => ({
            ...prevCategories,
            [category]: 0
        }));
    };

    return (
        <div>
            <h1>Dashboard</h1>
            <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                {Object.keys(categories).length > 0 ? (
                    Object.entries(categories).map(([category, count]) => (
                        <CategoryCard
                            key={category}
                            category={category}
                            count={count}
                            onMarkAsRead={handleMarkAsRead}
                        />
                    ))
                ) : (
                    <p>No categories to display. Waiting for data...</p>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
