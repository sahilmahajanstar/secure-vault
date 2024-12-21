import { ProfileCreateRequestBuilder } from './builder'
import apiservice from '../service'

const profile = '/profiles'

export const createProfile = async (
    credentials: ProfileCreateRequestBuilder,
) => {
    return apiservice.post(profile, credentials.build(), {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
}
