import { LoginRequestBuilder, ResetPasswordRequestBuilder } from './builder'

import apiservice from '../service'
import { mapUser } from '../mapper'

export const login = async (credentials: LoginRequestBuilder) => {
    const response = await apiservice.post('/auth/login/', credentials.build())
    return {
        user: mapUser(response.data.user),
        token: response.data.token,
    }
}

export const resetPassword = async (
    credentials: ResetPasswordRequestBuilder,
) => {
    const response = await apiservice.post(
        '/auth/reset_password',
        credentials.build(),
    )
    return {
        message: response.data.message,
    }
}

export const logout = async () => {
    const response = await apiservice.post('/auth/logout/')
    return {
        message: response.data.message,
    }
}
