import { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Camera, CheckCircle, XCircle, User, AlertTriangle } from 'lucide-react';
import { recognitionAPI } from '@/services/api';

interface VerificationResult {
  faceDetected: boolean;
  recognized: boolean;
  employee?: {
    id: string;
    name: string;
    department: string;
  };
  confidence?: number;
  message: string;
}

const VerifyFace = () => {
  const webcamRef = useRef<Webcam>(null);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [showWebcam, setShowWebcam] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VerificationResult | null>(null);

  const capture = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setCapturedImage(imageSrc);
        setShowWebcam(false);
        setResult(null);
      }
    }
  }, []);

  const handleVerify = async () => {
    if (!capturedImage) return;

    setLoading(true);
    setResult(null);

    try {
      // First detect if face exists
      const detectResponse = await recognitionAPI.detect(capturedImage);
      
      if (!detectResponse.face_detected) {
        setResult({
          faceDetected: false,
          recognized: false,
          message: detectResponse.message || 'No face detected in the image',
        });
        setLoading(false);
        return;
      }

      // If face detected, try to recognize
      try {
        const recognizeResponse = await recognitionAPI.recognize(capturedImage);
        
        if (recognizeResponse.recognized) {
          setResult({
            faceDetected: true,
            recognized: true,
            employee: {
              id: recognizeResponse.employee_id || 'Unknown',
              name: recognizeResponse.name || 'Unknown',
              department: recognizeResponse.department || 'Unknown',
            },
            confidence: recognizeResponse.confidence ?? undefined,
            message: `Successfully recognized: ${recognizeResponse.name}`,
          });
        } else {
          setResult({
            faceDetected: true,
            recognized: false,
            message: recognizeResponse.message || 'Face detected but not recognized in database',
          });
        }
      } catch (err: any) {
        setResult({
          faceDetected: true,
          recognized: false,
          message: err.response?.data?.detail || 'Face detected but recognition failed',
        });
      }
    } catch (err: any) {
      console.error('Verification error:', err);
      setResult({
        faceDetected: false,
        recognized: false,
        message: err.response?.data?.detail || 'Failed to verify face',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setCapturedImage(null);
    setResult(null);
    setShowWebcam(false);
  };

  return (
    <div className="w-full">
      <div className="mb-4 sm:mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Verify Face Detection</h1>
        <p className="text-sm sm:text-base text-gray-600 mt-2">
          Test face detection and recognition without marking attendance
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        {/* Camera/Image Section */}
        <div className="card">
          <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4">Capture Face</h2>

          {!capturedImage && !showWebcam && (
            <div className="text-center py-12">
              <Camera className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p className="text-gray-600 mb-4">Capture an image to verify face detection</p>
              <button
                onClick={() => setShowWebcam(true)}
                className="btn btn-primary"
              >
                <Camera className="w-4 h-4 mr-2" />
                Open Camera
              </button>
            </div>
          )}

          {showWebcam && (
            <div>
              <div className="relative bg-black rounded-lg overflow-hidden aspect-video mb-4">
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
                <div className="absolute bottom-3 sm:bottom-4 left-1/2 transform -translate-x-1/2 flex gap-3">
                  <button
                    onClick={() => setShowWebcam(false)}
                    className="btn btn-secondary px-4 sm:px-6"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={capture}
                    className="btn btn-primary px-6 sm:px-8"
                  >
                    <Camera className="w-4 sm:w-5 h-4 sm:h-5 mr-2" />
                    Capture
                  </button>
                </div>
              </div>
            </div>
          )}

          {capturedImage && (
            <div>
              <div className="relative rounded-lg overflow-hidden border-2 border-gray-200 mb-4">
                <img
                  src={capturedImage}
                  alt="Captured face"
                  className="w-full h-auto"
                />
              </div>
              <div className="flex flex-col sm:flex-row gap-3">
                <button
                  onClick={handleReset}
                  className="btn btn-secondary flex-1"
                  disabled={loading}
                >
                  Retake
                </button>
                <button
                  onClick={handleVerify}
                  className="btn btn-primary flex-1"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Verifying...
                    </>
                  ) : (
                    <>
                      <CheckCircle className="w-5 h-5 mr-2" />
                      Verify Face
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Results Section */}
        <div className="card">
          <h2 className="text-lg sm:text-xl font-semibold mb-3 sm:mb-4">Verification Results</h2>

          {!result ? (
            <div className="text-center py-12 text-gray-500">
              <AlertTriangle className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <p>Capture and verify an image to see results</p>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Face Detection Status */}
              <div className={`p-4 rounded-lg border-2 ${
                result.faceDetected
                  ? 'bg-green-50 border-green-200'
                  : 'bg-red-50 border-red-200'
              }`}>
                <div className="flex items-start">
                  {result.faceDetected ? (
                    <CheckCircle className="w-6 h-6 text-green-600 mr-3 flex-shrink-0 mt-0.5" />
                  ) : (
                    <XCircle className="w-6 h-6 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
                  )}
                  <div>
                    <h3 className="font-semibold text-base sm:text-lg mb-1">
                      {result.faceDetected ? 'Face Detected ✓' : 'No Face Detected ✗'}
                    </h3>
                    <p className={`text-sm ${
                      result.faceDetected ? 'text-green-700' : 'text-red-700'
                    }`}>
                      {result.faceDetected
                        ? 'A face was successfully detected in the image'
                        : 'No face found. Please ensure your face is clearly visible'}
                    </p>
                  </div>
                </div>
              </div>

              {/* Recognition Status */}
              {result.faceDetected && (
                <div className={`p-4 rounded-lg border-2 ${
                  result.recognized
                    ? 'bg-blue-50 border-blue-200'
                    : 'bg-orange-50 border-orange-200'
                }`}>
                  <div className="flex items-start">
                    {result.recognized ? (
                      <User className="w-6 h-6 text-blue-600 mr-3 flex-shrink-0 mt-0.5" />
                    ) : (
                      <AlertTriangle className="w-6 h-6 text-orange-600 mr-3 flex-shrink-0 mt-0.5" />
                    )}
                    <div className="flex-1">
                      <h3 className="font-semibold text-base sm:text-lg mb-1">
                        {result.recognized ? 'Face Recognized ✓' : 'Face Not Recognized'}
                      </h3>
                      <p className={`text-sm mb-3 ${
                        result.recognized ? 'text-blue-700' : 'text-orange-700'
                      }`}>
                        {result.message}
                      </p>

                      {result.recognized && result.employee && (
                        <div className="bg-white rounded-lg p-3 space-y-2">
                          <div className="grid grid-cols-2 gap-3 text-sm">
                            <div>
                              <p className="text-gray-500 text-xs">Employee ID</p>
                              <p className="font-semibold text-gray-900">{result.employee.id}</p>
                            </div>
                            <div>
                              <p className="text-gray-500 text-xs">Name</p>
                              <p className="font-semibold text-gray-900">{result.employee.name}</p>
                            </div>
                            <div>
                              <p className="text-gray-500 text-xs">Department</p>
                              <p className="font-semibold text-gray-900">{result.employee.department}</p>
                            </div>
                            {result.confidence && (
                              <div>
                                <p className="text-gray-500 text-xs">Confidence</p>
                                <p className="font-semibold text-gray-900">
                                  {(result.confidence * 100).toFixed(1)}%
                                </p>
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Info Message */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-sm text-blue-800">
                  <strong>Note:</strong> This is a test page. No attendance has been marked.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Tips */}
      <div className="mt-4 sm:mt-6 card bg-yellow-50 border border-yellow-200">
        <h3 className="text-base sm:text-lg font-semibold text-yellow-900 mb-2">
          Tips for Best Results
        </h3>
        <ul className="list-disc list-inside text-xs sm:text-sm text-yellow-800 space-y-1">
          <li>Ensure your face is clearly visible and well-lit</li>
          <li>Face the camera directly without tilting your head too much</li>
          <li>Remove glasses, masks, or anything covering your face</li>
          <li>Make sure there's only one face in the frame</li>
          <li>Position yourself at a reasonable distance from the camera</li>
        </ul>
      </div>
    </div>
  );
};

export default VerifyFace;
