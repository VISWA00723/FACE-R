import { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { Home, UserPlus, Calendar, Users, Menu, X, CheckCircle2, LogOut, Shield, UserCircle2 } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const adminNavItems = [
    { path: '/admin', icon: Shield, label: 'Admin Panel' },
    { path: '/admin/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/admin/register', icon: UserPlus, label: 'Register Employee' },
    { path: '/admin/verify', icon: CheckCircle2, label: 'Verify Face' },
    { path: '/admin/attendance', icon: Calendar, label: 'Attendance History' },
    { path: '/admin/employees', icon: Users, label: 'Employees' },
  ];

  const userNavItems = [
    { path: '/user', icon: UserCircle2, label: 'User Home' },
    { path: '/user/verify', icon: CheckCircle2, label: 'Verify Face' },
  ];

  const navItems = user?.role === 'admin' ? adminNavItems : userNavItems;

  const closeSidebar = () => setSidebarOpen(false);

  const onLogout = () => {
    logout();
    navigate('/login', { replace: true });
  };

  return (
    <div className="min-h-screen app-bg">
      <div className="aurora aurora-1" />
      <div className="aurora aurora-2" />

      <nav className="glass-nav sticky top-0 z-50">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden inline-flex items-center justify-center p-2 rounded-md text-slate-200 hover:text-white hover:bg-white/10 transition-colors"
                aria-label="Toggle menu"
              >
                {sidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>

              <div className="flex-shrink-0 flex items-center ml-2 lg:ml-0">
                <h1 className="text-lg sm:text-xl lg:text-2xl font-bold text-white">Face Recognition Attendance</h1>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="hidden sm:inline text-xs px-3 py-1 rounded-full bg-white/10 text-sky-200 border border-white/20">
                {user?.role?.toUpperCase()}
              </span>
              <button onClick={onLogout} className="btn btn-secondary">
                <LogOut className="w-4 h-4 mr-2" /> Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex relative">
        {sidebarOpen && (
          <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={closeSidebar} aria-hidden="true" />
        )}

        <aside
          className={`
            fixed lg:sticky top-16 left-0 z-40
            w-64 glass-sidebar
            min-h-[calc(100vh-4rem)]
            transform transition-transform duration-300 ease-in-out
            ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          `}
        >
          <nav className="mt-5 px-2 space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/admin' || item.path === '/user'}
                onClick={closeSidebar}
                className={({ isActive }) =>
                  `group flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                    isActive
                      ? 'bg-sky-500/30 text-sky-100 shadow-lg shadow-sky-900/30'
                      : 'text-slate-200 hover:bg-white/10 hover:text-white'
                  }`
                }
              >
                <item.icon className="mr-3 h-5 w-5 flex-shrink-0" />
                <span>{item.label}</span>
              </NavLink>
            ))}
          </nav>
        </aside>

        <main className="flex-1 w-full p-4 sm:p-6 lg:p-8 overflow-x-hidden">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
