/* eslint-disable @typescript-eslint/no-explicit-any */
// src/services/api.service.js
import axios from './base'

class Api {
    generateParams(params?: { [key: string]: string | number }) {
        let queryString = '?'
        if (!params) {
            return ''
        }
        for (const key in params) {
            const val = params[key]
            queryString += `${key}=${val}&`
        }
        return queryString
    }

    async get(
        url: string,
        params?: { [key: string]: string | number },
        config = {},
    ) {
        try {
            const queryString = this.generateParams(params)
            const response = await axios.get(url + queryString, config)
            return response.data
        } catch (error: any) {
            throw error.response.data.error
        }
    }

    async post(url: string, data = {}, config = {}) {
        try {
            const response = await axios.post(url, data, config)
            return response.data
        } catch (error: any) {
            throw error.response.data.error
        }
    }

    async put(url: string, data = {}, config = {}) {
        try {
            const response = await axios.put(url, data, config)
            return response.data
        } catch (error: any) {
            throw error.response.data.error
        }
    }

    async delete(url: string, config = {}) {
        try {
            const response = await axios.delete(url, config)
            return response.data
        } catch (error: any) {
            throw error.response.data.error
        }
    }
}

const ApiService = new Api()
export default ApiService
