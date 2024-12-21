export class LoginRequestBuilder {
    username!: string
    password!: string
    otp!: string

    setUsername(username: string) {
        this.username = username
        return this
    }

    setPassword(password: string) {
        this.password = password
        return this
    }

    setOtp(otp: string) {
        this.otp = otp
        return this
    }

    build() {
        return {
            username: this.username,
            password: this.password,
            otp: this.otp,
        }
    }
}

export class ResetPasswordRequestBuilder {
    email!: string
    new_password!: string
    otp!: string

    setEmail(email: string) {
        this.email = email
        return this
    }

    setNewPassword(new_password: string) {
        this.new_password = new_password
        return this
    }

    setOtp(otp: string) {
        this.otp = otp
        return this
    }

    build() {
        return {
            email: this.email,
            new_password: this.new_password,
            otp: this.otp,
        }
    }
}
