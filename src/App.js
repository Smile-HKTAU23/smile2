import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SearchPage from './SearchPage';
import Watch from './Watch';
import CoursesPage from './CoursesPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SearchPage />} />        
        <Route path="/results" element={<CoursesPage />} />
        <Route path="/watch" element={<Watch />} />        
      </Routes>
    </Router>
  );
};

export default App;
