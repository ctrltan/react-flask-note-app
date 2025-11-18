import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import { createContext, useContext, useState } from 'react';
import HomePage from './pages/HomePage.js';
import LoginPage from './pages/LoginPage.js';
import SignupPage from './pages/SignupPage.js';
import usePersistedState from './components/hooks/persistentState.js';
import ProtectedRoute from './components/wrappers/ProtectedRoute.js';

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
          <Route element={<ProtectedRoute />}>
            <Route path='/notes'/>
          </Route>
        </Routes>
      </div>
    </Router>
    </UserContext>
  );
}

export default App;
