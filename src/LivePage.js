import React, { useEffect, useRef } from 'react';
import io from 'socket.io-client';

const LivePage = () => {
  const socketRef = useRef(null);

  useEffect(() => {
    // Establish the WebSocket connection
    socketRef.current = io('http://localhost:5000');

    // Send the "hello" message every minute
    const interval = setInterval(() => {
      socketRef.current.emit('message', {'hello':'1'});
    }, 5000);

    socketRef.current.on('response', (data) => {
        console.log('Received response:', data);
        // Handle the response data as needed
      });

    // Clean up the interval and close the WebSocket connection on component unmount
    return () => {
      clearInterval(interval);
      socketRef.current.close();
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="App-title">WebSocket Example</h1>
      </header>
      <div className="App-content">
        <p>Sending "hello" message every minute...</p>
      </div>
      <footer className="App-footer">
        <p>WebSocket connection is open</p>
      </footer>
    </div>
  );
};

export default LivePage;
