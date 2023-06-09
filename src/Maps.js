import React, { useEffect, useState } from 'react';
import './Maps.css'
import { DirectionsRenderer, Marker, GoogleMap, DirectionsService } from '@react-google-maps/api';

const CardSwiper = ({ cards, locations, pos }) => {
    const [currentCardIndex, setCurrentCardIndex] = useState(0);
    const [currentMap, setCurrentMap] = useState(0);
    const [directions, setDirections] = useState(null);
    const [a, seta] = useState(0);
    
    
const containerStyle = {
    width: '100%',
    height: '650px'
  };
  
  const options = {
    disableDefaultUI: true
  }
  
  // Define your origin and destination
  const origin = { lat: 31.7749, lng: 31.4194 };
  const destination = { lat: 31.0522, lng: 31.2437 };
  const pickup1 = {lng: 34.82343,  lat: 32.06335}
  const dropoff1 =  {lng: 34.82343, lat: 32.06345}

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
      
    // Render the Google Maps component using the card's location information
    // Replace the following code with your own implementation using the Google Maps API
    console.log("here")
  
    console.log(card)
    return (
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={card.pickup}
          zoom={12}
          options={options}
        >
          
        {directions && <DirectionsRenderer directions={directions} />}

        <DirectionsService options={{
            destination: card.dropoff,
            origin: card.pickup,
            travelMode: 'DRIVING',
          }} callback={handleDirectionsService} />
        {getCurrentMarkers()}
          
        </GoogleMap>
    )
  };
  

    const handleSwipeLeft = () => {
      setCurrentCardIndex((prevIndex) => (prevIndex === 0 ? cards.length - 1 : prevIndex - 1));
      setCurrentMap(renderMap(locations[currentCardIndex]));
    };
  
    const handleSwipeRight = () => {
      setCurrentCardIndex((prevIndex) => (prevIndex === cards.length - 1 ? 0 : prevIndex + 1));
      setCurrentMap(renderMap(locations[currentCardIndex]));
    };
  
  
    const nextPage = () => {
      return
    }
  
  
    useEffect(() => {
        if (currentMap == 0 ) {

        const currentMap1 = renderMap({
            id: 1,
            location: 'Israel',
            pickup: pickup1,
            dropoff: dropoff1,
          });
        setCurrentMap(currentMap1);
    }
},[a]);



    return (
      <div>
      <div className="card-swiper">
        <button className="swipe-button left" onClick={handleSwipeLeft}>
          &lt;
        </button>
        <div className="card">{currentMap}</div>
        <button className="swipe-button right" onClick={handleSwipeRight}>
          &gt;
        </button>
        
      </div>
      <div className='down-button-div'>
        <button className="next-page down" onClick={nextPage}>
          choose
        </button>
      </div>
      </div>
    );
  };

  export default CardSwiper;
