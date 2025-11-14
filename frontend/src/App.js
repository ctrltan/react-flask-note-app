import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { createContext, useContext, useState } from 'react';
import HomePage from './pages/HomePage.js';
import LoginPage from './pages/LoginPage.js';
import SignupPage from './pages/SignupPage.js';
import usePersistedState from './components/hooks/persistentState.js';
import axios from 'axios';

export const UserContext = createContext();

function App() {
  const [user, setUser] = usePersistedState('user');

  return (
    <UserContext value={{user, setUser}}>
    <Router>
      <div>
        <Routes>
          <Route path='/' element={<HomePage />} />
          <Route path='/login' element={<LoginPage />}/>
          <Route path='/signup' element={<SignupPage />} />
        </Routes>
      </div>
    </Router>
    </UserContext>
  );
}

export default App;
