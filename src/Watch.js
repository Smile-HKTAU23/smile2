import React, { useEffect, useState, useRef } from 'react';
import './Maps.css';
import {
  DirectionsRenderer,
  Marker,
  GoogleMap,
  DirectionsService,
} from '@react-google-maps/api';
import io from 'socket.io-client';
import { useLocation } from 'react-router-dom';

const Watch = () => {
  const [directions, setDirections] = useState(null);
  const [pos, setPos] = useState({ lat: 32.069235, lng: 34.825947 });
  const [pos2, setPos2] = useState({ lat: 32.069235, lng: 34.825947 });
  const [driverPosition, setDriverPosition] = useState({
    lat: 32.110820, 
    lng: 34.806710,
  });
  const [currentMap, setCurrentMap] = useState(null);

  const parameters_location = useLocation();
  const card = parameters_location.state.card;

  console.log(card)

  const containerStyle = {
    width: '100%',
    height: '51rem',
  };

  const options = {
    disableDefaultUI: true,
  };

  const handleDirectionsService = (directionsService) => {
      setDirections(directionsService);
  };

  const getCurrentMarkers = () => {
    const markerData = [driverPosition, pos2];

    const markers = markerData.map((marker, index) => (
      <Marker
        key={`marker_${index}`}
        position={{
          lat: marker.lat,
          lng: marker.lng,
        }}
      />
    ));

    return markers;
  };

  const renderMap = (card) => {
    return (
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={card.pickup}
        zoom={8}
        options={options}
      >
        {directions && <DirectionsRenderer directions={directions} />}

        <DirectionsService
          options={{
            destination: card.dropoff,
            origin: card.pickup,
            travelMode: 'DRIVING',
          }}
          callback={handleDirectionsService}
        />

        {getCurrentMarkers()}
      </GoogleMap>
    );
  };

  const socketRef = useRef(null);

  useEffect(() => {
    socketRef.current = io('http://localhost:5000');

    const interval = setInterval(() => {
      socketRef.current.emit('message', { hello: '1' });
    }, 1000);

    socketRef.current.on('response', (data) => {
      setDriverPosition(data.driver_location);
      setPos(data.passenger_location);
      setPos2(data.passenger_destination);
    });

    return () => {
      clearInterval(interval);
      socketRef.current.close();
    };
  }, []);

  useEffect(() => {
    setCurrentMap(renderMap(card));
  }, [driverPosition, pos, pos2]);

  return <div className="card-swiper">{currentMap}</div>;
};

export default Watch;
