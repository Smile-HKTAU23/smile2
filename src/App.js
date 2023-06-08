import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SearchPage from './SearchPage';
import LivePage from './LivePage';
import CoursesPage from './CoursesPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LivePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/results" element={<CoursesPage />} />
      </Routes>
    </Router>
  );
};

export default App;
