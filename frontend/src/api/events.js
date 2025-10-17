import apiClient from './client';

export const eventsAPI = {
  getEventByQR: async (qrToken) => {
    const response = await apiClient.get(`/events/qr/${qrToken}`);
    return response.data;
  },

  getAllEvents: async () => {
    const response = await apiClient.get('/events');
    return response.data;
  },

  getEventById: async (eventId) => {
    const response = await apiClient.get(`/events/${eventId}`);
    return response.data;
  },
};
