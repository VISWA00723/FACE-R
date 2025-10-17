import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from '@/components/Layout';
import Dashboard from '@/pages/Dashboard';
import RegisterEmployee from '@/pages/RegisterEmployee';
import AttendanceHistory from '@/pages/AttendanceHistory';
import EmployeeList from '@/pages/EmployeeList';
import VerifyFace from '@/pages/VerifyFace';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="register" element={<RegisterEmployee />} />
          <Route path="verify" element={<VerifyFace />} />
          <Route path="attendance" element={<AttendanceHistory />} />
          <Route path="employees" element={<EmployeeList />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
