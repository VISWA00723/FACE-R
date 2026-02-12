import { useState, useRef, useCallback, useMemo } from 'react';
import Webcam from 'react-webcam';
import { Camera, Trash2, UserPlus, X } from 'lucide-react';
import { employeeAPI } from '@/services/api';
import type { EmployeeCreate } from '@/types';

type CaptureModeKey =
  | 'front'
  | 'left'
  | 'right'
  | 'up'
  | 'down'
  | 'near'
  | 'far'
  | 'eyes_open'
  | 'eyes_closed'
  | 'with_mask'
  | 'without_mask';

interface CaptureMode {
  key: CaptureModeKey;
  label: string;
  short: string;
  target: number;
  required: boolean;
}

interface CapturedSample {
  image: string;
  mode: CaptureModeKey;
}

const captureModes: CaptureMode[] = [
  { key: 'front', label: 'Front facing', short: 'Front', target: 4, required: true },
  { key: 'left', label: 'Turn 30° left', short: 'Left', target: 3, required: true },
  { key: 'right', label: 'Turn 30° right', short: 'Right', target: 3, required: true },
  { key: 'up', label: 'Chin slightly up', short: 'Up', target: 2, required: true },
  { key: 'down', label: 'Chin slightly down', short: 'Down', target: 2, required: true },
  { key: 'near', label: 'Move camera closer', short: 'Near', target: 2, required: true },
  { key: 'far', label: 'Move camera a bit farther', short: 'Far', target: 2, required: true },
  { key: 'eyes_open', label: 'Eyes open', short: 'Eyes Open', target: 3, required: true },
  { key: 'eyes_closed', label: 'Eyes gently closed', short: 'Eyes Closed', target: 2, required: true },
  { key: 'with_mask', label: 'With mask', short: 'Mask On', target: 3, required: true },
  { key: 'without_mask', label: 'Without mask', short: 'Mask Off', target: 3, required: true },
];

