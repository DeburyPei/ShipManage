import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";



  const http = axios.create({
    // timeout: 1000 * 86400,
    withCredentials: true,
    baseURL: 'http://localhost:8080/api/',
    headers: {
        'Content-Type': 'application/json; charset=utf-8'
    }
})

export default http