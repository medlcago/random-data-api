import axios from "axios";

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8080/api/v1/users'
});

export const getUser = async () => {
    try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await instance.get("/me", {
            headers: {
                Authorization: `Bearer ${accessToken}`

            }
        });
        return response.data;
    } catch (error) {
        console.log("Failed to get user");
    }
}

export const registerUser = async (username, telegram, password) => {
    try {
        const response = await instance.post("/", {
            email: username,
            telegram: telegram ? telegram : null,
            password: password,
        });
        const accessToken = response.data.token.access_token;
        const refreshToken = response.data.token.refresh_token;
        localStorage.setItem("accessToken", accessToken);
        localStorage.setItem("refreshToken", refreshToken);
        return {
            access_token: accessToken,
            refresh_token: refreshToken
        }
    } catch (error) {
        console.log("Failed to register user");
    }
}