const RegisterEmployee = () => {
  const webcamRef = useRef<Webcam>(null);
  const [employeeId, setEmployeeId] = useState('');
  const [name, setName] = useState('');
  const [department, setDepartment] = useState('');
  const [capturedSamples, setCapturedSamples] = useState<CapturedSample[]>([]);
  const [selectedMode, setSelectedMode] = useState<CaptureModeKey>('front');
  const [showWebcam, setShowWebcam] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const capturedImages = useMemo(() => capturedSamples.map((sample) => sample.image), [capturedSamples]);

  const modeCounts = useMemo(() => {
    return capturedSamples.reduce<Record<CaptureModeKey, number>>((acc, sample) => {
      acc[sample.mode] = (acc[sample.mode] || 0) + 1;
      return acc;
    }, {
      front: 0,
      left: 0,
      right: 0,
      up: 0,
      down: 0,
      near: 0,
      far: 0,
      eyes_open: 0,
      eyes_closed: 0,
      with_mask: 0,
      without_mask: 0,
    });
  }, [capturedSamples]);

  const requiredChecklist = useMemo(() => {
    return captureModes
      .filter((mode) => mode.required)
      .map((mode) => ({
        ...mode,
        count: modeCounts[mode.key],
        completed: modeCounts[mode.key] >= mode.target,
      }));
  }, [modeCounts]);

  const allRequiredCaptured = requiredChecklist.every((item) => item.completed);

  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc && capturedSamples.length < 50) {
        setCapturedSamples((prev) => [...prev, { image: imageSrc, mode: selectedMode }]);
      }
    }
  }, [capturedSamples.length, selectedMode]);

  const removeImage = (index: number) => {
    setCapturedSamples((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (capturedImages.length === 0) {
      setMessage({ type: 'error', text: 'Please capture at least one image.' });
      return;
    }

    if (!allRequiredCaptured) {
      setMessage({
        type: 'error',
        text: 'Please complete all required training scenarios (angles, eyes, mask on/off) before registering.',
      });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const data: EmployeeCreate = {
        employee_id: employeeId,
        name,
        department,
        images: capturedImages,
      };

      await employeeAPI.register(data);

      setMessage({
        type: 'success',
        text: `Successfully registered ${name} with ${capturedImages.length} guided training images.`,
      });

      setEmployeeId('');
      setName('');
      setDepartment('');
      setCapturedSamples([]);
      setSelectedMode('front');
      setShowWebcam(false);
    } catch (err: any) {
      console.error('Error registering employee:', err);
      setMessage({
        type: 'error',
        text: err.response?.data?.detail || 'Failed to register employee',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setEmployeeId('');
    setName('');
    setDepartment('');
    setCapturedSamples([]);
    setSelectedMode('front');
    setShowWebcam(false);
    setMessage(null);
  };

  return (
    <div className="w-full">
      <h1 className="text-2xl sm:text-3xl font-bold text-slate-100 mb-4 sm:mb-6">Register Employee</h1>

      {message && (
        <div
          className={`mb-4 sm:mb-6 p-3 sm:p-4 rounded-lg text-sm sm:text-base ${
            message.type === 'success'
              ? 'bg-sky-50 text-sky-700 border border-sky-200'
              : 'bg-red-50 text-red-700 border border-red-200'
          }`}
        >
          {message.text}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="card">
          <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4">Employee Information</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
            <div>
              <label htmlFor="employeeId" className="label">
                Employee ID *
              </label>
              <input
                id="employeeId"
                type="text"
                value={employeeId}
                onChange={(e) => setEmployeeId(e.target.value)}
                className="input"
                required
                placeholder="EMP001"
              />
            </div>
            <div>
              <label htmlFor="name" className="label">
                Full Name *
              </label>
              <input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="input"
                required
                placeholder="John Doe"
              />
            </div>
            <div>
              <label htmlFor="department" className="label">
                Department *
              </label>
              <input
                id="department"
                type="text"
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                className="input"
                required
                placeholder="Engineering"
              />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 sm:gap-0 mb-4">
            <h2 className="text-lg sm:text-xl font-semibold">Capture Face Images ({capturedImages.length}/50)</h2>
            <button
              type="button"
              onClick={() => setShowWebcam(!showWebcam)}
              className="btn btn-primary w-full sm:w-auto"
              disabled={capturedImages.length >= 50}
            >
              {showWebcam ? (
                <>
                  <X className="w-4 h-4 mr-2" />
                  Close Camera
                </>
              ) : (
                <>
                  <Camera className="w-4 h-4 mr-2" />
                  Open Camera
                </>
              )}
            </button>
          </div>

          <div className="mb-4 p-3 rounded-lg bg-slate-900/40 border border-slate-700">
            <p className="text-sm text-slate-200 mb-2">Guided capture mode (critical for stronger training):</p>
            <div className="flex flex-wrap gap-2">
              {captureModes.map((mode) => {
                const active = selectedMode === mode.key;
                const done = modeCounts[mode.key] >= mode.target;
                return (
                  <button
                    key={mode.key}
                    type="button"
                    className={`px-3 py-1.5 rounded-lg text-xs border transition ${
                      active
                        ? 'bg-sky-500/30 border-sky-300 text-sky-100'
                        : done
                        ? 'bg-orange-500/20 border-orange-300 text-orange-100'
                        : 'bg-slate-800 border-slate-600 text-slate-200'
                    }`}
                    onClick={() => setSelectedMode(mode.key)}
                  >
                    {mode.short} ({modeCounts[mode.key]}/{mode.target})
                  </button>
                );
              })}
            </div>
            <p className="text-xs text-slate-300 mt-2">
              Active instruction: <span className="font-semibold text-sky-200">{captureModes.find((mode) => mode.key === selectedMode)?.label}</span>
            </p>
          </div>

          {showWebcam && (
            <div className="mb-4">
              <div className="relative bg-black rounded-lg overflow-hidden aspect-video">
                <Webcam
                  ref={webcamRef}
                  audio={false}
                  screenshotFormat="image/jpeg"
                  className="w-full h-full object-cover"
                  mirrored={true}
                  screenshotQuality={0.92}
                  videoConstraints={{
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: 'user',
                    aspectRatio: 16 / 9,
                  }}
                  forceScreenshotSourceSize={false}
                  imageSmoothing={true}
                />
                <div className="absolute bottom-3 sm:bottom-4 left-1/2 transform -translate-x-1/2">
                  <button
                    type="button"
                    onClick={capture}
                    disabled={capturedImages.length >= 50}
                    className="btn btn-primary px-6 sm:px-8 py-2 sm:py-3 text-base sm:text-lg shadow-lg"
                  >
                    <Camera className="w-4 sm:w-5 h-4 sm:h-5 mr-2" />
                    Capture ({captureModes.find((mode) => mode.key === selectedMode)?.short})
                  </button>
                </div>
              </div>
              <p className="text-xs sm:text-sm text-slate-300 mt-2 text-center">
                Follow the active instruction and capture multiple shots with small motion and expression changes.
              </p>
            </div>
          )}

          <div className="mb-4 p-3 rounded-lg bg-slate-900/35 border border-slate-700">
            <h3 className="text-sm font-semibold text-slate-100 mb-2">Required scenario checklist</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 text-xs">
              {requiredChecklist.map((item) => (
                <div
                  key={item.key}
                  className={`px-2 py-1.5 rounded border ${
                    item.completed
                      ? 'bg-sky-500/20 border-sky-400 text-sky-100'
                      : 'bg-slate-800 border-slate-600 text-slate-300'
                  }`}
                >
                  {item.label}: {item.count}/{item.target}
                </div>
              ))}
            </div>
          </div>

          {capturedImages.length > 0 && (
            <div>
              <h3 className="text-base sm:text-lg font-medium mb-3">Captured Images</h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 sm:gap-3 md:gap-4">
                {capturedSamples.map((sample, index) => (
                  <div key={index} className="relative group">
                    <img
                      src={sample.image}
                      alt={`Capture ${index + 1}`}
                      className="w-full h-24 sm:h-28 md:h-32 object-cover rounded-lg border-2 border-gray-200 transition-transform group-hover:scale-105"
                    />
                    <button
                      type="button"
                      onClick={() => removeImage(index)}
                      className="absolute top-1 right-1 bg-red-500 text-white p-1.5 rounded-full opacity-100 sm:opacity-0 group-hover:opacity-100 transition-opacity shadow-lg"
                      aria-label="Remove image"
                    >
                      <Trash2 className="w-3 h-3 sm:w-4 sm:h-4" />
                    </button>
                    <span className="absolute bottom-1 left-1 bg-black bg-opacity-60 text-white text-xs px-1.5 sm:px-2 py-0.5 sm:py-1 rounded">
                      {index + 1}
                    </span>
                    <span className="absolute bottom-1 right-1 bg-slate-900/80 text-sky-100 text-[10px] px-1.5 py-0.5 rounded">
                      {captureModes.find((mode) => mode.key === sample.mode)?.short}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="flex flex-col sm:flex-row justify-end gap-3 sm:gap-4">
          <button
            type="button"
            onClick={handleReset}
            className="btn btn-secondary w-full sm:w-auto order-2 sm:order-1"
            disabled={loading}
          >
            Reset
          </button>
          <button
            type="submit"
            className="btn btn-primary w-full sm:w-auto order-1 sm:order-2"
            disabled={loading || capturedImages.length === 0 || !allRequiredCaptured}
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Registering...
              </>
            ) : (
              <>
                <UserPlus className="w-5 h-5 mr-2" />
                Register Employee
              </>
            )}
          </button>
        </div>
      </form>

      <div className="mt-4 sm:mt-6 card bg-blue-50 border border-blue-200">
        <h3 className="text-base sm:text-lg font-semibold text-blue-900 mb-2">Training Capture Protocol</h3>
        <ul className="list-disc list-inside text-xs sm:text-sm text-blue-800 space-y-1">
          <li>Collect a balanced set from all guided angles and distances for better embeddings.</li>
          <li>Capture with mask and without mask, plus eyes open and gently closed to improve robustness.</li>
          <li>Use varied lighting (soft indoor, brighter side-light) but keep face visible and sharp.</li>
          <li>Capture natural micro-expressions (neutral, slight smile) without heavy motion blur.</li>
          <li>Avoid overexposure and keep the full face inside frame for every scenario.</li>
        </ul>
      </div>
    </div>
  );
};

export default RegisterEmployee;
