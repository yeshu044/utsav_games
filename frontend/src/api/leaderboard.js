import apiClient from './client';

export const leaderboardAPI = {
  getLeaderboard: async (eventId, filter = 'all', limit = 50, offset = 0) => {
    const response = await apiClient.get(`/events/${eventId}/leaderboard`, {
      params: { filter, limit, offset },
    });
    return response.data;
  },

  getMyRank: async (eventId) => {
    const response = await apiClient.get(`/events/${eventId}/leaderboard/me`);
    return response.data;
  },
};
