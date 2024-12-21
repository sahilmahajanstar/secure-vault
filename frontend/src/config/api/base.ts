import axios from 'axios'
import { dispatch } from '../redux/store'
import { mapUser } from './mapper'
import { userActions } from '../../users/reducer/userReducer'

const API_BASE_URL = import.meta.env.VITE_API_URL

const axiosInstance = axios.create({
    baseURL: API_BASE_URL,
    timeout: 60000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor
axiosInstance.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => {
        return Promise.reject(error)
    },
)

// Response interceptor
axiosInstance.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config

        // Handle 401 Unauthorized
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true
            try {
                const refreshToken = localStorage.getItem('refreshToken')
                if (!refreshToken) {
                    dispatch(userActions.unauthenticate())
                    localStorage.clear()
                    if (
                        window.location.pathname.includes('/files/share/link')
                    ) {
                        window.location.href = '/users/login'
                    }
                    return Promise.reject(error)
                }
                const response = await axiosInstance.post(
                    '/auth/refresh/',
                    {
                        refresh_token: refreshToken,
                    },
                    // @ts-expect-error axios doesn't support _retry
                    { _retry: true },
                )
                const { token, user } = response.data.data
                dispatch(
                    userActions.setUserInfo({
                        user: mapUser(user)!,
                        token: token.access,
                        refreshToken: token.refresh,
                    }),
                )
                // Retry original request
                originalRequest.headers.Authorization = `Bearer ${token.token}`
                return axiosInstance(originalRequest)
            } catch (refreshError) {
                // Handle refresh token failure
                localStorage.clear()
                dispatch(userActions.unauthenticate())
                if (window.location.pathname.includes('/files/share/link')) {
                    window.location.href = '/users/login'
                }
                return Promise.reject(refreshError)
            }
        }

        return Promise.reject(error)
    },
)

export default axiosInstance
