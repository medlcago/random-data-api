import axios from "axios";

const instance = axios.create({
    baseURL: 'http://127.0.0.1:8080/api/v1/login'
});

export const loginUser = async (username, password) => {
    try {
        const response = await instance.post("/access-token", new URLSearchParams({
            username: username,
            password: password
        }));

        console.log("Login successful!");
        const accessToken = response.data.access_token;
        const refreshToken = response.data.refresh_token;

        localStorage.setItem("accessToken", accessToken);
        localStorage.setItem("refreshToken", refreshToken);
        return {
            access_token: accessToken,
            refresh_token: refreshToken
        };
    } catch (error) {
        console.log("Login failed. Invalid username or password.");
    }
}


export const logoutUser = async () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    console.log("Logout successful!");
}

export const verifyAccessToken = async () => {
    try {
        const token = localStorage.getItem("accessToken");
        if (!token) {
            return false;
        }
        const response = await instance.post("/verify-token", {
            token: token
        });
        return response.data.token_type === "access";
    } catch (error) {
        return false;
    }
}

export const refreshAccessToken = async () => {
    try {
        const refreshToken = localStorage.getItem("refreshToken");
        if (!refreshToken) {
            return false;
        }
        const response = await instance.post("/refresh-token", null, {
            headers: {
                "Authorization": `Bearer ${refreshToken}`

            }
        });
        const accessToken = response.data.access_token;
        localStorage.setItem("accessToken", accessToken);
        return true;
    } catch (error) {
        return false;
    }
}