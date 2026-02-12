import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogIn, ShieldCheck, UserCircle2 } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      await login(username.trim(), password);
      navigate('/', { replace: true });
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden login-bg p-6 flex items-center justify-center">
      <div className="orb orb-a" />
      <div className="orb orb-b" />
      <div className="glass-panel w-full max-w-md animate-float">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-white">Face-R Secure Login</h1>
          <p className="text-slate-300 mt-2 text-sm">Real-time authentication with database-backed users.</p>
        </div>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="label text-slate-200">Username</label>
            <input
              className="input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              autoComplete="username"
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
              autoComplete="current-password"
              required
            />
          </div>

          {error && <p className="text-red-300 text-sm">{error}</p>}

          <button type="submit" className="btn btn-primary w-full" disabled={loading}>
            {loading ? 'Signing in...' : <><LogIn className="w-4 h-4 mr-2" />Sign In</>}
          </button>
        </form>

        <div className="mt-5 p-3 rounded-lg bg-slate-900/50 border border-slate-700 text-xs text-slate-300 space-y-1">
          <p className="flex items-center gap-2"><ShieldCheck className="w-3.5 h-3.5 text-lime-300" /> <strong>Admin:</strong> admin / Admin@12345</p>
          <p className="flex items-center gap-2"><UserCircle2 className="w-3.5 h-3.5 text-sky-300" /> <strong>User:</strong> user / User@12345</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
