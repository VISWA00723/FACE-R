import { useState, useEffect } from 'react';
import { Users, UserCheck, UserX, LogIn, LogOut } from 'lucide-react';
import { attendanceAPI } from '@/services/api';
import type { AttendanceTodayResponse, AttendanceStats } from '@/types';
import { formatTime, getStatusColor } from '@/utils/helpers';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [todayData, setTodayData] = useState<AttendanceTodayResponse | null>(null);
  const [statsData, setStatsData] = useState<AttendanceStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [today, stats] = await Promise.all([
        attendanceAPI.getToday(),
        attendanceAPI.getStats(),
      ]);
      setTodayData(today);
      setStatsData(stats);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !todayData) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error && !todayData) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <button
          onClick={fetchData}
          className="btn btn-secondary"
        >
          Refresh
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <StatCard
          title="Total Employees"
          value={todayData?.total_employees || 0}
          icon={Users}
          color="bg-blue-500"
        />
        <StatCard
          title="Present"
          value={todayData?.present || 0}
          icon={UserCheck}
          color="bg-green-500"
        />
        <StatCard
          title="Absent"
          value={todayData?.absent || 0}
          icon={UserX}
          color="bg-red-500"
        />
        <StatCard
          title="Currently IN"
          value={todayData?.in_count || 0}
          icon={LogIn}
          color="bg-purple-500"
        />
        <StatCard
          title="Left Office (OUT)"
          value={todayData?.out_count || 0}
          icon={LogOut}
          color="bg-orange-500"
        />
      </div>

      {/* Chart */}
      {statsData && statsData.daily_stats.length > 0 && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Attendance Trend (Last 7 Days)</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={statsData.daily_stats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="present" fill="#10b981" name="Present" />
              <Bar dataKey="in" fill="#8b5cf6" name="IN" />
              <Bar dataKey="out" fill="#f97316" name="OUT" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Today's Attendance Table */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Today's Attendance</h2>
        
        {todayData?.attendance_logs.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No attendance records for today</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Employee ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Department
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    In Time
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Out Time
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {todayData?.attendance_logs.map((log) => (
                  <tr key={log.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {log.employee_id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {log.employee_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {log.department}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatTime(log.in_time)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatTime(log.out_time)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(log.status)}`}>
                        {log.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

// Stat Card Component
interface StatCardProps {
  title: string;
  value: number;
  icon: React.ElementType;
  color: string;
}

const StatCard = ({ title, value, icon: Icon, color }: StatCardProps) => (
  <div className="card">
    <div className="flex items-center">
      <div className={`${color} p-3 rounded-lg`}>
        <Icon className="h-6 w-6 text-white" />
      </div>
      <div className="ml-4">
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
      </div>
    </div>
  </div>
);

export default Dashboard;
