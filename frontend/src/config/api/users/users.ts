import { mapProfile, mapUser } from '../mapper'

import { RegisterRequestBuilder } from './builder'
import apiservice from '../service'

export const register = async (userData: RegisterRequestBuilder) => {
    const response = await apiservice.post('/users/', userData.build())
    return {
        user: mapUser(response.data.user),
        token: response.data.token,
    }
}

export const getUser = async () => {
    const response = await apiservice.get('/users/me')
    return {
        user: mapUser(response.data.user),
        profile: mapProfile(response.data.profile),
    }
}
