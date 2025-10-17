import apiClient from './client';

export const levelsAPI = {
  getEventLevels: async (eventId) => {
    const response = await apiClient.get(`/events/${eventId}/levels`);
    return response.data;
  },

  getLevelDetails: async (eventId, levelId) => {
    const response = await apiClient.get(`/events/${eventId}/levels/${levelId}`);
    return response.data;
  },
};
