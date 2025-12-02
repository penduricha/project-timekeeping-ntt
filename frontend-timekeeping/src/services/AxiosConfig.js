import axios from "axios";

export default class AxiosConfig {
    constructor() {

    }

    getAPIClientFromBackendJava(){
        const port = '8080';
        return axios.create({
            baseURL: `http://localhost:${port}/api`,
            headers: {
                'Content-Type': 'application/json',
                // Thiết lập header Authorization
            }
        });
    }

    getAPIClientFromBackendPython(){
        const port = '5000';
        return axios.create({
            baseURL: `http://localhost:${port}/api`,
            headers: {
                'Content-Type': 'application/json',
                // Thiết lập header Authorization
            }
        });
    }
}