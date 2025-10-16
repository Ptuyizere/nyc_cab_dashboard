import axios from "axios";

let API_LINK = "http://127.0.0.1:8000";

export async function fetchPagedTrips(limit = 10, offset = 0) {
    let response = await axios.get(`${API_LINK}/trips`, {
        params: {limit, offset},
    });
    return response.data;
}

export async function fetchAllTripsStats() {
    let response = await axios.get(`${API_LINK}/stats`);
    return response.data;
}