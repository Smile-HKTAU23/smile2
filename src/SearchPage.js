import React, { useState, useEffect } from 'react';
import './SearchPage.css';
import AutocompleteAddressInput from './AutocompleteAddressInput';
import { useNavigate } from 'react-router-dom';

const SearchPage = () => {
  const [destination, setDestination] = useState('');
  const [clientLocation, setClientLocation] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    // Get the client's GPS location
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        setClientLocation({ latitude, longitude });
      },
      (error) => {
        console.error('Error getting client location:', error);
      }
    );
  }, []);

  const handleSearch = () => {
    const url = `/get_options?dest_lat=${destination.latitude}&dest_lng=${destination.longitude}&source_lat=${clientLocation.latitude}&source_lng=${clientLocation.longitude}`;
        
    fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response from the backend if needed
        navigate('/results', { state: data  });
      })
      .catch((error) => {
        // Handle any errors
        console.error(error);
      });      
      
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="App-title">Search for a Ride</h1>
      </header>
      <div className="App-content">
        <h2>Enter your destination:</h2>
        <AutocompleteAddressInput onSelect={(location) => setDestination(location)} />
        <button className="search-button" onClick={handleSearch}>
          Search
        </button>
      </div>
      <footer className="App-footer">
        <p>Enjoy convenient and reliable rides at your fingertips.</p>
      </footer>
    </div>
  );
};

export default SearchPage;
