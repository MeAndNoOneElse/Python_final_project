import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { GroupContext } from './hooks/useApi';
import Groups from './pages/Groups';
import Dashboard from './pages/Dashboard';
import Storage from './pages/Storage';
import ShoppingList from './pages/ShoppingList';
import Expenses from './pages/Expenses';
import Debts from './pages/Debts';
import Distribute from './pages/Distribute';
import GroupMembers from './pages/GroupMembers';

// Инициализация Telegram WebApp
const initTelegramWebApp = () => {
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.expand();
    window.Telegram.WebApp.setBackgroundColor('#0f172a');
    window.Telegram.WebApp.setHeaderColor('#0f172a');
    window.Telegram.WebApp.enableClosingByActions();
  }
};

function App() {
  const [currentGroup, setCurrentGroup] = useState(null);

  useEffect(() => {
    initTelegramWebApp();
  }, []);

  return (
    <GroupContext.Provider value={{ currentGroup, setCurrentGroup }}>
      <Router>
        <div className="bg-gray-900 text-white min-h-screen tg-theme">
          <div className="p-4 pb-[calc(env(safe-area-inset-bottom)+1rem)]">
            <Routes>
              <Route path="/" element={<Groups />} />
              <Route path="/group/:groupId/dashboard" element={<Dashboard />} />
              <Route path="/group/:groupId/storage" element={<Storage />} />
              <Route path="/group/:groupId/shopping-list" element={<ShoppingList />} />
              <Route path="/group/:groupId/expenses" element={<Expenses />} />
              <Route path="/group/:groupId/debts" element={<Debts />} />
              <Route path="/group/:groupId/distribute" element={<Distribute />} />
              <Route path="/group/:groupId/members" element={<GroupMembers />} />
            </Routes>
          </div>
        </div>
      </Router>
    </GroupContext.Provider>
  );
}
export default App;
