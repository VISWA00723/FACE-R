import { Link } from 'react-router-dom';
import { Sparkles, CheckCircle2 } from 'lucide-react';

const UserHome = () => {
  return (
    <div className="space-y-6">
      <section className="glass-panel animate-float">
        <div className="flex items-center gap-3">
          <Sparkles className="text-emerald-300" />
          <div>
            <h1 className="text-3xl font-bold text-white">User Workspace</h1>
            <p className="text-slate-300">Use face verification quickly with a smooth 3D experience.</p>
          </div>
        </div>
      </section>

      <Link to="/user/verify" className="card-3d block max-w-xl">
        <CheckCircle2 className="w-8 h-8 text-emerald-300 mb-3" />
        <h2 className="text-xl font-semibold text-white">Verify Face</h2>
        <p className="text-slate-300 text-sm mt-1">Open the camera and validate detection/recognition in real-time.</p>
      </Link>
    </div>
  );
};

export default UserHome;
