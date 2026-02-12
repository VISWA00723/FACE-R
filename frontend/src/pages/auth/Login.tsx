import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogIn, ShieldCheck, UserCircle2 } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import type { UserRole } from '@/types/auth';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<UserRole>('user');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      await login(username.trim(), password, role);
      navigate(role === 'admin' ? '/admin' : '/user', { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-slate-950 via-emerald-950 to-cyan-950 p-6 flex items-center justify-center">
      <div className="aurora aurora-1" />
      <div className="aurora aurora-2" />
      <div className="glass-panel w-full max-w-md animate-float">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-white">Face-R Access Portal</h1>
          <p className="text-slate-300 mt-2 text-sm">Secure login for users and administrators</p>
        </div>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="label text-slate-200">Role</label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                className={`btn ${role === 'user' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setRole('user')}
              >
                <UserCircle2 className="w-4 h-4 mr-2" /> User
              </button>
              <button
                type="button"
                className={`btn ${role === 'admin' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setRole('admin')}
              >
                <ShieldCheck className="w-4 h-4 mr-2" /> Admin
              </button>
            </div>
          </div>

          <div>
            <label className="label text-slate-200">Username</label>
            <input
              className="input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>

          <div>
            <label className="label text-slate-200">Password</label>
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>

          {error && <p className="text-red-300 text-sm">{error}</p>}

          <button type="submit" className="btn btn-primary w-full" disabled={loading}>
            {loading ? 'Signing in...' : <><LogIn className="w-4 h-4 mr-2" />Sign In</>}
          </button>
        </form>

        <div className="mt-5 p-3 rounded-lg bg-slate-900/50 border border-slate-700 text-xs text-slate-300">
          <p><strong>User:</strong> user / user123</p>
          <p><strong>Admin:</strong> admin / admin123</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
