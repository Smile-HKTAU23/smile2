import React, { useEffect, useState } from 'react';
import './Maps.css'
import { DirectionsRenderer, Marker, GoogleMap, DirectionsService } from '@react-google-maps/api';



const Watch = ({ location, pos, pos2 }) => {
    const [directions, setDirections] = useState(null);
    let currentMap = null;

    const card = location
    console.log(card, pos)
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
  
  let driverPosition = {lat: 32.110820, lng:34.806710}

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
    console.log("marker")
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


    return (
      <div className="card-swiper">
        {currentMap}
      </div>
    );
  };

  export default Watch;
