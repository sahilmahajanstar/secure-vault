export class RegisterRequestBuilder {
    username: string = ''
    password: string = ''
    email: string = ''
    first_name: string = ''
    last_name: string = ''
    phone: string = ''
    country_code: string = ''

    setUsername(username: string) {
        this.username = username
        return this
    }

    setPassword(password: string) {
        this.password = password
        return this
    }

    setEmail(email: string) {
        this.email = email
        return this
    }

    setFirstName(firstName: string) {
        this.first_name = firstName
        return this
    }

    setLastName(lastName: string) {
        this.last_name = lastName
        return this
    }

    setPhone(phone: string) {
        this.phone = phone
        return this
    }

    setCountryCode(countryCode: string) {
        this.country_code = countryCode
        return this
    }

    build() {
        return {
            username: this.username,
            password: this.password,
            email: this.email,
            first_name: this.first_name,
            last_name: this.last_name,
            // phone_number: this.phone,
            // country_code: this.country_code
        }
    }
}
