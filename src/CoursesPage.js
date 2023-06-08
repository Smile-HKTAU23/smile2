import React from 'react';
import { useLocation } from 'react-router-dom';
import CardSwiper from './Maps.js';

const CoursesPage = () => {
  const location = useLocation();
  console.log(location.state)
  let cards = location.state.map((loc) => {
    return {
      id:loc.id,
      lat:loc.pickup.lat,
      lng:loc.pickup.lng,
    }
  }
  );  


  return (
    <div>
      <h2>Results Page</h2>
      <p>Destination: </p>
      <CardSwiper cards={cards} locations={location.state}/>
    </div>
  );
};

export default CoursesPage;
