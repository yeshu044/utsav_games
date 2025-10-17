import apiClient from './client';

export const authAPI = {
  sendOTP: async (phoneNumber) => {
    const response = await apiClient.post('/auth/send-otp', {
      phone_number: phoneNumber,
    });
    return response.data;
  },

  verifyOTP: async (phoneNumber, otpCode, name = null) => {
    const response = await apiClient.post('/auth/verify-otp', {
      phone_number: phoneNumber,
      otp_code: otpCode,
      name,
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  updateProfile: async (data) => {
    const response = await apiClient.put('/auth/me', null, {
      params: data,
    });
    return response.data;
  },
};
