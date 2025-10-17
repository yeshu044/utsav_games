import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from './stores/authStore';

// Pages
import LoginPage from './pages/auth/LoginPage';
import EventEntryPage from './pages/event/EventEntryPage';
import DashboardPage from './pages/event/DashboardPage';
import GameLevelPage from './pages/game/GameLevelPage';
import LeaderboardPage from './pages/event/LeaderboardPage';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

function App() {
  return (
    <Router>
      <Toaster position="top-center" />
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/event/:qrToken" element={<EventEntryPage />} />
        
        {/* Protected Routes */}
        <Route
          path="/dashboard/:eventId"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/event/:eventId/level/:levelId"
          element={
            <ProtectedRoute>
              <GameLevelPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/event/:eventId/leaderboard"
          element={
            <ProtectedRoute>
              <LeaderboardPage />
            </ProtectedRoute>
          }
        />
        
        {/* Default Route */}
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
