import axios from 'axios';
import Constants from 'expo-constants';

// Use host URI for local dev or a default
const BASE_URL = Constants.expoConfig.extra.apiUrl || 'http://localhost:8000';

const api = axios.create({
    baseURL: BASE_URL,
    timeout: 10000,
});

export const mulberryApi = {
    checkHealth: async () => {
        try {
            const response = await api.get('/health');
            return response.data;
        } catch (error) {
            console.error('Health check failed', error);
            throw error;
        }
    },

    predictQuality: async (imageUri) => {
        const formData = new FormData();
        formData.append('file', {
            uri: imageUri,
            name: 'leaf.jpg',
            type: 'image/jpeg',
        });

        try {
            const response = await api.post('/predict/leaf-quality', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            return response.data;
        } catch (error) {
            console.error('Quality prediction failed', error);
            throw error;
        }
    },

    predictYield: async (avgQuality, temperature, humidity) => {
        try {
            const response = await api.post('/predict/yield', {
                avg_quality: avgQuality,
                temperature,
                humidity,
            });
            return response.data;
        } catch (error) {
            console.error('Yield prediction failed', error);
            throw error;
        }
    },
};
