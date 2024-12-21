import { VerifyEmailType } from './type'

export class VerifyEmailRequestBuilder {
    email: string = ''
    username: string = ''
    type: string = ''

    setEmail(email: string) {
        this.email = email
        return this
    }

    setType(type: VerifyEmailType) {
        this.type = type
        return this
    }

    setUsername(username: string) {
        this.username = username
        return this
    }

    build() {
        return {
            email: this.email,
            type: this.type,
            username: this.username,
        }
    }
}

export class VerifyEmailOTPRequestBuilder {
    otp: string = ''
    email: string = ''
    type: string = ''

    setOTP(otp: string) {
        this.otp = otp
        return this
    }

    setEmail(email: string) {
        this.email = email
        return this
    }

    setType(type: VerifyEmailType) {
        this.type = type
        return this
    }

    build() {
        return {
            otp: this.otp,
            email: this.email,
            type: this.type,
        }
    }
}
