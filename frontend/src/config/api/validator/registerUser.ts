export interface RegisterUserValidation {
    firstName: string
    lastName: string
    email: string
    password: string
    username: string
}

export class RegisterUserValidator {
    private static EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    private static NAME_REGEX = /^[a-zA-Z\s]*$/
    private static PASSWORD_REGEX =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/
    private static USERNAME_REGEX = /^[a-zA-Z0-9._]{3,30}$/

    static validateFirstName(firstName: string): string | null {
        if (!firstName) {
            return 'First name is required'
        }
        if (firstName.length < 2) {
            return 'First name must be at least 2 characters'
        }
        if (firstName.length > 50) {
            return 'First name cannot exceed 50 characters'
        }
        if (!this.NAME_REGEX.test(firstName)) {
            return 'First name can only contain letters and spaces'
        }
        return null
    }

    static validateLastName(lastName: string): string | null {
        if (!lastName) {
            return 'Last name is required'
        }
        if (lastName.length < 2) {
            return 'Last name must be at least 2 characters'
        }
        if (lastName.length > 50) {
            return 'Last name cannot exceed 50 characters'
        }
        if (!this.NAME_REGEX.test(lastName)) {
            return 'Last name can only contain letters and spaces'
        }
        return null
    }

    static validateEmail(email: string): string | null {
        if (!email) {
            return 'Email is required'
        }
        if (!this.EMAIL_REGEX.test(email)) {
            return 'Invalid email format'
        }
        if (email.length > 255) {
            return 'Email cannot exceed 255 characters'
        }
        return null
    }

    static validatePassword(password: string): string | null {
        if (!password) {
            return 'Password is required'
        }
        if (password.length < 8) {
            return 'Password must be at least 8 characters'
        }
        if (password.length > 100) {
            return 'Password cannot exceed 100 characters'
        }
        if (!this.PASSWORD_REGEX.test(password)) {
            return 'Password must contain at least one uppercase letter, one lowercase letter, one number and one special character'
        }
        return null
    }

    static validateUsername(username: string): string | null {
        if (!username) {
            return 'Username is required'
        }
        console.log(this.USERNAME_REGEX.test(username), '--------')
        if (!this.USERNAME_REGEX.test(username)) {
            return 'Username must be alphanumeric, underscore, dot, 3-30 characters'
        }
        return null
    }

    static validate(data: RegisterUserValidation): {
        isValid: boolean
        errors: Partial<Record<keyof RegisterUserValidation, string>>
    } {
        const errors: Partial<Record<keyof RegisterUserValidation, string>> = {}

        const firstNameError = this.validateFirstName(data.firstName)
        if (firstNameError) errors.firstName = firstNameError

        const lastNameError = this.validateLastName(data.lastName)
        if (lastNameError) errors.lastName = lastNameError

        const emailError = this.validateEmail(data.email)
        if (emailError) errors.email = emailError

        const passwordError = this.validatePassword(data.password)
        if (passwordError) errors.password = passwordError

        const usernameError = this.validateUsername(data.username)
        if (usernameError) errors.username = usernameError

        return {
            isValid: Object.keys(errors).length === 0,
            errors,
        }
    }
}
