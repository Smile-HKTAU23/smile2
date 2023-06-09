import React from 'react';
import { useLocation } from 'react-router-dom';
import CardSwiper from './Maps.js';

const CoursesPage = () => {
  const location = useLocation();
  console.log(location.state)
  const options = location.state.options;
  const pos = location.state.pos;
  let cards = options.map((loc) => {
    return {
      id:loc.id,
      lat:loc.pickup.lat,
      lng:loc.pickup.lng,
    }
  }
  );  


  return (
    <div className='cetered'>
      <div>
        <h2 className='centered'>Results Page</h2>
      </div>
      <CardSwiper cards={cards} locations={options} pos={pos}/>
    </div>
  );
};

export default CoursesPage;
