import {
    VerifyEmailOTPRequestBuilder,
    VerifyEmailRequestBuilder,
} from './builder'

import apiservice from '../service'

const verify = '/verify'

export const verifyEmail = async (request: VerifyEmailRequestBuilder) => {
    return apiservice.post(verify + '/email/', request.build())
}

export const validateEmailOTP = async (
    request: VerifyEmailOTPRequestBuilder,
) => {
    return apiservice.post(verify + '/validate_email/', request.build())
}
