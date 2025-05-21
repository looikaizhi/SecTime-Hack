import axios from 'axios';
const API_BASE_URL = 'http://localhost:3001';
const api = {
    getSuiCoinList: async () => {
        try{
            const response = await axios.get(`${API_BASE_URL}/api/coinList`);
            console.log("Sui Coin List:", response.data);
            return response.data;
        }
        catch (error) {
            console.error("Error fetching Sui Coin List:", error);
            return [];
        }
    },

    getSuiCoinInfo: async (coinId?: string) => {
        try{
            const response = await axios.get(`${API_BASE_URL}/api/coinInfo`, {
                params: coinId ? { coin_id: coinId } : {}
            });
            console.log("Sui Coin Info:", response.data);
            return response.data;
        }
        catch (error) {
            console.error("Error fetching Sui Coin Info:", error);
            return null;
        }
    },

    getSuiCoinWeight: async (coinId?: string) => {
        try{
            const response = await axios.get(`${API_BASE_URL}/api/coinWeight`, {
                params: coinId ? { coin_id: coinId } : {}
            });
            console.log("Sui Coin Weight:", response.data);
            return response.data;
        }
        catch (error) {
            console.error("Error fetching Sui Coin Weight:", error);
            return null;
        }
    }

}

export default api;