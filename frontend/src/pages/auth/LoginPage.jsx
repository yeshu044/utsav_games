import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Phone, Key, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { authAPI } from '../../api/auth';
import { useAuthStore } from '../../stores/authStore';

function LoginPage() {
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);
  
  const [step, setStep] = useState('phone'); // 'phone' or 'otp'
  const [phoneNumber, setPhoneNumber] = useState('+91');
  const [otpCode, setOtpCode] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [isNewUser, setIsNewUser] = useState(false);

  const handleSendOTP = async (e) => {
    e.preventDefault();
    
    if (phoneNumber.length !== 13) {
      toast.error('Please enter a valid 10-digit phone number');
      return;
    }

    setLoading(true);
    try {
      await authAPI.sendOTP(phoneNumber);
      toast.success('OTP sent to your phone!');
      setStep('otp');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to send OTP');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    
    if (otpCode.length !== 6) {
      toast.error('Please enter a valid 6-digit OTP');
      return;
    }

    if (isNewUser && !name.trim()) {
      toast.error('Please enter your name');
      return;
    }

    setLoading(true);
    try {
      const response = await authAPI.verifyOTP(
        phoneNumber,
        otpCode,
        isNewUser ? name : null
      );
      
      setAuth(response.user, response.access_token);
      toast.success('Login successful!');
      
      // Redirect to event or dashboard
      // For now, just show success
      setTimeout(() => {
        navigate('/');
      }, 1000);
    } catch (error) {
      const errorMsg = error.response?.data?.detail;
      
      if (errorMsg?.includes('Name is required')) {
        setIsNewUser(true);
        toast.error('Please enter your name to continue');
      } else {
        toast.error(errorMsg || 'Invalid OTP. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handlePhoneChange = (e) => {
    const value = e.target.value;
    if (value.startsWith('+91') && value.length <= 13) {
      setPhoneNumber(value);
    }
  };

  const handleOTPChange = (e) => {
    const value = e.target.value.replace(/\D/g, '');
    if (value.length <= 6) {
      setOtpCode(value);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-100 via-white to-secondary-100 p-4">
      <div className="w-full max-w-md">
        {/* Logo/Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-display font-bold text-primary-600 mb-2">
            🎮 Utsav Games
          </h1>
          <p className="text-gray-600">
            Play games, guess names, win prizes!
          </p>
        </div>

        {/* Login Card */}
        <div className="card">
          {step === 'phone' ? (
            // Step 1: Phone Number
            <form onSubmit={handleSendOTP}>
              <div className="mb-6">
                <h2 className="text-2xl font-bold mb-2">Login</h2>
                <p className="text-gray-600">
                  Enter your phone number to receive an OTP
                </p>
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number
                </label>
                <div className="relative">
                  <Phone className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    type="tel"
                    value={phoneNumber}
                    onChange={handlePhoneChange}
                    placeholder="+919876543210"
                    className="input pl-12"
                    required
                    autoFocus
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Format: +91 followed by 10 digits
                </p>
              </div>

              <button
                type="submit"
                disabled={loading || phoneNumber.length !== 13}
                className="btn-primary w-full flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Sending OTP...
                  </>
                ) : (
                  'Send OTP'
                )}
              </button>
            </form>
          ) : (
            // Step 2: OTP Verification
            <form onSubmit={handleVerifyOTP}>
              <div className="mb-6">
                <h2 className="text-2xl font-bold mb-2">Verify OTP</h2>
                <p className="text-gray-600">
                  Enter the 6-digit code sent to
                  <br />
                  <span className="font-semibold">{phoneNumber}</span>
                </p>
                <button
                  type="button"
                  onClick={() => {
                    setStep('phone');
                    setOtpCode('');
                    setName('');
                    setIsNewUser(false);
                  }}
                  className="text-primary-600 text-sm mt-1 hover:underline"
                >
                  Change number
                </button>
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  OTP Code
                </label>
                <div className="relative">
                  <Key className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <input
                    type="text"
                    inputMode="numeric"
                    value={otpCode}
                    onChange={handleOTPChange}
                    placeholder="123456"
                    className="input pl-12 text-center text-2xl tracking-widest"
                    required
                    autoFocus
                    maxLength={6}
                  />
                </div>
              </div>

              {isNewUser && (
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Your Name
                  </label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter your name"
                    className="input"
                    required
                  />
                </div>
              )}

              <button
                type="submit"
                disabled={loading || otpCode.length !== 6}
                className="btn-primary w-full flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Verifying...
                  </>
                ) : (
                  'Verify & Login'
                )}
              </button>

              <div className="mt-4 text-center">
                <button
                  type="button"
                  onClick={handleSendOTP}
                  disabled={loading}
                  className="text-sm text-gray-600 hover:text-primary-600"
                >
                  Didn't receive code? Resend OTP
                </button>
              </div>
            </form>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-6 text-sm text-gray-600">
          <p>By continuing, you agree to our Terms & Privacy Policy</p>
        </div>

        {/* Dev Helper - Remove in production */}
        {import.meta.env.DEV && step === 'otp' && (
          <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-xs text-yellow-800 font-mono">
              <strong>Dev Mode:</strong> Check your backend console for the OTP code
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default LoginPage;
