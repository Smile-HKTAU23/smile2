import React, { useEffect, useState,  useRef } from 'react';
import './Maps.css'
import { DirectionsRenderer, Marker, GoogleMap, DirectionsService } from '@react-google-maps/api';
import io from 'socket.io-client';
import { useLocation } from 'react-router-dom';

const Watch = () => {

    const [directions, setDirections] = useState(null);

    const parameters_location = useLocation();
    const card = parameters_location.state.card
    let pos = { lat: 32.069235, lng: 34.825947 };
    let pos2 = { lat: 32.069235, lng: 34.825947 };
    let driverPosition = {lat: 32.110820, lng:34.806710}
    
    let currentMap = null;
    const containerStyle = {
      width: '100%',
      height: '51rem'
    };

  const setDriversPosition = (newPos) => {
    driverPosition = newPos;
  }

  const setPos = (newPos) => {
    pos = newPos;
  }

  const setPos2 = (newPos) => {
    pos2 = newPos;
  }

  const options = {
    disableDefaultUI: true
  }

  const handleDirectionsService = (directionsService) => {
    if (directions == null)
      {
        console.log(directionsService)
        setDirections(directionsService)  
      }            
  };
  
  const getCurrentMarkers = () => {
    const markerData = [
      pos,
      driverPosition,
      pos2
      // Add more marker data as needed
    ];
  
    // Create an array of <Marker> components based on the marker data
    const markers = markerData.map((marker, index) => (
      <Marker
        key={`marker_${index}`} // Unique key for each marker
        position={{
          lat: marker.lat,
          lng: marker.lng,
        }}
      />
    ));
  
    return markers;
  
  }

  const renderMap = (card) => {
    return (<GoogleMap
        mapContainerStyle={containerStyle}
        center={driverPosition}
        zoom={8}
        options={options}
      >
        
      {directions && <DirectionsRenderer directions={directions} />}

      <DirectionsService options={{
          destination: card.dropoff,
          origin: card.pickup,
          travelMode: 'DRIVING',
        }} callback={handleDirectionsService} />

      {getCurrentMarkers()}
        
      </GoogleMap>)
  }

  const setCurrentMap = (newMap) => {
    currentMap = newMap;
  }
  setCurrentMap(renderMap(card));

  const socketRef = useRef(null);

  useEffect(() => {
    // Establish the WebSocket connection
    socketRef.current = io('http://localhost:5000');

    // Send the "hello" message every minute
    const interval = setInterval(() => {
      socketRef.current.emit('message', {'hello':'1'});
    }, 1000);

    socketRef.current.on('response', (data) => {      
        console.log(data.driver_location)
        console.log(data.passenger_location)
        setDriversPosition(data.driver_location)
        setPos(data.passenger_location);
        setPos2(data.passenger_destination);       
        setCurrentMap(renderMap(card))              
        
      });

    // Clean up the interval and close the WebSocket connection on component unmount
    return () => {
      clearInterval(interval);
      socketRef.current.close();
    };
  }, []);

    return (
      <div className="card-swiper">
        {currentMap}
      </div>
    );
  };

  export default Watch;
