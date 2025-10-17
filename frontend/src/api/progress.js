import apiClient from './client';

export const progressAPI = {
  getUserProgress: async (eventId) => {
    const response = await apiClient.get(`/events/${eventId}/progress`);
    return response.data;
  },

  startLevel: async (eventId, levelId, deviceInfo = {}) => {
    const response = await apiClient.post(
      `/events/${eventId}/levels/${levelId}/start`,
      { device_info: deviceInfo }
    );
    return response.data;
  },

  completeLevel: async (eventId, levelId, progressId, resultData, isPassed) => {
    const response = await apiClient.post(
      `/events/${eventId}/levels/${levelId}/complete`,
      {
        progress_id: progressId,
        result_data: resultData,
        is_passed: isPassed,
      }
    );
    return response.data;
  },
};
