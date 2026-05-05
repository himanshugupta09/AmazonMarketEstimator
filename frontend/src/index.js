import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // This is crucial: it injects all the Tailwind styling
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);