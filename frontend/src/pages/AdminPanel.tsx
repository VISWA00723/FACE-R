import { Link } from 'react-router-dom';
import { Shield, UserPlus, CheckCircle2, Calendar, Users } from 'lucide-react';

const cards = [
  { to: '/admin/register', title: 'Register Employee', description: 'Capture profiles and biometric data.', icon: UserPlus },
  { to: '/admin/verify', title: 'Verify Face', description: 'Validate recognition flow without attendance.', icon: CheckCircle2 },
  { to: '/admin/attendance', title: 'Attendance Reports', description: 'Review trends and export records.', icon: Calendar },
  { to: '/admin/employees', title: 'Manage Employees', description: 'View and maintain employee records.', icon: Users },
];

const AdminPanel = () => {
  return (
    <div className="space-y-6">
      <section className="glass-panel">
        <div className="flex items-center gap-3">
          <Shield className="text-cyan-300" />
          <div>
            <h1 className="text-3xl font-bold text-white">Admin Panel</h1>
            <p className="text-slate-300">Control center for operations, attendance, and employee lifecycle.</p>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards.map((card) => (
          <Link key={card.title} to={card.to} className="card-3d">
            <card.icon className="w-8 h-8 text-cyan-300 mb-3" />
            <h2 className="text-lg font-semibold text-white">{card.title}</h2>
            <p className="text-slate-300 text-sm mt-1">{card.description}</p>
          </Link>
        ))}
      </section>
    </div>
  );
};

export default AdminPanel;
