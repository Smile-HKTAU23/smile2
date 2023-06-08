import React from 'react';
import { useLocation } from 'react-router-dom';

const CoursesPage = () => {
  const location = useLocation();
  console.log(location.state)

  return (
    <div>
      <h2>Results Page</h2>
      <p>Destination: </p>
    </div>
  );
};

export default CoursesPage;
