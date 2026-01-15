import axios from 'axios';
import Constants from 'expo-constants';

// Get API URL from app.json extra or fallback to localhost
const getApiUrl = () => {
    const apiUrl = Constants.expoConfig?.extra?.apiUrl;
    // Production Render Backend
    return apiUrl || 'https://mulberry-backend-enx1.onrender.com';
};

const BASE_URL = getApiUrl();

const api = axios.create({
    baseURL: BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const mulberryApi = {
    /**
     * Predict yield based on quality and environmental factors.
     * @param {number} avgQuality - 0 to 1 score from vision model
     * @param {number} temperature - in Celsius
     * @param {number} humidity - percentage
     * @returns {Promise<number>} - Predicted yield
     */
    predictYield: async (avgQuality, temperature, humidity) => {
        try {
            const response = await api.post('/predict/yield', {
                avg_quality: avgQuality,
                temperature: temperature,
                humidity: humidity,
            });
            return response.data.estimated_yield;
        } catch (error) {
            console.error("Yield prediction error:", error);
            throw error;
        }
    },

    /**
     * Check backend health
     */
    checkHealth: async () => {
        try {
            const response = await api.get('/health');
            return response.data;
        } catch (error) {
            console.error("Health check error:", error);
            return null;
        }
    },

    /**
     * Predict leaf quality (Fallback if LiteRT fails)
     * @param {string} imageBase64 
     */
    predictQuality: async (fileUri) => {
        try {
            const formData = new FormData();
            formData.append('file', {
                uri: fileUri,
                name: 'leaf.jpg',
                type: 'image/jpeg',
            });

            const response = await api.post('/predict/leaf-quality', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            return response.data;
        } catch (error) {
            console.error("Quality prediction error:", error);
            throw error;
        }
    }
};
