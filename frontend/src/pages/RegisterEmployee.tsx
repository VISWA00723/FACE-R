import { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Camera, Trash2, UserPlus, X } from 'lucide-react';
import { employeeAPI } from '@/services/api';
import type { EmployeeCreate } from '@/types';

const RegisterEmployee = () => {
  const webcamRef = useRef<Webcam>(null);
  const [employeeId, setEmployeeId] = useState('');
  const [name, setName] = useState('');
  const [department, setDepartment] = useState('');
  const [capturedImages, setCapturedImages] = useState<string[]>([]);
  const [showWebcam, setShowWebcam] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc && capturedImages.length < 50) {
        setCapturedImages((prev) => [...prev, imageSrc]);
      }
    }
  }, [capturedImages.length]);

  const removeImage = (index: number) => {
    setCapturedImages((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (capturedImages.length === 0) {
      setMessage({ type: 'error', text: 'Please capture at least one image' });
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
        text: `Successfully registered ${name} with ${capturedImages.length} images`,
      });

      // Reset form
      setEmployeeId('');
      setName('');
      setDepartment('');
      setCapturedImages([]);
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
    setCapturedImages([]);
    setShowWebcam(false);
    setMessage(null);
  };

  return (
    <div className="w-full">
      <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4 sm:mb-6">Register Employee</h1>

      {message && (
        <div
          className={`mb-4 sm:mb-6 p-3 sm:p-4 rounded-lg text-sm sm:text-base ${
            message.type === 'success'
              ? 'bg-green-50 text-green-700 border border-green-200'
              : 'bg-red-50 text-red-700 border border-red-200'
          }`}
        >
          {message.text}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Employee Information */}
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

        {/* Webcam Capture */}
        <div className="card">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3 sm:gap-0 mb-4">
            <h2 className="text-lg sm:text-xl font-semibold">
              Capture Face Images ({capturedImages.length}/50)
            </h2>
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
                    Capture
                  </button>
                </div>
              </div>
              <p className="text-xs sm:text-sm text-gray-600 mt-2 text-center">
                Position your face in the camera and capture from different angles
              </p>
            </div>
          )}

          {/* Captured Images Grid */}
          {capturedImages.length > 0 && (
            <div>
              <h3 className="text-base sm:text-lg font-medium mb-3">Captured Images</h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 sm:gap-3 md:gap-4">
                {capturedImages.map((img, index) => (
                  <div key={index} className="relative group">
                    <img
                      src={img}
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
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Action Buttons */}
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
            disabled={loading || capturedImages.length === 0}
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

      {/* Tips */}
      <div className="mt-4 sm:mt-6 card bg-blue-50 border border-blue-200">
        <h3 className="text-base sm:text-lg font-semibold text-blue-900 mb-2">Tips for Best Results</h3>
        <ul className="list-disc list-inside text-xs sm:text-sm text-blue-800 space-y-1">
          <li>Capture at least 20-30 images for better accuracy</li>
          <li>Capture from different angles (front, left, right, slightly up/down)</li>
          <li>Ensure good lighting conditions</li>
          <li>Maintain a neutral expression and face the camera directly</li>
          <li>Remove glasses or masks if possible</li>
        </ul>
      </div>
    </div>
  );
};

export default RegisterEmployee;
