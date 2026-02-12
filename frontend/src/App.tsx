import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from '@/components/Layout';
import Dashboard from '@/pages/Dashboard';
import RegisterEmployee from '@/pages/RegisterEmployee';
import AttendanceHistory from '@/pages/AttendanceHistory';
import EmployeeList from '@/pages/EmployeeList';
import VerifyFace from '@/pages/VerifyFace';
import Login from '@/pages/auth/Login';
import AdminPanel from '@/pages/AdminPanel';
import UserHome from '@/pages/UserHome';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { AuthProvider, useAuth } from '@/context/AuthContext';

const RootRedirect = () => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  return <Navigate to={user.role === 'admin' ? '/admin' : '/user'} replace />;
};

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<RootRedirect />} />
      <Route path="/login" element={<Login />} />

      <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
        <Route path="/admin" element={<Layout />}>
          <Route index element={<AdminPanel />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="register" element={<RegisterEmployee />} />
          <Route path="verify" element={<VerifyFace />} />
          <Route path="attendance" element={<AttendanceHistory />} />
          <Route path="employees" element={<EmployeeList />} />
        </Route>
      </Route>

      <Route element={<ProtectedRoute allowedRoles={['user']} />}>
        <Route path="/user" element={<Layout />}>
          <Route index element={<UserHome />} />
          <Route path="verify" element={<VerifyFace />} />
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}

export default App;
