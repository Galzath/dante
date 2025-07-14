import React from 'react';
import axios from 'axios';

const CategoryCard = ({ category, count, onMarkAsRead }) => {
    const handleMarkAsRead = () => {
        axios.post('http://localhost:8000/mark-as-read', { category })
            .then(response => {
                console.log(response.data);
                // Immediately update the UI after successful request
                if (onMarkAsRead) {
                    onMarkAsRead(category);
                }
            })
            .catch(error => {
                console.error('There was an error marking the emails as read!', error);
                alert('Failed to mark emails as read. Please try again.');
            });
    };

    return (
        <div style={{ border: '1px solid #ccc', padding: '16px', margin: '16px', borderRadius: '8px', minWidth: '200px' }}>
            <h2>{category}</h2>
            <p>Unread: {count}</p>
            {count > 0 && <button onClick={handleMarkAsRead}>Mark as Read</button>}
        </div>
    );
};

export default CategoryCard;
